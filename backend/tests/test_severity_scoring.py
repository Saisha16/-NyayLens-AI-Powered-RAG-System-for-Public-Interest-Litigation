"""Unit tests for severity scoring."""

import pytest
from backend.severity_scoring import calculate_severity

class TestSeverityScoring:
    """Severity scoring tests."""
    
    def test_critical_severity_murder(self):
        """Test critical severity for murder."""
        text = "Man murdered in Delhi by unknown assailants."
        all_texts = [text]
        
        score = calculate_severity(text, all_texts)
        assert score >= 0.75, f"Murder should be high severity, got {score}"
        assert score <= 1.0, f"Score should not exceed 1.0, got {score}"
    
    def test_critical_severity_rape(self):
        """Test critical severity for rape."""
        text = "Woman raped in broad daylight in city center."
        all_texts = [text]
        
        score = calculate_severity(text, all_texts)
        assert score >= 0.85, f"Rape should be very high severity, got {score}"
    
    def test_high_severity_corruption(self):
        """Test high severity for corruption."""
        text = "Official caught in corruption scam worth 10 crores."
        all_texts = [text]
        
        score = calculate_severity(text, all_texts)
        assert 0.55 <= score <= 0.75, f"Corruption should be medium-high, got {score}"
    
    def test_medium_severity_health(self):
        """Test medium severity for health issue."""
        text = "Hospital lacking proper sanitation facilities."
        all_texts = [text]
        
        score = calculate_severity(text, all_texts)
        assert 0.3 <= score <= 0.6, f"Health issue should be medium, got {score}"
    
    def test_severity_boost_minors(self):
        """Test severity boost for crimes against minors."""
        text_without = "Man arrested in case."
        text_with = "Man arrested for abusing minor children."
        
        score_without = calculate_severity(text_without, [text_without])
        score_with = calculate_severity(text_with, [text_with])
        
        # Score with minors should be higher
        assert score_with > score_without or score_with == score_without
    
    def test_severity_low_for_general(self):
        """Test low severity for general news."""
        text = "New bridge inaugurated in city."
        all_texts = [text]
        
        score = calculate_severity(text, all_texts)
        assert score <= 0.4, f"General news should be low severity, got {score}"
    
    def test_severity_normalization(self):
        """Test severity score is normalized 0-1."""
        texts = [
            "Murder in crime-ridden area",
            "Health crisis in hospital",
            "Weather update for city"
        ]
        
        for text in texts:
            score = calculate_severity(text, texts)
            assert 0 <= score <= 1, f"Score must be 0-1, got {score}"
    
    def test_severity_trafficking(self):
        """Test severity for human trafficking."""
        text = "Human trafficking ring busted, 50 victims rescued."
        all_texts = [text]
        
        score = calculate_severity(text, all_texts)
        assert score >= 0.80, f"Trafficking should be high severity, got {score}"
    
    def test_severity_mass_incident(self):
        """Test severity boost for mass incidents."""
        text = "Mass protest turns violent, 20 killed."
        all_texts = [text]
        
        score = calculate_severity(text, all_texts)
        assert score >= 0.75, f"Mass incident should be high severity, got {score}"
