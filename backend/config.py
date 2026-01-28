"""Configuration management."""

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration from environment."""
    
    # API
    API_TITLE = "NyayLens"
    API_VERSION = "1.0.0"
    API_DESCRIPTION = "AI-Powered Public Interest Litigation Generator"
    
    # Database
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/nyaylens.db")
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    # Authentication
    JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret-key-change-in-production")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_EXPIRY_HOURS = int(os.getenv("JWT_EXPIRY_HOURS", "24"))
    
    # API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    SENTRY_DSN = os.getenv("SENTRY_DSN", "")
    
    # Features
    ENABLE_LLM_CLASSIFICATION = os.getenv("ENABLE_LLM_CLASSIFICATION", "false").lower() == "true"
    ENABLE_WEBSOCKETS = os.getenv("ENABLE_WEBSOCKETS", "true").lower() == "true"
    ENABLE_CACHING = os.getenv("ENABLE_CACHING", "true").lower() == "true"
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # News Ingestion
    RSS_FEEDS_ENABLED = os.getenv("RSS_FEEDS_ENABLED", "true").lower() == "true"
    MAX_ARTICLES_PER_FEED = int(os.getenv("MAX_ARTICLES_PER_FEED", "15"))
    DEFAULT_DAYS_BACK = int(os.getenv("DEFAULT_DAYS_BACK", "7"))
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS = int(os.getenv("RATE_LIMIT_REQUESTS", "100"))
    RATE_LIMIT_WINDOW = int(os.getenv("RATE_LIMIT_WINDOW", "60"))  # seconds
    
    # CORS
    ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")
    
    @classmethod
    def is_production(cls):
        """Check if running in production."""
        return os.getenv("ENV", "development") == "production"
    
    @classmethod
    def validate(cls):
        """Validate critical configuration."""
        if cls.is_production():
            if cls.JWT_SECRET == "dev-secret-key-change-in-production":
                raise ValueError("❌ JWT_SECRET not set for production!")
            if not cls.SENTRY_DSN:
                raise ValueError("⚠️  SENTRY_DSN recommended for production error tracking")

config = Config()
