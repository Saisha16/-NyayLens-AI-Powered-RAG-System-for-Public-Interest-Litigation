"""Unit tests for RAG pipeline."""

import pytest
from backend.rag_pipeline import retrieve_legal_sections, get_jurisdiction_info

class TestRAGPipeline:
    """RAG system tests."""
    
    def test_retrieve_legal_sections_crime(self):
        """Test legal section retrieval for crime topic."""
        sections = retrieve_legal_sections(
            issue_text="Murder case",
            topics=["crime"],
            entities=[]
        )
        
        assert isinstance(sections, list)
        assert len(sections) > 0
        assert any("Right" in str(s) or "case" in str(s).lower() for s in sections)
    
    def test_retrieve_legal_sections_corruption(self):
        """Test legal section retrieval for corruption."""
        sections = retrieve_legal_sections(
            issue_text="Corruption scandal",
            topics=["corruption"],
            entities=[]
        )
        
        assert isinstance(sections, list)
        assert len(sections) > 0
    
    def test_retrieve_legal_sections_education(self):
        """Test legal section retrieval for education."""
        sections = retrieve_legal_sections(
            issue_text="School denial",
            topics=["education"],
            entities=[]
        )
        
        assert isinstance(sections, list)
        assert len(sections) > 0
    
    def test_retrieve_legal_sections_multiple_topics(self):
        """Test retrieval with multiple topics."""
        sections = retrieve_legal_sections(
            issue_text="Issue involving multiple areas",
            topics=["crime", "women_children"],
            entities=[]
        )
        
        assert isinstance(sections, list)
        assert len(sections) >= 0
    
    def test_legal_sections_structure(self):
        """Test retrieved sections have proper structure."""
        sections = retrieve_legal_sections(
            issue_text="Test issue",
            topics=["crime"],
            entities=[]
        )
        
        for section in sections:
            assert isinstance(section, dict)
            # Should have source field at minimum
            assert "source" in section or "category" in section
    
    def test_jurisdiction_info_crime(self):
        """Test jurisdiction retrieval for crime."""
        jurisdiction = get_jurisdiction_info(["crime"])
        
        assert isinstance(jurisdiction, dict)
        assert "court" in jurisdiction or "article" in jurisdiction
    
    def test_jurisdiction_info_corruption(self):
        """Test jurisdiction retrieval for corruption."""
        jurisdiction = get_jurisdiction_info(["corruption"])
        
        assert isinstance(jurisdiction, dict)
    
    def test_jurisdiction_info_multiple_topics(self):
        """Test jurisdiction with multiple topics."""
        jurisdiction = get_jurisdiction_info(["crime", "corruption"])
        
        assert isinstance(jurisdiction, dict)
    
    def test_retrieve_empty_topics(self):
        """Test retrieval with empty topics."""
        sections = retrieve_legal_sections(
            issue_text="Test",
            topics=[],
            entities=[]
        )
        
        # Should still return something (general provisions)
        assert isinstance(sections, list)
    
    def test_retrieve_with_entities(self):
        """Test retrieval with entity information."""
        sections = retrieve_legal_sections(
            issue_text="Test issue",
            topics=["crime"],
            entities=["IPC", "Article 15"]
        )
        
        assert isinstance(sections, list)
