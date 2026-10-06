from pathlib import Path
import re
from pypdf import PdfReader
from docx import Document
from app.services.embeddings import embed_texts
from app.db.repository import insert_chunks

def load_document(path: Path):
    suffix=path.suffix.lower()
    if suffix=='.txt': return path.read_text(encoding='utf-8',errors='ignore')
    if suffix=='.pdf': return '\n\n'.join((p.extract_text() or '') for p in PdfReader(str(path)).pages)
    if suffix=='.docx': return '\n'.join(p.text for p in Document(str(path)).paragraphs)
    raise ValueError('Only PDF, DOCX and TXT are supported')

def clean_text(text):
    text=text.replace('\x00',' ')
    text=re.sub(r'[ \t]+',' ',text)
    text=re.sub(r'\n{3,}','\n\n',text)
    return text.strip()

def chunk_text(text, chunk_size=1200, overlap=200):
    text=clean_text(text)
    chunks=[]; start=0
    while start < len(text):
        end=min(start+chunk_size,len(text))
        if end < len(text):
            boundary=text.rfind('\n',start,end)
            if boundary < start+chunk_size//2: boundary=text.rfind(' ',start,end)
            if boundary >= start+chunk_size//2: end=boundary
        chunk=text[start:end].strip()
        if chunk: chunks.append(chunk)
        if end>=len(text): break
        start=max(end-overlap,start+1)
    return chunks

def index_file(path, brand_name):
    text=load_document(path)
    chunks=chunk_text(text)
    if not chunks: raise ValueError('No readable text found')
    count=insert_chunks(brand_name,path.name,chunks,embed_texts(chunks))
    return count
