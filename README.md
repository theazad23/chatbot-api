Setting Up the Project

python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

Install Dependencies:

pip install -r requirements.txt

Run the Application:

uvicorn app:app --reload
