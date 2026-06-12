from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import os
import shutil

from app.utils.pdf_loader import extract_pdf_pages
from app.rag.document_processor import create_documents
from app.rag.vector_store import (
    create_vector_store,
    similarity_search
)
from pydantic import BaseModel
from app.rag.rag_service import ask_question
from fastapi.responses import StreamingResponse


class ChatRequest(BaseModel):
    question: str

app = FastAPI()

UPLOAD_DIR = "data/raw"

os.makedirs(UPLOAD_DIR, exist_ok=True)


class SearchRequest(BaseModel):
    query: str


@app.get("/")
def root():
    return {"message": "University Bylaw RAG API Running"}


@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    pages = extract_pdf_pages(file_path)

    documents = create_documents(
        pages,
        file.filename
    )

    create_vector_store(documents)

    return {
        "message": "PDF uploaded and indexed successfully",
        "filename": file.filename,
        "total_chunks": len(documents)
    }


@app.post("/search")
def search(request: SearchRequest):

    results = similarity_search(request.query)

    response = []

    for result in results:
        response.append(result.page_content)

    return {
        "query": request.query,
        "results": response
    }

@app.post("/chat")
def chat(request: ChatRequest):

    response = ask_question(
        request.question
    )

    return response

