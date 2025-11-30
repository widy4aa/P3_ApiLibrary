"""
Package repositories
"""
from .base_repository import BaseRepository
from .book_repository import BookRepository, book_repository
from .loan_repository import LoanRepository, loan_repository

__all__ = [
    'BaseRepository',
    'BookRepository', 'book_repository',
    'LoanRepository', 'loan_repository'
]
