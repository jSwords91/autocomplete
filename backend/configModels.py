from pydantic import BaseModel
from typing import List

class Config(BaseModel):
    """Configuration for the FastAPI app metadata."""
    TITLE: str = "Autocomplete API"
    DESCRIPTION: str = "An API for showing autocomplete suggestions for a given text."
    VERSION: str = "1.0.0"

class ModelName(BaseModel):
    """Model for this app."""
    name: str  = "distilbert/distilgpt2"

class Settings(BaseModel):
    """Settings for the application."""
    # CORS settings
    ALLOWED_ORIGINS: List[str] = ["*"]
    ALLOW_CREDENTIALS: bool = True
    ALLOWED_METHODS: List[str] = ["*"]
    ALLOWED_HEADERS: List[str] = ["*"]

    # Application settings
    FRONTEND_DIR: str = "frontend"

    # Min words needed to make a prediction -- more words, better predictions
    MIN_WORDS: int = 5