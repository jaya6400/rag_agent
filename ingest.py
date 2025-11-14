from dotenv import load_dotenv
import os
import google.generativeai as genai
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import Qdrant
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

# Configure Gemini (still needed for text generation)
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Use local Hugging Face embeddings instead
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-MiniLM-L3-v2"  # Only ~60MB
)

pdf_path = "Unit-4.pdf"
loader = PyPDFLoader(pdf_path)
documents = loader.load()

print(f"📄 Loaded {len(documents)} pages from PDF")

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len,
)
chunks = text_splitter.split_documents(documents)

print(f"✂️  Split into {len(chunks)} chunks")

print("🔄 Creating Qdrant collection and adding documents...")
vector_db = Qdrant.from_documents(
    documents=chunks,
    embedding=embedding_model,
    url="http://localhost:6333",
    collection_name="learning_rag",
)

print("✅ Successfully created 'learning_rag' collection and ingested documents!")
print(f"📊 Total vectors stored: {len(chunks)}")