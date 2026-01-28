"""Pytest configuration and fixtures."""

import pytest
import json
from pathlib import Path

@pytest.fixture
def sample_news_article():
    """Sample news article for testing."""
    return {
        "id": "test_001",
        "title": "Police Officer Arrested for Sexual Harassment of Minor",
        "text": """A police constable was arrested after a boy made allegations of sexual harassment 
        in Karnataka's Bengaluru. The constable is posted with the police station in RT Nagar 
        neighbourhood. The boy alleged sexual harassment during a patrol duty incident. 
        Investigation is ongoing.""",
        "summary": "Police officer arrested for sexual harassment allegations.",
        "topics": ["crime", "women_children"],
        "source": "https://feeds.feedburner.com/ndtvnews-top-stories",
        "url": "https://example.com/news/123",
        "published": "Sat, 24 Jan 2026 18:58:58 +0530"
    }

@pytest.fixture
def sample_articles():
    """Multiple sample articles."""
    return [
        {
            "title": "Corruption Scandal in Municipal Corp",
            "text": "Municipal official caught in bribery scandal worth 50 lakhs...",
            "topics": ["corruption"],
        },
        {
            "title": "School Lunch Program Denied to Students",
            "text": "Government school stopped providing midday meals to 500 children...",
            "topics": ["education"],
        },
        {
            "title": "River Pollution Crisis",
            "text": "Industrial waste dumping polluting drinking water source...",
            "topics": ["environment", "health"],
        },
    ]

@pytest.fixture
def sample_entity_dict():
    """Sample extracted entities."""
    return {
        "persons": ["Yamuna Naik"],
        "organizations": ["Karnataka Police", "RT Nagar Police Station"],
        "locations": ["Bengaluru", "Karnataka"],
        "laws": ["IPC Section 354", "Indian Constitution Article 15"]
    }

@pytest.fixture
def test_data_dir(tmp_path):
    """Create temporary test data directory."""
    data_dir = tmp_path / "data" / "news"
    data_dir.mkdir(parents=True)
    
    # Create sample news file
    news_file = data_dir / "latest_news.json"
    news_file.write_text(json.dumps([
        {
            "id": "1",
            "title": "Test Article 1",
            "text": "Sample crime news",
            "topics": ["crime"],
            "summary": "Crime summary",
            "source": "test",
            "url": "http://test.com/1",
            "published": "2026-01-24"
        }
    ]))
    
    return tmp_path
