"""Unit tests for validators."""

import pytest
from backend.validators import (
    NewsArticleInput, PILGenerationInput, RefreshNewsInput,
    sanitize_text, validate_email
)

class TestValidators:
    """Input validation tests."""
    
    def test_valid_news_article_input(self):
        """Test valid news article input."""
        data = {
            "url": "https://example.com/news/123",
            "title": "Test Article"
        }
        article = NewsArticleInput(**data)
        assert article.url == data["url"]
        assert article.title == data["title"]
    
    def test_invalid_url_format(self):
        """Test invalid URL format rejection."""
        with pytest.raises(ValueError):
            NewsArticleInput(
                url="not-a-valid-url",
                title="Test"
            )
    
    def test_invalid_url_scheme(self):
        """Test non-HTTP URL rejection."""
        with pytest.raises(ValueError):
            NewsArticleInput(
                url="ftp://example.com/file",
                title="Test"
            )
    
    def test_url_too_long(self):
        """Test URL length validation."""
        long_url = "https://example.com/" + "a" * 3000
        with pytest.raises(ValueError):
            NewsArticleInput(
                url=long_url,
                title="Test"
            )
    
    def test_title_sanitization(self):
        """Test title sanitization."""
        data = {
            "url": "https://example.com/news",
            "title": 'Test<script>alert("xss")</script>Article'
        }
        article = NewsArticleInput(**data)
        # Should remove script tags
        assert "<script>" not in article.title
    
    def test_title_too_long(self):
        """Test title length validation."""
        with pytest.raises(ValueError):
            NewsArticleInput(
                url="https://example.com",
                title="a" * 600
            )
    
    def test_pil_generation_input_valid(self):
        """Test valid PIL generation input."""
        data = {
            "article_index": 0,
            "topic": "crime"
        }
        pil_input = PILGenerationInput(**data)
        assert pil_input.article_index == 0
        assert pil_input.topic == "crime"
    
    def test_pil_generation_invalid_topic(self):
        """Test invalid topic rejection."""
        with pytest.raises(ValueError):
            PILGenerationInput(
                article_index=0,
                topic="invalid_topic"
            )
    
    def test_pil_generation_negative_index(self):
        """Test negative index rejection."""
        with pytest.raises(ValueError):
            PILGenerationInput(
                article_index=-1,
                topic="crime"
            )
    
    def test_refresh_news_valid(self):
        """Test valid refresh news input."""
        data = {
            "days_back": 7,
            "max_per_feed": 15
        }
        refresh = RefreshNewsInput(**data)
        assert refresh.days_back == 7
    
    def test_refresh_news_days_out_of_range(self):
        """Test days_back out of range."""
        with pytest.raises(ValueError):
            RefreshNewsInput(
                days_back=100,  # Max is 90
                max_per_feed=15
            )
    
    def test_sanitize_text_basic(self):
        """Test text sanitization."""
        text = "Hello World"
        sanitized = sanitize_text(text)
        assert sanitized == "Hello World"
    
    def test_sanitize_text_long(self):
        """Test text truncation."""
        long_text = "a" * 20000
        sanitized = sanitize_text(long_text, max_length=10000)
        assert len(sanitized) <= 10000
    
    def test_sanitize_text_control_chars(self):
        """Test control character removal."""
        text = "Hello\x00World\x01Test"
        sanitized = sanitize_text(text)
        # Should remove null characters
        assert "\x00" not in sanitized
    
    def test_validate_email_valid(self):
        """Test valid email validation."""
        assert validate_email("test@example.com") is True
        assert validate_email("user.name+tag@domain.co.uk") is True
    
    def test_validate_email_invalid(self):
        """Test invalid email validation."""
        assert validate_email("not-an-email") is False
        assert validate_email("@example.com") is False
        assert validate_email("user@") is False
