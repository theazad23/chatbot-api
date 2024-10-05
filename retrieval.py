from langchain.docstore.document import Document
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from config import EMBEDDING_MODEL_NAME, VECTORSTORE_DIR
import os

# Ensure the vector store directory exists
if not os.path.exists(VECTORSTORE_DIR):
    os.makedirs(VECTORSTORE_DIR)

# Prepare documents
documents = [
    Document(page_content="""
    Python is a high-level, interpreted programming language known for its readability and versatility.
    It's widely used in web development, data analysis, artificial intelligence, and more.
    """),
    Document(page_content="""
    The capital of France is Paris, known for its rich history, art, fashion, and culture.
    Landmarks include the Eiffel Tower, Louvre Museum, and Notre-Dame Cathedral.
    """),
    Document(page_content="""
    The Theory of Relativity, developed by Albert Einstein, revolutionized theoretical physics.
    It introduced concepts about the relationship between space and time.
    """),
    # Add more documents as needed
]

# Initialize the embedding model
embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)

# Create or load the vector store
if os.path.exists(VECTORSTORE_DIR):
    vectorstore = Chroma(
        persist_directory=VECTORSTORE_DIR,
        embedding_function=embeddings
    )
else:
    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding_function=embeddings,
        persist_directory=VECTORSTORE_DIR
    )

# Create the retriever
retriever = vectorstore.as_retriever()
