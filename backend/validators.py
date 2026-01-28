"""Input validation and sanitization."""

from pydantic import BaseModel, Field, validator, HttpUrl
from typing import Optional, List
import re
from urllib.parse import urlparse

class NewsArticleInput(BaseModel):
    """Validate custom news article input."""
    url: str = Field(..., description="Article URL")
    title: Optional[str] = Field(None, description="Custom title (optional)")
    
    @validator('url')
    def validate_url(cls, v):
        """Ensure valid HTTP/HTTPS URL."""
        try:
            result = urlparse(v)
            if not all([result.scheme in ['http', 'https'], result.netloc]):
                raise ValueError("Invalid URL format")
            if len(v) > 2048:
                raise ValueError("URL too long (max 2048 chars)")
            return v
        except Exception as e:
            raise ValueError(f"URL validation failed: {str(e)}")
    
    @validator('title')
    def validate_title(cls, v):
        """Sanitize title."""
        if v is None:
            return v
        if len(v) > 500:
            raise ValueError("Title too long (max 500 chars)")
        # Remove dangerous characters
        v = re.sub(r'[<>"\']', '', v)
        return v

class PILGenerationInput(BaseModel):
    """Validate PIL generation request."""
    article_index: int = Field(..., ge=0, description="News article index")
    topic: Optional[str] = Field(None, description="Filter by topic")
    custom_description: Optional[str] = Field(None, max_length=5000)
    
    @validator('topic')
    def validate_topic(cls, v):
        """Ensure valid topic."""
        valid_topics = [
            "corruption", "crime", "education", "environment", 
            "general", "health", "women_children", "human_trafficking"
        ]
        if v and v not in valid_topics:
            raise ValueError(f"Invalid topic. Allowed: {valid_topics}")
        return v

class RefreshNewsInput(BaseModel):
    """Validate news refresh request."""
    days_back: int = Field(7, ge=1, le=90, description="Days to fetch news from")
    max_per_feed: int = Field(15, ge=1, le=50, description="Max articles per feed")


class CustomPILRequest(BaseModel):
    """Validate custom PIL generation payload."""

    article_summary: str = Field(..., min_length=10, max_length=8000)
    article_text: Optional[str] = Field(None, max_length=12000)
    source: Optional[str] = Field(None, max_length=200)
    topics: Optional[List[str]] = None
    entities: Optional[List[str]] = None
    title: Optional[str] = Field(None, max_length=300)

    @validator("topics", each_item=True)
    def validate_topics(cls, v):
        if not v:
            return v
        # Keep it simple: alphanumerics, spaces, underscores, hyphens
        if len(v) > 50:
            raise ValueError("Topic too long (max 50 chars)")
        if not re.match(r"^[\w\-\s]+$", v):
            raise ValueError("Topic contains invalid characters")
        return v

    @validator("entities", each_item=True)
    def validate_entities(cls, v):
        if not v:
            return v
        if len(v) > 80:
            raise ValueError("Entity too long (max 80 chars)")
        v = re.sub(r'[<>\"]', '', v)
        return v

def sanitize_text(text: str, max_length: int = 10000) -> str:
    """Sanitize text input."""
    if not isinstance(text, str):
        raise ValueError("Text must be string")
    
    if len(text) > max_length:
        text = text[:max_length]
    
    # Remove control characters
    text = ''.join(char for char in text if ord(char) >= 32 or char in '\n\t\r')
    
    return text.strip()

def validate_email(email: str) -> bool:
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None
