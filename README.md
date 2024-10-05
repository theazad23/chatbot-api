# Chatbot API Project

This project is designed to serve as an API that interacts with a locally hosted LLM (Large Language Model) using LangChain, FastAPI, and a retrieval-based approach for enhanced question answering.

## Project Setup

### 1. Clone the Repository

Begin by cloning the repository to your local environment:

```bash
git clone https://github.com/your-username/chatbot-api.git
cd chatbot-api
```

### 2. Create a Virtual Environment

Create and activate a Python virtual environment to isolate your project dependencies.

On Linux/MacOS:

```bash
python -m venv venv
source venv/bin/activate
```
On Windows:

```bash

python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

Install the required Python packages using pip:

```bash
pip install -r requirements.txt
```

### 4. Set Up Your .env File

To securely store sensitive configuration details, such as the API key and the LLM server URL, create a .env file in the project root with the following content:

```makefile

# .env file

API_KEY=dummy-key  # For LM Studio, no real key is needed
BASE_URL=http://192.168.10.248:1234/v1  # Replace with your actual LLM server URL
MODEL_NAME=lmstudio-community/Llama-3.2-3B-Instruct-GGUF/Llama-3.2-3B-Instruct-Q4_K_M.gguf
```
    Note: Update BASE_URL to point to the correct address for your LLM Studio server.

### 5. Running the Application

Once the virtual environment is activated and dependencies are installed, start the FastAPI server:

```bash

uvicorn app:app --reload
```
The API will be running on http://127.0.0.1:8000. You can now interact with the API using a client like curl or Postman, or by creating a UI that connects to this API.

### 6. API Endpoints

    POST /chat: Sends a query to the chatbot and receives a response.

Example usage:

```bash

curl -X POST "http://127.0.0.1:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{"query": "What is Python?"}'
```
    POST /llm_test: Sends a prompt directly to the LLM for testing.

Example usage:

```bash

curl -X POST "http://127.0.0.1:8000/llm_test" \
     -H "Content-Type: application/json" \
     -d '{"query": "Say something about AI."}'
```
    POST /retriever_test: Retrieves the most relevant documents related to the provided query.

Example usage:

```bash

curl -X POST "http://127.0.0.1:8000/retriever_test" \
     -H "Content-Type: application/json" \
     -d '{"query": "Tell me about Python."}'
```

### 7. Project Structure

The project is organized into modules to make it easy to experiment and extend. Here's the structure:

graphql

chatbot_api/
│
├── app.py                 # Main FastAPI app file
├── llm_client.py          # Custom LLM client interacting with the local LLM server
├── retrieval.py           # Handles document retrieval and vector store setup
├── routes.py              # API endpoints and logic for FastAPI
├── requirements.txt       # Project dependencies
├── .env                   # Environment variables (not included in version control)
└── .gitignore             # Git ignore file

### 8. What to Add to .gitignore

Ensure your .gitignore includes the following files and directories to avoid committing unnecessary or sensitive files:

```bash

# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
build/
dist/
.eggs/
*.egg-info/
*.egg

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.coverage
.cache

# Virtual environments
.venv/
env/
ENV/
venv.bak/

# Environments
.env
.venv
env/
venv/

# Jupyter Notebook
.ipynb_checkpoints

# Pyre type checker
.pyre/

# PyCharm
.idea/
```
### 9. Additional Notes

    Make sure to update your .env file to match your environment.
    If using a different LLM model or server configuration, adjust the .env file accordingly.

This project is designed to be modular and easily extendable. You can experiment with different retrieval models, LLM configurations, and user interfaces.
