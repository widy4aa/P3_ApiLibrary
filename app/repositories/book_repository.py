"""
Book Repository - Implementasi Adapter untuk akses data Book

Mengimplementasikan BaseRepository interface untuk operasi database Book
"""

from app.repositories.base_repository import BaseRepository
from app.models import Book
from app.database import db


class BookRepository(BaseRepository):
    """
    Repository untuk operasi database tabel books
    
    Pattern: Adapter
    Mengadaptasi operasi database SQLAlchemy ke interface standar
    """
    
    def find_all(self, filters=None):
        """
        Mendapatkan semua buku yang tidak dihapus
        
        Args:
            filters (dict): Optional filters
                - category: Filter by category
                - available_only: Hanya buku yang tersedia
                - limit: Batasi jumlah hasil
                - offset: Skip sejumlah record
        
        Returns:
            List[Book]: Daftar buku
        """
        query = Book.query.filter_by(is_deleted=False)
        
        if filters:
            # Filter berdasarkan category
            if 'category' in filters and filters['category']:
                query = query.filter(Book.category.ilike(f"%{filters['category']}%"))
            
            # Filter hanya buku yang tersedia
            if filters.get('available_only'):
                query = query.filter(Book.available > 0)
            
            # Ordering
            if filters.get('order_by'):
                order_field = filters['order_by']
                if order_field == 'title':
                    query = query.order_by(Book.title)
                elif order_field == 'year':
                    query = query.order_by(Book.year.desc())
                elif order_field == 'created_at':
                    query = query.order_by(Book.created_at.desc())
            else:
                query = query.order_by(Book.created_at.desc())
            
            # Pagination
            if 'limit' in filters:
                query = query.limit(filters['limit'])
            if 'offset' in filters:
                query = query.offset(filters['offset'])
        else:
            query = query.order_by(Book.created_at.desc())
        
        return query.all()
    
    def find_by_id(self, id):
        """
        Mendapatkan buku berdasarkan ID
        
        Args:
            id: Book ID
        
        Returns:
            Book object atau None
        """
        return Book.query.filter_by(id=id, is_deleted=False).first()
    
    def find_by_isbn(self, isbn):
        """
        Mendapatkan buku berdasarkan ISBN
        
        Args:
            isbn: ISBN buku
        
        Returns:
            Book object atau None
        """
        return Book.query.filter_by(isbn=isbn, is_deleted=False).first()
    
    def save(self, book):
        """
        Menyimpan buku baru ke database
        
        Args:
            book: Book object
        
        Returns:
            Saved Book object dengan ID
        """
        db.session.add(book)
        db.session.commit()
        return book
    
    def update(self, book):
        """
        Update buku yang sudah ada
        
        Args:
            book: Book object yang sudah dimodifikasi
        
        Returns:
            Updated Book object
        """
        db.session.commit()
        return book
    
    def delete(self, id):
        """
        Soft delete buku
        
        Args:
            id: Book ID
        
        Returns:
            Boolean: True jika berhasil
        """
        book = self.find_by_id(id)
        if book:
            book.is_deleted = True
            db.session.commit()
            return True
        return False
    
    def hard_delete(self, id):
        """
        Hard delete buku (permanen)
        Gunakan dengan hati-hati!
        
        Args:
            id: Book ID
        
        Returns:
            Boolean: True jika berhasil
        """
        book = db.session.get(Book, id)
        if book:
            db.session.delete(book)
            db.session.commit()
            return True
        return False
    
    def count(self, filters=None):
        """
        Menghitung jumlah buku
        
        Args:
            filters: Optional filters
        
        Returns:
            Integer: jumlah buku
        """
        query = Book.query.filter_by(is_deleted=False)
        
        if filters:
            if 'category' in filters and filters['category']:
                query = query.filter(Book.category.ilike(f"%{filters['category']}%"))
            if filters.get('available_only'):
                query = query.filter(Book.available > 0)
        
        return query.count()
    
    def search(self, keyword):
        """
        Mencari buku berdasarkan keyword
        
        Args:
            keyword: Kata kunci pencarian
        
        Returns:
            List[Book]: Daftar buku yang cocok
        """
        if not keyword:
            return []
        
        search_term = f"%{keyword}%"
        return Book.query.filter(
            Book.is_deleted == False,
            db.or_(
                Book.title.ilike(search_term),
                Book.author.ilike(search_term),
                Book.isbn.ilike(search_term),
                Book.category.ilike(search_term)
            )
        ).order_by(Book.title).all()
    
    def get_categories(self):
        """
        Mendapatkan daftar semua kategori unik
        
        Returns:
            List[str]: Daftar kategori
        """
        result = db.session.query(Book.category).filter(
            Book.is_deleted == False
        ).distinct().all()
        return [r[0] for r in result]
    
    def update_availability(self, book_id, delta):
        """
        Update ketersediaan buku
        
        Args:
            book_id: ID buku
            delta: Perubahan jumlah (+1 untuk return, -1 untuk pinjam)
        
        Returns:
            Boolean: True jika berhasil
        """
        book = self.find_by_id(book_id)
        if book:
            new_available = book.available + delta
            if 0 <= new_available <= book.stock:
                book.available = new_available
                db.session.commit()
                return True
        return False


# Singleton instance
book_repository = BookRepository()
