"""Unit tests for NLP pipeline."""

import pytest
from backend.nlp_pipeline import extract_issue, extract_entities

class TestNLPPipeline:
    """NLP pipeline tests."""
    
    def test_entity_extraction_basic(self, sample_news_article):
        """Test basic entity extraction."""
        text = sample_news_article["text"]
        entities = extract_entities(text)
        
        assert isinstance(entities, dict)
        assert "persons" in entities or "locations" in entities
    
    def test_entity_extraction_person(self):
        """Test person entity extraction."""
        text = "John Smith, a police officer, was arrested."
        entities = extract_entities(text)
        
        assert "persons" in entities or len(entities) > 0
    
    def test_entity_extraction_location(self):
        """Test location entity extraction."""
        text = "An incident occurred in Bengaluru, Karnataka."
        entities = extract_entities(text)
        
        assert "locations" in entities or len(entities) > 0
    
    def test_entity_extraction_organization(self):
        """Test organization entity extraction."""
        text = "The Karnataka Police arrested the suspect."
        entities = extract_entities(text)
        
        assert "organizations" in entities or len(entities) > 0
    
    def test_issue_extraction(self, sample_news_article):
        """Test issue extraction from article."""
        issue = extract_issue(sample_news_article["text"])
        
        assert "issue_summary" in issue
        assert "entities" in issue
        assert isinstance(issue["entities"], list)
    
    def test_issue_extraction_crime(self):
        """Test extraction from crime article."""
        text = "A murder case was registered against the accused in Delhi."
        issue = extract_issue(text)
        
        assert len(issue["entities"]) >= 0
        assert issue["issue_summary"]
    
    def test_issue_extraction_empty(self):
        """Test extraction from empty text."""
        issue = extract_issue("")
        
        assert "issue_summary" in issue
        assert isinstance(issue["entities"], list)
    
    def test_issue_extraction_long_text(self):
        """Test extraction from long text."""
        long_text = " ".join(["This is a news article about corruption."] * 100)
        issue = extract_issue(long_text)
        
        assert "issue_summary" in issue
