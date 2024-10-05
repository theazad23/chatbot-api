from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'dummy-key')
OPENAI_API_BASE = os.getenv('OPENAI_API_BASE', 'http://192.168.10.248:1234/v1')
MODEL_ID = os.getenv('MODEL_ID', 'lmstudio-community/Llama-3.2-3B-Instruct-GGUF/Llama-3.2-3B-Instruct-Q4_K_M.gguf')
EMBEDDING_MODEL_NAME = os.getenv('EMBEDDING_MODEL_NAME', 'all-MiniLM-L6-v2')
VECTORSTORE_DIR = os.getenv('VECTORSTORE_DIR', './chroma_db')
