"""
Loan Repository - Implementasi Adapter untuk akses data Loan

Mengimplementasikan BaseRepository interface untuk operasi database Loan
"""

from app.repositories.base_repository import BaseRepository
from app.models import Loan
from app.database import db
from datetime import datetime


class LoanRepository(BaseRepository):
    """
    Repository untuk operasi database tabel loans
    
    Pattern: Adapter
    Mengadaptasi operasi database SQLAlchemy ke interface standar
    """
    
    def find_all(self, filters=None):
        """
        Mendapatkan semua peminjaman
        
        Args:
            filters (dict): Optional filters
                - status: 'borrowed', 'returned', 'overdue'
                - book_id: Filter by book
                - borrower_name: Filter by borrower
                - limit: Batasi jumlah hasil
                - offset: Skip sejumlah record
        
        Returns:
            List[Loan]: Daftar peminjaman
        """
        query = Loan.query
        
        if filters:
            # Filter berdasarkan status
            if 'status' in filters and filters['status']:
                query = query.filter(Loan.status == filters['status'])
            
            # Filter berdasarkan book_id
            if 'book_id' in filters and filters['book_id']:
                query = query.filter(Loan.book_id == filters['book_id'])
            
            # Filter berdasarkan borrower
            if 'borrower_name' in filters and filters['borrower_name']:
                query = query.filter(
                    Loan.borrower_name.ilike(f"%{filters['borrower_name']}%")
                )
            
            # Pagination
            if 'limit' in filters:
                query = query.limit(filters['limit'])
            if 'offset' in filters:
                query = query.offset(filters['offset'])
        
        return query.order_by(Loan.created_at.desc()).all()
    
    def find_by_id(self, id):
        """
        Mendapatkan peminjaman berdasarkan ID
        
        Args:
            id: Loan ID
        
        Returns:
            Loan object atau None
        """
        return db.session.get(Loan, id)
    
    def save(self, loan):
        """
        Menyimpan peminjaman baru ke database
        
        Args:
            loan: Loan object
        
        Returns:
            Saved Loan object dengan ID
        """
        db.session.add(loan)
        db.session.commit()
        return loan
    
    def update(self, loan):
        """
        Update peminjaman yang sudah ada
        
        Args:
            loan: Loan object yang sudah dimodifikasi
        
        Returns:
            Updated Loan object
        """
        db.session.commit()
        return loan
    
    def delete(self, id):
        """
        Hapus peminjaman (hard delete)
        
        Args:
            id: Loan ID
        
        Returns:
            Boolean: True jika berhasil
        """
        loan = self.find_by_id(id)
        if loan:
            db.session.delete(loan)
            db.session.commit()
            return True
        return False
    
    def count(self, filters=None):
        """
        Menghitung jumlah peminjaman
        
        Args:
            filters: Optional filters
        
        Returns:
            Integer: jumlah peminjaman
        """
        query = Loan.query
        
        if filters:
            if 'status' in filters and filters['status']:
                query = query.filter(Loan.status == filters['status'])
            if 'book_id' in filters and filters['book_id']:
                query = query.filter(Loan.book_id == filters['book_id'])
        
        return query.count()
    
    def find_active_by_book(self, book_id):
        """
        Mendapatkan peminjaman aktif untuk buku tertentu
        
        Args:
            book_id: ID buku
        
        Returns:
            List[Loan]: Daftar peminjaman aktif
        """
        return Loan.query.filter_by(
            book_id=book_id,
            status='borrowed'
        ).all()
    
    def find_overdue_loans(self):
        """
        Mendapatkan semua peminjaman yang terlambat
        
        Returns:
            List[Loan]: Daftar peminjaman terlambat
        """
        today = datetime.utcnow().date()
        return Loan.query.filter(
            Loan.status == 'borrowed',
            Loan.due_date < today
        ).all()
    
    def find_by_borrower(self, borrower_name):
        """
        Mendapatkan semua peminjaman dari seorang peminjam
        
        Args:
            borrower_name: Nama peminjam
        
        Returns:
            List[Loan]: Daftar peminjaman
        """
        return Loan.query.filter(
            Loan.borrower_name.ilike(f"%{borrower_name}%")
        ).order_by(Loan.created_at.desc()).all()
    
    def get_loan_statistics(self):
        """
        Mendapatkan statistik peminjaman
        
        Returns:
            Dict: Statistik peminjaman
        """
        total = Loan.query.count()
        borrowed = Loan.query.filter_by(status='borrowed').count()
        returned = Loan.query.filter_by(status='returned').count()
        
        today = datetime.utcnow().date()
        overdue = Loan.query.filter(
            Loan.status == 'borrowed',
            Loan.due_date < today
        ).count()
        
        return {
            'total_loans': total,
            'borrowed_loans': borrowed,
            'returned_loans': returned,
            'overdue_loans': overdue
        }


# Singleton instance
loan_repository = LoanRepository()
