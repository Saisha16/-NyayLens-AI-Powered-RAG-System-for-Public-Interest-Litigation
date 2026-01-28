"""Tests for authentication module."""

import pytest
from backend.auth import (
    verify_password, get_password_hash, create_access_token,
    authenticate_user, TokenData
)
from jose import jwt
from datetime import datetime, timedelta
from backend.config import config

class TestAuthentication:
    """Authentication tests."""
    
    def test_password_hashing(self):
        """Test password hashing."""
        password = "test_password_123"
        hashed = get_password_hash(password)
        
        assert hashed != password
        assert len(hashed) > 0
    
    def test_password_verification_valid(self):
        """Test valid password verification."""
        password = "test_password_123"
        hashed = get_password_hash(password)
        
        assert verify_password(password, hashed) is True
    
    def test_password_verification_invalid(self):
        """Test invalid password verification."""
        password = "test_password_123"
        wrong_password = "wrong_password"
        hashed = get_password_hash(password)
        
        assert verify_password(wrong_password, hashed) is False
    
    def test_create_access_token(self):
        """Test JWT token creation."""
        username = "testuser"
        user_id = "user_123"
        
        token = create_access_token(username, user_id)
        
        assert isinstance(token, str)
        assert len(token) > 0
    
    def test_token_payload(self):
        """Test JWT token payload contents."""
        username = "testuser"
        user_id = "user_123"
        
        token = create_access_token(username, user_id)
        
        # Decode without verification to check payload
        payload = jwt.decode(
            token,
            config.JWT_SECRET,
            algorithms=[config.JWT_ALGORITHM]
        )
        
        assert payload["username"] == username
        assert payload["user_id"] == user_id
        assert "exp" in payload
    
    def test_token_expiry(self):
        """Test token expiry."""
        username = "testuser"
        user_id = "user_123"
        expires_delta = timedelta(seconds=1)
        
        token = create_access_token(
            username,
            user_id,
            expires_delta=expires_delta
        )
        
        payload = jwt.decode(
            token,
            config.JWT_SECRET,
            algorithms=[config.JWT_ALGORITHM]
        )
        
        assert "exp" in payload
        assert payload["exp"] > datetime.utcnow().timestamp()
    
    def test_authenticate_user_valid(self):
        """Test user authentication with valid credentials."""
        user = authenticate_user("demo", "demo123")
        
        assert user is not None
        assert user.username == "demo"
        assert user.user_id == "user_123"
    
    def test_authenticate_user_invalid_username(self):
        """Test user authentication with invalid username."""
        user = authenticate_user("nonexistent", "password")
        
        assert user is None
    
    def test_authenticate_user_invalid_password(self):
        """Test user authentication with invalid password."""
        user = authenticate_user("demo", "wrong_password")
        
        assert user is None
    
    def test_token_data_model(self):
        """Test TokenData pydantic model."""
        token_data = TokenData(
            username="testuser",
            user_id="user_123"
        )
        
        assert token_data.username == "testuser"
        assert token_data.user_id == "user_123"
