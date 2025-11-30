"""
Loan Validator - Concrete Strategy untuk validasi data Loan

Implementasi Strategy Pattern untuk validasi input peminjaman
"""

from app.validators.validation_strategy import ValidationStrategy
from app.repositories import book_repository, loan_repository
from datetime import datetime


class LoanValidationStrategy(ValidationStrategy):
    """
    Concrete Strategy untuk validasi data Loan
    
    Pattern: Strategy
    Mengimplementasikan algoritma validasi spesifik untuk Loan
    """
    
    # Daftar field yang wajib diisi
    REQUIRED_FIELDS = ['book_id', 'borrower_name', 'loan_date']
    
    # Batasan validasi
    MAX_BORROWER_NAME_LENGTH = 100
    MAX_LOAN_DAYS = 30  # Maksimal durasi pinjam
    
    def validate(self, data):
        """
        Validasi data peminjaman
        
        Args:
            data (dict): Data peminjaman yang akan divalidasi
        
        Returns:
            tuple: (is_valid: bool, errors: dict)
        """
        errors = {}
        
        # Cek required fields
        required_errors = self._check_required_fields(data, self.REQUIRED_FIELDS)
        errors.update(required_errors)
        
        # Validasi book_id
        if 'book_id' in data and data['book_id']:
            book_error = self._validate_book(data['book_id'])
            if book_error:
                errors['book_id'] = book_error
        
        # Validasi borrower_name
        if 'borrower_name' in data and data['borrower_name']:
            error = self._check_string_length(
                data['borrower_name'], 'borrower_name', 
                min_len=2, 
                max_len=self.MAX_BORROWER_NAME_LENGTH
            )
            if error:
                errors['borrower_name'] = error
        
        # Validasi loan_date
        if 'loan_date' in data and data['loan_date']:
            date_error = self._validate_date(data['loan_date'], 'loan_date')
            if date_error:
                errors['loan_date'] = date_error
        
        # Validasi due_date (optional)
        if 'due_date' in data and data['due_date']:
            date_error = self._validate_date(data['due_date'], 'due_date')
            if date_error:
                errors['due_date'] = date_error
            else:
                # Cek apakah due_date setelah loan_date
                duration_error = self._validate_loan_duration(
                    data.get('loan_date'), 
                    data['due_date']
                )
                if duration_error:
                    errors['due_date'] = duration_error
        
        is_valid = len(errors) == 0
        return is_valid, errors
    
    def validate_return(self, loan_id):
        """
        Validasi untuk proses pengembalian
        
        Args:
            loan_id: ID peminjaman
        
        Returns:
            tuple: (is_valid: bool, errors: dict)
        """
        errors = {}
        
        loan = loan_repository.find_by_id(loan_id)
        
        if not loan:
            errors['loan_id'] = 'Peminjaman tidak ditemukan'
        elif loan.status == 'returned':
            errors['loan_id'] = 'Buku sudah dikembalikan sebelumnya'
        
        is_valid = len(errors) == 0
        return is_valid, errors
    
    def _validate_book(self, book_id):
        """
        Validasi ketersediaan buku
        
        Args:
            book_id: ID buku yang akan dipinjam
        
        Returns:
            str or None: Error message atau None jika valid
        """
        try:
            book_id_int = int(book_id)
        except (TypeError, ValueError):
            return 'book_id harus berupa angka'
        
        # Cek apakah buku ada
        book = book_repository.find_by_id(book_id_int)
        if not book:
            return 'Buku tidak ditemukan'
        
        # Cek ketersediaan
        if book.available <= 0:
            return 'Buku tidak tersedia (semua sedang dipinjam)'
        
        return None
    
    def _validate_date(self, date_str, field_name):
        """
        Validasi format tanggal
        
        Args:
            date_str: String tanggal (format: YYYY-MM-DD)
            field_name: Nama field untuk error message
        
        Returns:
            str or None: Error message atau None jika valid
        """
        if not date_str:
            return f'{field_name} wajib diisi'
        
        try:
            parsed_date = datetime.strptime(str(date_str), '%Y-%m-%d').date()
        except ValueError:
            return f'{field_name} format tidak valid (gunakan: YYYY-MM-DD)'
        
        return None
    
    def _validate_loan_duration(self, loan_date_str, due_date_str):
        """
        Validasi durasi peminjaman
        
        Args:
            loan_date_str: Tanggal pinjam
            due_date_str: Tanggal jatuh tempo
        
        Returns:
            str or None: Error message atau None jika valid
        """
        try:
            loan_date = datetime.strptime(str(loan_date_str), '%Y-%m-%d').date()
            due_date = datetime.strptime(str(due_date_str), '%Y-%m-%d').date()
        except (ValueError, TypeError):
            return None  # Skip jika format invalid (akan ditangkap validasi lain)
        
        # Due date harus setelah atau sama dengan loan date
        if due_date < loan_date:
            return 'Tanggal jatuh tempo harus setelah tanggal pinjam'
        
        # Cek maksimal durasi
        duration = (due_date - loan_date).days
        if duration > self.MAX_LOAN_DAYS:
            return f'Durasi pinjam maksimal {self.MAX_LOAN_DAYS} hari'
        
        return None


# Singleton instance
loan_validator = LoanValidationStrategy()
