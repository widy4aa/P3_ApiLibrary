"""
Package controllers
"""
from .book_controller import book_bp
from .loan_controller import loan_bp
from .statistics_controller import statistics_bp

__all__ = ['book_bp', 'loan_bp', 'statistics_bp']
