import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load .env file automatically
load_dotenv()

class Settings(BaseSettings):
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    HF_TOKEN: str = os.getenv("HF_TOKEN", "")
    
    VECTOR_DIR: str = os.getenv("VECTOR_DIR", "data/chroma")
    FEEDS_FILE: str = os.getenv("FEEDS_FILE", "data/feeds_finance.yaml")
    DOMAIN_POLICY: str = os.getenv("DOMAIN_POLICY", "data/domain_policies.json")
    
    MODEL_EMBED: str = os.getenv("MODEL_EMBED", "sentence-transformers/all-MiniLM-L6-v2")
    MODEL_NLI: str = os.getenv("MODEL_NLI", "facebook/bart-large-mnli")
    MODEL_RERANK: str = os.getenv("MODEL_RERANK", "cross-encoder/ms-marco-MiniLM-L-6-v2")
    
    CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", 500))
    CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", 50))
    TOP_K: int = int(os.getenv("TOP_K", 5))

SETTINGS = Settings()
