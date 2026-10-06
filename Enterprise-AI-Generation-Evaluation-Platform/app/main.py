from pathlib import Path
import shutil
import time
import uuid
from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.responses import Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

from app.db.connection import init_db
from app.db.repository import save_brand, get_brand, save_prompt, search_chunks, save_event
from app.models.schemas import BrandRequest, PromptRequest, GenerateRequest, EvaluationRequest
from app.services.ingestion import index_file
from app.services.embeddings import embed_texts
from app.services.prompts import build_prompt
from app.services.router import choose_model
from app.services.ollama import generate
from app.services.evaluation import safety_check, groundedness, quality_score
from app.services.metrics import GENERATIONS, FAILURES, LATENCY, SAFETY, QUALITY, COST, ACTIVE

UPLOAD_DIR=Path('documents'); UPLOAD_DIR.mkdir(exist_ok=True)
app=FastAPI(title='AI Generation & Evaluation Platform',version='1.0.0',description='Production-oriented RAG, prompt versioning, model routing, evaluation, guardrails and observability platform.')

@app.on_event('startup')
def startup(): init_db()

@app.get('/health')
def health(): return {'status':'ok'}

@app.get('/metrics')
def metrics(): return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.post('/brands')
def create_brand(request: BrandRequest):
    save_brand(request.model_dump())
    return {'message':'Brand configuration saved','brand_name':request.brand_name}

@app.post('/prompts')
def create_prompt(request: PromptRequest):
    save_prompt(request.name,request.version,request.system_instruction,request.active)
    return {'message':'Prompt version saved','name':request.name,'version':request.version,'active':request.active}

@app.post('/documents/upload')
async def upload_document(brand_name: str, file: UploadFile=File(...)):
    if not get_brand(brand_name): raise HTTPException(404,'Create the brand configuration first')
    suffix=Path(file.filename or '').suffix.lower()
    if suffix not in {'.pdf','.docx','.txt'}: raise HTTPException(400,'Only PDF, DOCX and TXT are supported')
    destination=UPLOAD_DIR/Path(file.filename).name
    with destination.open('wb') as buffer: shutil.copyfileobj(file.file,buffer)
    try:
        count=index_file(destination,brand_name)
        return {'filename':destination.name,'brand_name':brand_name,'chunks_created':count}
    except Exception as exc:
        if destination.exists(): destination.unlink()
        raise HTTPException(500,str(exc))

@app.post('/generate')
def generate_content(request: GenerateRequest):
    brand=get_brand(request.brand_name)
    if not brand: raise HTTPException(404,'Brand configuration not found')
    request_id=str(uuid.uuid4()); start=time.perf_counter(); ACTIVE.inc()
    model=choose_model(request.task,request.model); provider='ollama'
    try:
        sources=search_chunks(request.brand_name,embed_texts([request.question])[0],request.top_k)
        context='\n\n'.join(f"[Source {i}] {s['filename']}\n{s['content']}" for i,s in enumerate(sources,1))
        prompt_version,prompt=build_prompt(request.question,context,brand,request.prompt_version)
        result=generate(model,prompt)
        safety_pass,hits=safety_check(result['text'],brand['forbidden_terms'])
        grounded=groundedness(result['text'],sources)
        quality=quality_score(result['text'],sources,safety_pass)
        latency=(time.perf_counter()-start)*1000
        # Local Ollama has no provider billing. This field is an explicit configurable estimate placeholder.
        estimated_cost=0.0
        GENERATIONS.labels(model,provider,request.brand_name).inc(); LATENCY.labels(model,provider).observe(latency/1000); QUALITY.labels(request.brand_name).observe(quality); COST.labels(model,provider).inc(estimated_cost)
        if not safety_pass: SAFETY.labels(request.brand_name).inc()
        save_event({'request_id':request_id,'brand_name':request.brand_name,'model':model,'provider':provider,'prompt_version':prompt_version,'input_tokens':result['input_tokens'],'output_tokens':result['output_tokens'],'estimated_cost_usd':estimated_cost,'latency_ms':latency,'quality_score':quality,'safety_pass':safety_pass,'groundedness_score':grounded})
        if not safety_pass:
            return {'request_id':request_id,'status':'blocked','answer':'Generation blocked by brand safety guardrails.','violations':hits,'evaluation':{'quality_score':quality,'groundedness':grounded,'safety_pass':False},'sources':sources}
        return {'request_id':request_id,'status':'ok','model':model,'provider':provider,'prompt_version':prompt_version,'answer':result['text'],'evaluation':{'quality_score':quality,'groundedness':grounded,'safety_pass':True},'usage':{'input_tokens':result['input_tokens'],'output_tokens':result['output_tokens'],'estimated_cost_usd':estimated_cost},'latency_ms':round(latency,2),'sources':[{'filename':s['filename'],'similarity':round(s['similarity'],4),'chunk_id':s['id']} for s in sources]}
    except Exception:
        FAILURES.labels(model,provider).inc(); raise
    finally: ACTIVE.dec()

@app.post('/evaluate')
def evaluate(request: EvaluationRequest):
    brand=get_brand(request.brand_name)
    if not brand: raise HTTPException(404,'Brand configuration not found')
    sources=[{'content':x} for x in request.source_texts]
    safety_pass,hits=safety_check(request.answer,brand['forbidden_terms'])
    grounded=groundedness(request.answer,sources)
    quality=quality_score(request.answer,sources,safety_pass)
    return {'quality_score':quality,'groundedness':grounded,'safety_pass':safety_pass,'violations':hits}
