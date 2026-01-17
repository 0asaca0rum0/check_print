#!/usr/bin/env python3
"""
Check Printer Application - Main Entry Point
Supports both Linux and Windows
"""
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.app import main

if __name__ == "__main__":
    main()
