"""
Utility functions for the Check Printer application.
"""
import os
import sys
from num2words import num2words


def get_resource_path(filename: str) -> str:
    """Get the absolute path to a resource file."""
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        base_path = sys._MEIPASS
    else:
        # Running as script
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    return os.path.join(base_path, filename)


def amount_to_words(amount: float, language: str = 'fr') -> str:
    """Convert numeric amount to words."""
    try:
        words = num2words(amount, lang=language)
        return f"{words} Dinars".capitalize()
    except Exception as e:
        print(f"Error converting amount to words: {e}")
        return "Erreur de conversion"


def format_amount_display(amount: float) -> str:
    """Format amount for display on check."""
    return f"{amount:,.2f}".replace(",", "X").replace(".", ",").replace("X", " ")


def is_windows() -> bool:
    """Check if running on Windows."""
    return sys.platform.startswith('win')


def is_linux() -> bool:
    """Check if running on Linux."""
    return sys.platform.startswith('linux')


def is_macos() -> bool:
    """Check if running on macOS."""
    return sys.platform.startswith('darwin')
