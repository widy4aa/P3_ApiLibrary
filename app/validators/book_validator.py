"""
Book Validator - Concrete Strategy untuk validasi data Book

Implementasi Strategy Pattern untuk validasi input buku
"""

from app.validators.validation_strategy import ValidationStrategy
from app.repositories import book_repository
from datetime import datetime


class BookValidationStrategy(ValidationStrategy):
    """
    Concrete Strategy untuk validasi data Book
    
    Pattern: Strategy
    Mengimplementasikan algoritma validasi spesifik untuk Book
    """
    
    # Daftar field yang wajib diisi untuk create
    REQUIRED_FIELDS_CREATE = ['title', 'author', 'isbn', 'year', 'category', 'stock']
    
    # Batasan validasi
    MAX_TITLE_LENGTH = 200
    MAX_AUTHOR_LENGTH = 100
    MAX_ISBN_LENGTH = 20
    MAX_CATEGORY_LENGTH = 50
    MIN_YEAR = 1000
    
    def validate(self, data, is_update=False):
        """
        Validasi data buku
        
        Args:
            data (dict): Data buku yang akan divalidasi
            is_update (bool): True jika untuk update (field tidak wajib lengkap)
        
        Returns:
            tuple: (is_valid: bool, errors: dict)
        """
        errors = {}
        
        # Cek required fields untuk create
        if not is_update:
            required_errors = self._check_required_fields(data, self.REQUIRED_FIELDS_CREATE)
            errors.update(required_errors)
        
        # Validasi title
        if 'title' in data and data['title']:
            error = self._check_string_length(
                data['title'], 'title', 
                min_len=1, 
                max_len=self.MAX_TITLE_LENGTH
            )
            if error:
                errors['title'] = error
        
        # Validasi author
        if 'author' in data and data['author']:
            error = self._check_string_length(
                data['author'], 'author', 
                min_len=1, 
                max_len=self.MAX_AUTHOR_LENGTH
            )
            if error:
                errors['author'] = error
        
        # Validasi ISBN
        if 'isbn' in data and data['isbn']:
            isbn_error = self._validate_isbn(data['isbn'], data.get('id'))
            if isbn_error:
                errors['isbn'] = isbn_error
        
        # Validasi year
        if 'year' in data:
            year_error = self._validate_year(data['year'])
            if year_error:
                errors['year'] = year_error
        
        # Validasi category
        if 'category' in data and data['category']:
            error = self._check_string_length(
                data['category'], 'category', 
                min_len=1, 
                max_len=self.MAX_CATEGORY_LENGTH
            )
            if error:
                errors['category'] = error
        
        # Validasi stock
        if 'stock' in data:
            stock_error = self._validate_stock(data['stock'])
            if stock_error:
                errors['stock'] = stock_error
        
        is_valid = len(errors) == 0
        return is_valid, errors
    
    def _validate_isbn(self, isbn, book_id=None):
        """
        Validasi ISBN
        
        Args:
            isbn: ISBN yang akan divalidasi
            book_id: ID buku (untuk update, skip jika ISBN sama)
        
        Returns:
            str or None: Error message atau None jika valid
        """
        if not isbn:
            return 'ISBN wajib diisi'
        
        isbn = str(isbn).strip()
        
        if len(isbn) > self.MAX_ISBN_LENGTH:
            return f'ISBN maksimal {self.MAX_ISBN_LENGTH} karakter'
        
        # Cek duplikasi ISBN
        existing_book = book_repository.find_by_isbn(isbn)
        if existing_book:
            if book_id is None or existing_book.id != book_id:
                return 'ISBN sudah terdaftar di sistem'
        
        return None
    
    def _validate_year(self, year):
        """
        Validasi tahun terbit
        
        Args:
            year: Tahun yang akan divalidasi
        
        Returns:
            str or None: Error message atau None jika valid
        """
        try:
            year_int = int(year)
        except (TypeError, ValueError):
            return 'Tahun harus berupa angka'
        
        current_year = datetime.now().year
        
        if year_int < self.MIN_YEAR:
            return f'Tahun minimal {self.MIN_YEAR}'
        
        if year_int > current_year + 1:
            return f'Tahun tidak boleh lebih dari {current_year + 1}'
        
        return None
    
    def _validate_stock(self, stock):
        """
        Validasi jumlah stock
        
        Args:
            stock: Jumlah stock yang akan divalidasi
        
        Returns:
            str or None: Error message atau None jika valid
        """
        try:
            stock_int = int(stock)
        except (TypeError, ValueError):
            return 'Stock harus berupa angka'
        
        if stock_int < 0:
            return 'Stock tidak boleh negatif'
        
        if stock_int > 10000:
            return 'Stock maksimal 10000'
        
        return None


# Singleton instance
book_validator = BookValidationStrategy()
