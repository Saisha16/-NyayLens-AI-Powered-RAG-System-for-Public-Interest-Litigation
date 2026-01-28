"""JWT Authentication for NyayLens API."""

from datetime import datetime, timedelta
from typing import Optional
from pydantic import BaseModel
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from backend.config import config

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

class TokenData(BaseModel):
    """JWT token payload."""
    username: str
    user_id: str
    exp: Optional[datetime] = None

class User(BaseModel):
    """User model."""
    user_id: str
    username: str
    email: str
    is_active: bool = True

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash password."""
    return pwd_context.hash(password)

def create_access_token(
    username: str,
    user_id: str,
    expires_delta: Optional[timedelta] = None
) -> str:
    """Create JWT access token."""
    if expires_delta is None:
        expires_delta = timedelta(hours=config.JWT_EXPIRY_HOURS)
    
    expire = datetime.utcnow() + expires_delta
    to_encode = {
        "username": username,
        "user_id": user_id,
        "exp": expire
    }
    
    encoded_jwt = jwt.encode(
        to_encode,
        config.JWT_SECRET,
        algorithm=config.JWT_ALGORITHM
    )
    return encoded_jwt

async def verify_token(token: str) -> TokenData:
    """Verify JWT token."""
    
    try:
        payload = jwt.decode(
            token,
            config.JWT_SECRET,
            algorithms=[config.JWT_ALGORITHM]
        )
        username: str = payload.get("username")
        user_id: str = payload.get("user_id")
        
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )
        
        return TokenData(username=username, user_id=user_id)
        
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token or token expired"
        )

# Example user database (replace with real DB in production)
# Password: demo123 (pre-hashed for test purposes)
DEMO_USERS = {
    "demo": {
        "user_id": "user_123",
        "username": "demo",
        "password_hash": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5ztP6yiH.eKhG",  # demo123
        "email": "demo@nyaylens.dev"
    }
}

def authenticate_user(username: str, password: str) -> Optional[User]:
    """Authenticate user with username/password."""
    user_data = DEMO_USERS.get(username)
    
    if not user_data:
        return None
    
    if not verify_password(password, user_data["password_hash"]):
        return None
    
    return User(
        user_id=user_data["user_id"],
        username=user_data["username"],
        email=user_data["email"]
    )
