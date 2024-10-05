# routes.py

from fastapi import APIRouter, HTTPException
from llm_client import OpenAIClientLLM
from retrieval import retriever
from models import ChatRequest, ChatResponse
from prompts import PROMPT
from langchain.chains import LLMChain
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
import logging

# Initialize router
router = APIRouter()

# Initialize LLM
llm = OpenAIClientLLM()

# Create an LLM chain with your prompt
llm_chain = LLMChain(llm=llm, prompt=PROMPT)

# Create the stuff documents chain
qa_chain = StuffDocumentsChain(
    llm_chain=llm_chain,
    document_variable_name="context",
)

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    query = request.query
    try:
        # Retrieve relevant documents
        docs = retriever.get_relevant_documents(query)
        # Prepare inputs for the chain
        chain_inputs = {
            "input_documents": docs,
            "question": query,
        }
        # Run the QA chain
        result = qa_chain(chain_inputs)
        answer = result["output_text"]
        return ChatResponse(response=answer)
    except Exception as e:
        logging.error(f"Error during /chat: {e}")
        raise HTTPException(status_code=500, detail="An internal error occurred.")

# ... rest of your routes ...
