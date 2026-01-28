"""Database migration: News storage with PostgreSQL via SQLAlchemy.

Replaces JSON-based storage with proper database for concurrent access.
"""

from sqlalchemy import select, and_
from typing import List, Optional
from datetime import datetime
import json
from pathlib import Path

from backend.db_models import NewsArticle, get_db, init_db
from backend.logger import logger


def save_news_article(article_data: dict) -> NewsArticle:
    """Save or update a news article in the database."""
    db = next(get_db())
    
    try:
        # Check if article already exists (by URL)
        existing = db.query(NewsArticle).filter(
            NewsArticle.url == article_data.get("url")
        ).first()
        
        if existing:
            # Update existing
            for key, value in article_data.items():
                if hasattr(existing, key) and key not in ["id", "created_at"]:
                    setattr(existing, key, value)
            existing.updated_at = datetime.utcnow()
            article = existing
        else:
            # Create new
            article = NewsArticle(
                title=article_data.get("title", ""),
                text=article_data.get("text", ""),
                summary=article_data.get("summary", ""),
                url=article_data.get("url", ""),
                source=article_data.get("source", ""),
                topics=json.dumps(article_data.get("topics", [])),
                published=article_data.get("published", ""),
                severity_score=article_data.get("severity_score", 0.0),
            )
            db.add(article)
        
        db.commit()
        db.refresh(article)
        logger.info(f"Saved news article: {article.title[:50]}")
        return article
    
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to save news article: {e}")
        raise
    finally:
        db.close()


def get_all_news(topic: Optional[str] = None, limit: int = 100) -> List[dict]:
    """Retrieve news articles from database with optional topic filter."""
    db = next(get_db())
    
    try:
        query = db.query(NewsArticle).order_by(NewsArticle.created_at.desc())
        
        if topic:
            # Filter by topic (topics stored as JSON array)
            query = query.filter(NewsArticle.topics.contains(f'"{topic}"'))
        
        articles = query.limit(limit).all()
        
        result = []
        for idx, article in enumerate(articles):
            result.append({
                "index": idx,
                "id": article.id,
                "title": article.title,
                "text": article.text,
                "summary": article.summary,
                "url": article.url,
                "source": article.source,
                "topics": json.loads(article.topics) if article.topics else [],
                "published": article.published,
                "severity_score": article.severity_score,
                "created_at": article.created_at.isoformat() if article.created_at else None,
            })
        
        logger.info(f"Retrieved {len(result)} news articles")
        return result
    
    except Exception as e:
        logger.error(f"Failed to retrieve news: {e}")
        return []
    finally:
        db.close()


def migrate_json_to_db():
    """One-time migration: Load existing JSON news into database."""
    json_path = Path("data/news/latest_news.json")
    
    if not json_path.exists():
        logger.warning("No JSON news file found; skipping migration")
        return
    
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            articles = json.load(f)
        
        logger.info(f"Migrating {len(articles)} articles from JSON to database...")
        
        for article_data in articles:
            try:
                save_news_article(article_data)
            except Exception as e:
                logger.error(f"Failed to migrate article: {e}")
                continue
        
        logger.info("Migration completed successfully")
        
        # Optionally backup JSON file
        backup_path = json_path.with_suffix(".json.backup")
        json_path.rename(backup_path)
        logger.info(f"JSON file backed up to {backup_path}")
    
    except Exception as e:
        logger.error(f"Migration failed: {e}")
        raise


if __name__ == "__main__":
    # Run migration
    init_db()
    migrate_json_to_db()
