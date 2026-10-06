import requests
from app.config import settings

def generate(model, prompt):
    response=requests.post(f"{settings.ollama_url}/api/generate",json={"model":model,"prompt":prompt,"stream":False,"options":{"temperature":0.2}},timeout=180)
    response.raise_for_status()
    data=response.json()
    return {"text":data.get('response','').strip(),"input_tokens":int(data.get('prompt_eval_count',0) or 0),"output_tokens":int(data.get('eval_count',0) or 0)}
