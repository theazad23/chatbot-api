from langchain.prompts import PromptTemplate

custom_prompt_template = """

Use the following context to answer the question.  

Context:
{context}

Question:
{question}

If you don't have the answer in your context, let the user know and attempt to answer the question using information outside the context.
Answer in a clear and concise manner.  
"""

PROMPT = PromptTemplate(
    template=custom_prompt_template, input_variables=["context", "question"]
)