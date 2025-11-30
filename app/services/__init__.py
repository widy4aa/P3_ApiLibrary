"""
Package services
"""
from .book_service import BookService, book_service
from .loan_service import LoanService, loan_service
from .statistics_service import StatisticsService, statistics_service

__all__ = [
    'BookService', 'book_service',
    'LoanService', 'loan_service',
    'StatisticsService', 'statistics_service'
]
