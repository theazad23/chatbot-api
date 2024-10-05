# main.py

import logging
logging.basicConfig(level=logging.DEBUG)

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, PrivateAttr
import os

from fastapi.middleware.cors import CORSMiddleware

# Import necessary modules
from langchain.llms.base import LLM
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from typing import Optional, List
from langchain_community.vectorstores import Chroma  # Updated import
from langchain_huggingface.embeddings import HuggingFaceEmbeddings  # Updated import
from langchain.docstore.document import Document
from openai import OpenAI

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your frontend's URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure the OpenAI client
client = OpenAI(
    api_key='dummy-key',  # LM Studio doesn't require a real API key
    base_url='http://192.168.10.248:1234/v1'  # Replace with your LM Studio server's address
)

# Define the custom LLM class
class OpenAIClientLLM(LLM, BaseModel):
    model_name: str
    temperature: float = 0.7
    max_tokens: int = 150

    _client: OpenAI = PrivateAttr()

    class Config:
        arbitrary_types_allowed = True  # Allows non-Pydantic types like OpenAI

    def __init__(self, **data):
        super().__init__(**data)
        self._client = client  # Assign the OpenAI client instance here

    @property
    def _llm_type(self) -> str:
        return "custom_openai_client"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        try:
            chat_completion = self._client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                stop=stop,
            )
            return chat_completion.choices[0].message.content.strip()
        except Exception as e:
            raise e

# Replace 'your-model-id' with your actual model ID
model_id = 'lmstudio-community/Llama-3.2-3B-Instruct-GGUF/Llama-3.2-3B-Instruct-Q4_K_M.gguf'

# Initialize the LLM instance
llm = OpenAIClientLLM(
    model_name=model_id,
    temperature=0.7,
    max_tokens=2048
)

# Prepare documents for the vector store
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
embeddings = HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')

# Remove existing vector store directory if needed
import shutil
import os
if os.path.exists('./chroma_db'):
    shutil.rmtree('./chroma_db')

# Create the vector store
vectorstore = Chroma.from_documents(
    documents=documents,
    embedding=embeddings,
    persist_directory='./chroma_db'
)

# Create the retriever
retriever = vectorstore.as_retriever()

# Define a custom prompt
custom_prompt_template = """Use the following context to answer the question.

Context:
{context}

Question:
{question}

Answer in a clear and concise manner.
"""
PROMPT = PromptTemplate(
    template=custom_prompt_template, input_variables=["context", "question"]
)

# Load the QA chain
qa_chain = load_qa_chain(
    llm=llm,
    chain_type="stuff",
    prompt=PROMPT
)

# Define request and response models
class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    response: str

# Create the chat endpoint
@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    query = request.query
    try:
        # Retrieve relevant documents
        docs = retriever.get_relevant_documents(query)
        # Run the QA chain
        answer = qa_chain.run(input_documents=docs, question=query)
        return ChatResponse(response=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# LLM test endpoint
@app.post("/llm_test", response_model=ChatResponse)
async def llm_test(request: ChatRequest):
    prompt = request.query
    try:
        answer = llm(prompt)
        return ChatResponse(response=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Retriever test endpoint
@app.post("/retriever_test", response_model=ChatResponse)
async def retriever_test(request: ChatRequest):
    query = request.query
    try:
        docs = retriever.get_relevant_documents(query)
        content = "\n\n".join([doc.page_content for doc in docs])
        return ChatResponse(response=content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
