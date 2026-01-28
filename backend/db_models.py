"""SQLAlchemy ORM models for NyayLens."""

from sqlalchemy import Column, String, Integer, Float, DateTime, Text, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from backend.config import config

Base = declarative_base()

class NewsArticle(Base):
    """News article model."""
    __tablename__ = "news_articles"
    
    id = Column(String, primary_key=True)
    title = Column(String(500), nullable=False)
    text = Column(Text, nullable=False)
    summary = Column(Text)
    topics = Column(String(500))  # JSON stringified
    source = Column(String(500))
    url = Column(String(2048))
    published = Column(String(100))
    fetched_at = Column(DateTime, default=datetime.utcnow)
    
class GeneratedPIL(Base):
    """Generated PIL document model."""
    __tablename__ = "generated_pils"
    
    id = Column(String, primary_key=True)
    article_id = Column(String, nullable=False)
    pil_content = Column(Text, nullable=False)
    severity_score = Column(Float)
    priority_level = Column(String(20))
    pdf_path = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
    
class User(Base):
    """User model for authentication."""
    __tablename__ = "users"
    
    id = Column(String, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
class APIUsageLog(Base):
    """API usage logging for analytics."""
    __tablename__ = "api_usage_logs"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String)
    endpoint = Column(String(200))
    method = Column(String(20))
    status_code = Column(Integer)
    response_time_ms = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

# Database initialization
def get_engine():
    """Get database engine."""
    return create_engine(
        config.DATABASE_URL,
        echo=config.LOG_LEVEL == "DEBUG"
    )

def get_session_factory():
    """Get session factory."""
    engine = get_engine()
    return sessionmaker(bind=engine)

def init_db():
    """Initialize database tables."""
    engine = get_engine()
    Base.metadata.create_all(bind=engine)

def get_db():
    """Get database session."""
    SessionFactory = get_session_factory()
    db = SessionFactory()
    try:
        yield db
    finally:
        db.close()
