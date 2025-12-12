from typing import List, Dict, Any
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.core.config import settings


class VectorService:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(
            model = "text-embedding-3-small",
            openai_api_key=settings.openai_api_key
        )