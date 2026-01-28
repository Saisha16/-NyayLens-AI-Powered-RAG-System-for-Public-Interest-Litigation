"""Structured logging configuration."""

import logging
import json
from datetime import datetime
from pythonjsonlogger import jsonlogger

def setup_logging(log_level=logging.INFO):
    """Configure structured JSON logging."""
    
    logger = logging.getLogger("nyaylens")
    logger.setLevel(log_level)
    
    # File handler with JSON format
    file_handler = logging.FileHandler("logs/nyaylens.log")
    file_handler.setLevel(log_level)
    
    # JSON formatter
    formatter = jsonlogger.JsonFormatter(
        '%(timestamp)s %(level)s %(name)s %(message)s %(exc_info)s'
    )
    file_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    
    # Console handler (pretty format)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    return logger

logger = setup_logging()
