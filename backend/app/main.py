import os
import uuid
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from .services.extractor import extract_document
from .services.chunker import make_chunks, retrieve_chunks
from .services.ai import generate_summary, answer_question

load_dotenv()
app = FastAPI(title="DocuMind API", version="1.0.0")
origin = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")
app.add_middleware(CORSMiddleware, allow_origins=[origin, "http://localhost:5173"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

MAX_BYTES = int(os.getenv("MAX_FILE_SIZE_MB", "10")) * 1024 * 1024
sessions = {}

class SummaryRequest(BaseModel):
    document_id: str
    length: str = Field(pattern="^(small|medium|large)$")

class ChatRequest(BaseModel):
    document_id: str
    question: str = Field(min_length=1, max_length=1000)

@app.get("/api/health")
def health():
    return {"status": "ok"}

@app.post("/api/upload")
async def upload(file: UploadFile = File(...)):
    data = await file.read()
    if len(data) > MAX_BYTES:
        raise HTTPException(413, f"File is too large. Maximum size is {MAX_BYTES // 1024 // 1024} MB.")
    try:
        pages = extract_document(file.filename or "document", data)
    except ValueError as e:
        raise HTTPException(400, str(e))
    except Exception as e:
        raise HTTPException(500, f"Document processing failed: {e}")
    doc_id = str(uuid.uuid4())
    chunks = make_chunks(pages)
    sessions[doc_id] = {"filename": file.filename, "pages": pages, "chunks": chunks}
    return {"document_id": doc_id, "filename": file.filename, "pages": len(pages), "characters": sum(len(p["text"]) for p in pages)}

@app.post("/api/summarize")
def summarize(request: SummaryRequest):
    doc = sessions.get(request.document_id)
    if not doc:
        raise HTTPException(404, "Document session not found. Please upload the document again.")
    try:
        result = generate_summary(doc["pages"], request.length)
        return result
    except Exception as e:
        raise HTTPException(502, f"Summary generation failed: {e}")

@app.post("/api/chat")
def chat(request: ChatRequest):
    doc = sessions.get(request.document_id)
    if not doc:
        raise HTTPException(404, "Document session not found. Please upload the document again.")
    chunks = retrieve_chunks(doc["chunks"], request.question)
    try:
        return answer_question(chunks, request.question)
    except Exception as e:
        raise HTTPException(502, f"Question answering failed: {e}")
