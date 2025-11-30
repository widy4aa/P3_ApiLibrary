"""
Model Loan - Representasi tabel loans di database

Model ini merepresentasikan peminjaman buku
"""

from datetime import datetime, timedelta
from app.database import db


class Loan(db.Model):
    """
    Model untuk tabel loans
    
    Attributes:
        id: Primary key
        book_id: Foreign key ke tabel books
        borrower_name: Nama peminjam
        loan_date: Tanggal pinjam
        due_date: Tanggal jatuh tempo pengembalian
        return_date: Tanggal actual pengembalian (null jika belum dikembalikan)
        status: Status peminjaman ('borrowed', 'returned', 'overdue')
        notes: Catatan tambahan terkait peminjaman/perpanjangan
        created_at: Waktu pembuatan record
    """
    
    __tablename__ = 'loans'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Foreign Key
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    
    # Loan Information
    borrower_name = db.Column(db.String(100), nullable=False)
    loan_date = db.Column(db.Date, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(20), default='borrowed', nullable=False)  # 'borrowed', 'returned', 'overdue'
    notes = db.Column(db.Text, nullable=True)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, book_id, borrower_name, loan_date, due_date=None, notes=None):
        """
        Inisialisasi Loan object
        
        Args:
            book_id: ID buku yang dipinjam
            borrower_name: Nama peminjam
            loan_date: Tanggal pinjam
            due_date: Tanggal jatuh tempo (default: 14 hari dari loan_date)
        """
        self.book_id = book_id
        self.borrower_name = borrower_name
        
        # Konversi string ke date object jika diperlukan
        if isinstance(loan_date, str):
            self.loan_date = datetime.strptime(loan_date, '%Y-%m-%d').date()
        else:
            self.loan_date = loan_date
        
        # Set due_date (default 14 hari dari loan_date)
        if due_date:
            if isinstance(due_date, str):
                self.due_date = datetime.strptime(due_date, '%Y-%m-%d').date()
            else:
                self.due_date = due_date
        else:
            self.due_date = self.loan_date + timedelta(days=14)
        
        self.status = 'borrowed'
        self.notes = notes
    
    def mark_as_returned(self, return_date=None):
        """
        Tandai peminjaman sebagai sudah dikembalikan
        
        Args:
            return_date: Tanggal pengembalian (default: today)
        """
        if return_date:
            if isinstance(return_date, str):
                self.return_date = datetime.strptime(return_date, '%Y-%m-%d').date()
            else:
                self.return_date = return_date
        else:
            self.return_date = datetime.utcnow().date()
        
        self.status = 'returned'
    
    def is_overdue(self):
        """
        Cek apakah peminjaman sudah terlambat
        
        Returns:
            Boolean: True jika terlambat
        """
        if self.status == 'returned':
            return False
        return datetime.utcnow().date() > self.due_date
    
    def to_dict(self):
        """
        Konversi object Loan ke dictionary untuk JSON response
        
        Returns:
            Dictionary representasi Loan
        """
        return {
            'id': self.id,
            'book_id': self.book_id,
            'book_title': self.book.title if self.book else None,
            'borrower_name': self.borrower_name,
            'loan_date': self.loan_date.isoformat() if self.loan_date else None,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'return_date': self.return_date.isoformat() if self.return_date else None,
            'status': self.status,
            'is_overdue': self.is_overdue(),
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        """String representation untuk debugging"""
        return f'<Loan {self.id}: Book {self.book_id} by {self.borrower_name} ({self.status})>'
