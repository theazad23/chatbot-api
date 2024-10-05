from langchain.llms.base import LLM
from typing import Optional, List
from pydantic import BaseModel, PrivateAttr
from openai import OpenAI
from config import OPENAI_API_KEY, OPENAI_API_BASE, MODEL_ID
import os

# Load environment variables for model temperature and max tokens
MODEL_TEMP = float(os.getenv('MODEL_TEMP', 0.7))  # Default to 0.7 if not set
MODEL_MAX_TOKENS = int(os.getenv('MODEL_MAX_TOKENS', 512))  # Default to 512 if not set

# Configure the OpenAI client
client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_API_BASE
)

class OpenAIClientLLM(LLM, BaseModel):
    model_name: str = MODEL_ID
    temperature: float = MODEL_TEMP
    max_tokens: int = MODEL_MAX_TOKENS

    _client: OpenAI = PrivateAttr()

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, **data):
        super().__init__(**data)
        self._client = client

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
