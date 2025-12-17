
# RAG Backend Service

A production-ready Retrieval-Augmented Generation (RAG) backend service that enables question-answering capabilities over custom document collections.

##  Features

- **Document Ingestion**: Scrape and process web pages or upload text documents
- **Semantic Search**: Find relevant content using vector embeddings
- **Question Answering**: Get accurate answers based on the ingested content
- **RESTful API**: Easy integration with web and mobile applications
- **Production-Ready**: Includes error handling, logging, and rate limiting

## Quick Start

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/rag-backend.git
   cd rag-backend
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Configuration

Create a `.env` file in the project root with your configuration:

```env
# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=False

# Rate Limiting
RATE_LIMIT=10
RATE_PERIOD=60  # in seconds
```

### Running the Server

```bash
uvicorn app.main:app --host $HOST --port $PORT --reload
```

The API will be available at `http://localhost:8000`

## Frontend

The project includes a simple web interface to interact with the RAG backend. The frontend is built with vanilla HTML, CSS, and JavaScript for easy deployment and minimal dependencies.

### Features

- **Simple Interface**: Clean and intuitive UI for interacting with the RAG system
- **Real-time Responses**: Stream responses from the backend
- **Responsive Design**: Works on both desktop and mobile devices
- **Dark/Light Mode**: Toggle between color schemes

### Running the Frontend

1. Make sure the backend server is running (see [Running the Server](#-quick-start) above)
2. Open the frontend in your browser:
   ```bash
   # Using Python's built-in HTTP server
   cd frontend
   python -m http.server 3000
## 📚 API Documentation

Once the server is running, access the interactive API documentation:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Endpoints

- `POST /ingest` - Ingest content from a URL
  ```json
  {
    "url": "https://example.com"
  }
  ```

- `POST /ask` - Ask a question
  ```json
  {
    "question": "What is RAG?"
  }
  ```

- `GET /health` - Health check endpoint

## 🔧 Development

### Project Structure

```
rag-backend/
├── app/
│   ├── __init__.py
│   ├── main.py         # FastAPI application
│   ├── ingest.py       # Web scraping and text processing
│   ├── rag.py          # RAG implementation
│   ├── store.py        # Vector store interface
│   └── middleware.py   # Custom middleware
├── tests/              # Test files
├── .env.example        # Example environment variables
├── requirements.txt    # Project dependencies
└── README.md
```

### Running Tests

```bash
pytest
```

### Code Style

This project uses:
- Black for code formatting
- Flake8 for linting
- Mypy for type checking

Run the following to ensure code quality:

```bash
black .
flake8
mypy .
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



##  Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) for the awesome web framework
- [Sentence Transformers](https://www.sbert.net/) for text embeddings
- [FAISS](https://github.com/facebookresearch/faiss) for efficient similarity search

---

<div align="center">
  Made with ❤️ by chandril
</div>
```
