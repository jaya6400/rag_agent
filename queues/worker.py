from dotenv import load_dotenv
import google.generativeai as genai
import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import Qdrant

load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Vector Embeddings - using HuggingFace (local, no quota limits)
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-MiniLM-L3-v2",
    model_kwargs={'device': 'cpu'}
)

vector_db = Qdrant.from_existing_collection(
    url="http://localhost:6333",
    collection_name="learning_rag",
    embedding=embedding_model,
)


async def process_query(query: str):
    print("Searching Chunks", query)
    search_results = vector_db.similarity_search(query=query)

    context = "\n\n\n".join([
        f"Page Content: {result.page_content}\nPage Number: {result.metadata['page_label']}\nFile Location: {result.metadata['source']}" 
        for result in search_results
    ])

    SYSTEM_PROMPT = f"""
    You are a helpfull AI Assistant who answeres user query based on the available context retrieved from a PDF file along with page_contents and page number.

    You should only ans the user based on the following context and navigate the user to open the right page number to know more.

    Context:
    {context}
    """

    # Initialize Gemini model
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Create the full prompt (Gemini doesn't have separate system/user roles like OpenAI)
    full_prompt = f"{SYSTEM_PROMPT}\n\nUser Query: {query}"
    
    # Generate response
    response = model.generate_content(full_prompt)

    print(f"🤖: {response.text}")
    return response.text