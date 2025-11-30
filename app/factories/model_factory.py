"""
DESIGN PATTERN: FACTORY METHOD
Model Factory untuk membuat instance model objects secara konsisten

Tujuan:
- Centralized object creation
- Konsistensi dalam pembuatan objects
- Validasi dan transformasi data sebelum object creation
- Memudahkan perubahan logic pembuatan object di satu tempat
"""

from app.models import Book, Loan
from datetime import datetime


class ModelFactory:
    """
    Factory class untuk membuat model objects
    
    Pattern: Factory Method
    Menyediakan interface untuk membuat objects tanpa specify class secara eksplisit
    """
    
    @staticmethod
    def create_book(data):
        """
        Factory method untuk membuat Book object
        
        Args:
            data (dict): Dictionary berisi data buku
                - title: str
                - author: str
                - isbn: str
                - year: int
                - category: str
                - stock: int
        
        Returns:
            Book: Instance Book object yang sudah tervalidasi
        
        Raises:
            ValueError: Jika data tidak valid
        """
        try:
            # Extract dan validate data
            title = data.get('title', '').strip()
            author = data.get('author', '').strip()
            isbn = data.get('isbn', '').strip()
            year = int(data.get('year', 0))
            category = data.get('category', '').strip()
            stock = int(data.get('stock', 0))
            
            # Basic validation
            if not all([title, author, isbn, category]):
                raise ValueError("Semua field wajib diisi")
            
            if year < 1000 or year > datetime.now().year + 1:
                raise ValueError(f"Tahun tidak valid: {year}")
            
            if stock < 0:
                raise ValueError("Stock tidak boleh negatif")
            
            # Create Book instance
            book = Book(
                title=title,
                author=author,
                isbn=isbn,
                year=year,
                category=category,
                stock=stock
            )
            
            return book
            
        except (TypeError, ValueError) as e:
            raise ValueError(f"Error creating Book: {str(e)}")
    
    @staticmethod
    def create_loan(data):
        """
        Factory method untuk membuat Loan object
        
        Args:
            data (dict): Dictionary berisi data peminjaman
                - book_id: int
                - borrower_name: str
                - loan_date: str (format: YYYY-MM-DD)
                - due_date: str (optional, format: YYYY-MM-DD)
        
        Returns:
            Loan: Instance Loan object yang sudah tervalidasi
        
        Raises:
            ValueError: Jika data tidak valid
        """
        try:
            # Extract data
            book_id = int(data.get('book_id', 0))
            borrower_name = data.get('borrower_name', '').strip()
            loan_date_str = data.get('loan_date', '')
            due_date_str = data.get('due_date', None)
            
            # Basic validation
            if not book_id or not borrower_name or not loan_date_str:
                raise ValueError("book_id, borrower_name, dan loan_date wajib diisi")
            
            # Parse dates
            try:
                loan_date = datetime.strptime(loan_date_str, '%Y-%m-%d').date()
            except ValueError:
                raise ValueError("Format loan_date tidak valid. Gunakan: YYYY-MM-DD")
            
            due_date = None
            if due_date_str:
                try:
                    due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
                except ValueError:
                    raise ValueError("Format due_date tidak valid. Gunakan: YYYY-MM-DD")
            
            # Create Loan instance
            loan = Loan(
                book_id=book_id,
                borrower_name=borrower_name,
                loan_date=loan_date,
                due_date=due_date
            )
            
            return loan
            
        except (TypeError, ValueError) as e:
            raise ValueError(f"Error creating Loan: {str(e)}")
    
    @staticmethod
    def update_book(book, data):
        """
        Factory method untuk update Book object
        
        Args:
            book (Book): Book object yang akan diupdate
            data (dict): Dictionary berisi data yang akan diupdate
        
        Returns:
            Book: Updated Book object
        """
        # Update hanya field yang ada di data
        if 'title' in data and data['title']:
            book.title = data['title'].strip()
        
        if 'author' in data and data['author']:
            book.author = data['author'].strip()
        
        if 'isbn' in data and data['isbn']:
            book.isbn = data['isbn'].strip()
        
        if 'year' in data:
            year = int(data['year'])
            if year < 1000 or year > datetime.now().year + 1:
                raise ValueError(f"Tahun tidak valid: {year}")
            book.year = year
        
        if 'category' in data and data['category']:
            book.category = data['category'].strip()
        
        if 'stock' in data:
            stock = int(data['stock'])
            if stock < 0:
                raise ValueError("Stock tidak boleh negatif")
            
            # Adjust available berdasarkan perubahan stock
            diff = stock - book.stock
            book.stock = stock
            book.available = max(0, book.available + diff)
        
        # Update timestamp
        book.updated_at = datetime.utcnow()
        
        return book


# Singleton instance untuk digunakan di seluruh aplikasi
model_factory = ModelFactory()
