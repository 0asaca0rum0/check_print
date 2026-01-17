"""
Data models for the Check Printer application.
"""
from PyQt6.QtCore import QDate
from dataclasses import dataclass
from typing import Optional


@dataclass
class CheckData:
    """Data structure for check information."""
    amount: float
    words: str
    beneficiary: str
    location: str
    date: QDate

    def to_dict(self):
        """Convert to dictionary."""
        return {
            "amount": self.amount,
            "words": self.words,
            "beneficiary": self.beneficiary,
            "location": self.location,
            "date": self.date
        }


class CheckTemplate:
    """Check template configuration."""
    
    TEMPLATES = {
        "BDR": "bdr_1.jpg",
        "BNA": "bna_1.jpg",
        "CCP": "chèque-ccp.png"
    }
    
    # Position sets for different check types
    # Coordinates (X, Y) in Percentages (0.0 to 1.0)
    POSITIONS = {
        "BDR": {
            "amount_num": (0.820, 0.009),
            "amount_words": (0.289, 0.264),
            "beneficiary": (0.246, 0.416),
            "location": (0.623, 0.508),
            "date": (0.750, 0.516)
        },
        "BNA": {
            "amount_num": (0.831, 0.044),
            "amount_words": (0.044, 0.375),
            "beneficiary": (0.263, 0.440),
            "location": (0.580, 0.567),
            "date": (0.771, 0.567)
        },
        "CCP": {
            "amount_num": (0.804, 0.028),
            "amount_words": (0.272, 0.244),
            "beneficiary": (0.180, 0.424),
            "location": (0.639, 0.472),
            "date": (0.765, 0.480)
        }
    }
    
    DEFAULT_POSITIONS = {
        "amount_num": (0.78, 0.05),
        "amount_words": (0.25, 0.28),
        "beneficiary": (0.20, 0.50),
        "location": (0.15, 0.65),
        "date": (0.50, 0.65)
    }
    
    @classmethod
    def get_positions(cls, check_type: Optional[str]) -> dict:
        """Get positions for a specific check type."""
        if check_type and check_type in cls.POSITIONS:
            return cls.POSITIONS[check_type]
        return cls.DEFAULT_POSITIONS
    
    @classmethod
    def get_template_path(cls, check_type: str) -> Optional[str]:
        """Get template file path."""
        return cls.TEMPLATES.get(check_type)
