# RAG Agent - Queue-Based PDF Question Answering System

A Retrieval-Augmented Generation (RAG) system that enables intelligent question-answering from PDF documents using a queue-based architecture. Built with FastAPI, Gemini AI, and Qdrant vector database.

## 🚀 Features

- **Queue-Based Architecture**: Async processing for scalable document queries
- **PDF Intelligence**: Extract and query information from PDF documents with page references
- **Vector Search**: Fast semantic search using Qdrant and HuggingFace embeddings
- **AI-Powered Responses**: Context-aware answers using Google Gemini 1.5 Flash
- **REST API**: FastAPI backend for easy integration

## 🛠️ Tech Stack

- **LLM**: Google Gemini 1.5 Flash
- **Embeddings**: HuggingFace Sentence Transformers (local, no API limits)
- **Vector Database**: Qdrant
- **Cache/Queue**: Valkey (Redis alternative)
- **API Framework**: FastAPI
- **Language**: Python 3.13+

## 📋 Prerequisites

- Docker and Docker Compose
- Python 3.13+
- Google Gemini API Key ([Get one here](https://ai.google.dev/))

## 🔧 Installation & Setup

### 1. Clone the Repository

```bash
git clone <repo-url>
cd rag_agent
```

### 2. Create Virtual Environment

```bash
python -m venv .venv

# On Windows
.venv\Scripts\activate

# On Linux/Mac
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_gemini_api_key_here
```

### 5. Start Docker Services

Start Qdrant (vector database) and Valkey (cache):

```bash
docker-compose up -d
```

Verify services are running:

```bash
docker-compose ps
```

You should see:
- Qdrant running on `http://localhost:6333`
- Valkey running on `localhost:6379`

### 6. Ingest Your PDF Documents

Place your PDF file in the project directory and update the path in `ingest.py`:

```python
pdf_path = "your_document.pdf"  # Update this line
```

Run the ingestion script:

```bash
python ingest.py
```

This will:
- Load and chunk your PDF
- Generate embeddings using HuggingFace models
- Store vectors in Qdrant collection `learning_rag`

### 7. Start the Application

```bash
python main.py
```

The FastAPI server will start on `http://localhost:8000`

## 📖 Usage

### API Endpoints

Check the interactive API documentation:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Start Redis queue worker

```
cd queues
rq worker
```

### Example Query

```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the main topic of the document?"}'
```

The system will:
1. Search for relevant document chunks using vector similarity
2. Retrieve context with page numbers and source information
3. Generate an AI-powered response using Gemini
4. Return the answer with page references for further reading

## 🏗️ Project Structure

```
rag_agent/
├── main.py                 # FastAPI application entry point
├── server.py               # API routes and endpoints
├── ingest.py               # PDF ingestion and vector storage
├── queues/
│   └── worker.py           # Queue worker for RAG processing
├── docker-compose.yml      # Docker services configuration
├── .env                    # Environment variables (create this)
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## 🐳 Docker Services

### Qdrant (Vector Database)
- **Ports**: 6333 (HTTP), 6334 (gRPC)
- **Dashboard**: `http://localhost:6333/dashboard`
- **Data**: Persisted in `./qdrant_storage`

### Valkey (Cache/Queue)
- **Port**: 6379
- **Use**: Redis-compatible cache and queue system

### Managing Services

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# Restart services
docker-compose restart
```

## 🔍 Monitoring

### Check Qdrant Collection

```bash
curl http://localhost:6333/collections/learning_rag
```

### View Qdrant Dashboard

Navigate to: `http://localhost:6333/dashboard`

## 🛠️ Troubleshooting

### Connection Refused Error
- Ensure Docker services are running: `docker-compose ps`
- Check if ports 6333 and 6379 are available

### Quota Exceeded (Google API)
- The project uses HuggingFace embeddings (local, no quota)
- Only Gemini text generation uses API calls
- Check your usage: https://ai.dev/usage

### Collection Not Found
- Run `python ingest.py` to create the collection
- Verify collection exists via Qdrant dashboard

## 📝 Dependencies

Key dependencies (see `requirements.txt` for full list):

```
fastapi
google-generativeai
langchain-huggingface
langchain-qdrant
langchain-community
sentence-transformers
qdrant-client
redis
python-dotenv
```

## 🤝 Contributing

Feel free to open issues or submit pull requests!


## 🙏 Acknowledgments

- Google Gemini API for LLM capabilities
- Qdrant for vector database
- HuggingFace for embedding models
- LangChain for RAG framework