"""Tests for configuration module."""

import pytest
import os
from backend.config import Config, config

class TestConfiguration:
    """Configuration tests."""
    
    def test_default_config_values(self):
        """Test default configuration values."""
        assert config.API_TITLE == "NyayLens"
        assert config.API_VERSION == "1.0.0"
        assert config.JWT_ALGORITHM == "HS256"
    
    def test_database_url_default(self):
        """Test default database URL."""
        # Should default to SQLite if not set
        assert config.DATABASE_URL is not None
        assert "sqlite" in config.DATABASE_URL.lower() or "postgresql" in config.DATABASE_URL.lower()
    
    def test_rate_limit_values(self):
        """Test rate limit configuration."""
        assert config.RATE_LIMIT_REQUESTS > 0
        assert config.RATE_LIMIT_WINDOW > 0
    
    def test_jwt_expiry_positive(self):
        """Test JWT expiry is positive."""
        assert config.JWT_EXPIRY_HOURS > 0
    
    def test_log_level_valid(self):
        """Test log level is valid."""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        assert config.LOG_LEVEL in valid_levels
    
    def test_max_articles_per_feed(self):
        """Test max articles per feed config."""
        assert config.MAX_ARTICLES_PER_FEED > 0
        assert config.MAX_ARTICLES_PER_FEED <= 100
    
    def test_default_days_back(self):
        """Test default days back for news."""
        assert config.DEFAULT_DAYS_BACK > 0
        assert config.DEFAULT_DAYS_BACK <= 90
    
    def test_allowed_origins_list(self):
        """Test CORS allowed origins."""
        assert isinstance(config.ALLOWED_ORIGINS, list)
        assert len(config.ALLOWED_ORIGINS) > 0
    
    def test_rss_feeds_enabled_flag(self):
        """Test RSS feeds enabled flag."""
        assert isinstance(config.RSS_FEEDS_ENABLED, bool)
    
    def test_config_is_production_method(self):
        """Test is_production detection."""
        result = config.is_production()
        assert isinstance(result, bool)
    
    def test_feature_flags(self):
        """Test feature flag types."""
        assert isinstance(config.ENABLE_LLM_CLASSIFICATION, bool)
        assert isinstance(config.ENABLE_WEBSOCKETS, bool)
        assert isinstance(config.ENABLE_CACHING, bool)
