from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, HttpUrl, validator
import logging
import time
from typing import Optional

from app.ingest import scrape_website, chunk_text
from app.store import vector_store
from app.rag import rag_query
from app.middleware import RateLimitMiddleware

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="RAG Backend API",
    description="Retrieval-Augmented Generation Backend Service",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    RateLimitMiddleware,
    calls=10,  # 10 requests per minute
    period=60   # per minute
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["GET", "POST"],  # Restrict to necessary methods
    allow_headers=["*"],
)

class IngestRequest(BaseModel):
    url: HttpUrl
    
    @validator('url')
    def validate_url(cls, v):
        # Add URL validation logic if needed
        return str(v)

class QueryRequest(BaseModel):
    question: str
    
    @validator('question')
    def validate_question(cls, v):
        if not v or len(v.strip()) < 3:
            raise ValueError('Question must be at least 3 characters long')
        if len(v) > 1000:
            raise ValueError('Question must be less than 1000 characters')
        return v.strip()

class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
    timestamp: float

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unexpected error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc) if app.debug else "An unexpected error occurred",
            "timestamp": time.time()
        }
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "timestamp": time.time()
        }
    )

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "version": "1.0.0"
    }

@app.post("/ingest")
async def ingest_data(req: IngestRequest):
    """Ingest content from a URL"""
    start_time = time.time()
    logger.info(f"Starting ingestion for URL: {req.url}")
    
    try:
        text = scrape_website(req.url)
        if not text:
            raise HTTPException(
                status_code=400,
                detail="Failed to scrape content from the provided URL"
            )
        
        chunks = chunk_text(text)
        if not chunks:
            raise HTTPException(
                status_code=400,
                detail="No content could be extracted from the URL"
            )
        
        vector_store.add_texts(chunks)
        
        processing_time = time.time() - start_time
        logger.info(f"Successfully ingested {len(chunks)} chunks in {processing_time:.2f}s")
        
        return {
            "chunks": len(chunks),
            "processing_time": processing_time,
            "url": str(req.url)
        }
    
    except Exception as e:
        logger.error(f"Ingestion failed for URL {req.url}: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Ingestion failed: {str(e)}"
        )

@app.post("/ask")
async def ask_question(req: QueryRequest):
    """Ask a question using RAG"""
    start_time = time.time()
    logger.info(f"Processing question: {req.question[:100]}...")
    
    try:
        answer = rag_query(req.question)
        processing_time = time.time() - start_time
        
        logger.info(f"Question answered in {processing_time:.2f}s")
        
        return {
            "answer": answer,
            "question": req.question,
            "processing_time": processing_time
        }
    
    except Exception as e:
        logger.error(f"Query failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Query failed: {str(e)}"
        )
