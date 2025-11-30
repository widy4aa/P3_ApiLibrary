"""
Model Book - Representasi tabel books di database

Model ini merepresentasikan entity Buku dalam sistem perpustakaan
"""

from datetime import datetime
from app.database import db


class Book(db.Model):
    """
    Model untuk tabel books
    
    Attributes:
        id: Primary key
        title: Judul buku
        author: Nama penulis
        isbn: International Standard Book Number (unique)
        year: Tahun terbit
        category: Kategori buku
        stock: Total stok buku
        available: Jumlah buku yang tersedia (tidak sedang dipinjam)
        created_at: Waktu pembuatan record
        updated_at: Waktu update terakhir
        is_deleted: Flag untuk soft delete
    """
    
    __tablename__ = 'books'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Book Information
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    isbn = db.Column(db.String(20), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    
    # Stock Management
    stock = db.Column(db.Integer, default=0, nullable=False)
    available = db.Column(db.Integer, default=0, nullable=False)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_deleted = db.Column(db.Boolean, default=False)
    
    # Relationship dengan Loan
    loans = db.relationship('Loan', backref='book', lazy=True)
    
    def __init__(self, title, author, isbn, year, category, stock):
        """
        Inisialisasi Book object
        
        Args:
            title: Judul buku
            author: Penulis
            isbn: ISBN
            year: Tahun terbit
            category: Kategori
            stock: Jumlah stok
        """
        self.title = title
        self.author = author
        self.isbn = isbn
        self.year = year
        self.category = category
        self.stock = stock
        self.available = stock  # Initially, semua stock tersedia
    
    def to_dict(self):
        """
        Konversi object Book ke dictionary untuk JSON response
        
        Returns:
            Dictionary representasi Book
        """
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'isbn': self.isbn,
            'year': self.year,
            'category': self.category,
            'stock': self.stock,
            'available': self.available,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'is_deleted': self.is_deleted
        }
    
    def __repr__(self):
        """String representation untuk debugging"""
        return f'<Book {self.id}: {self.title} by {self.author}>'
