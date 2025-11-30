"""
Loan Service - Facade untuk operasi peminjaman buku

Mengelola proses peminjaman dan pengembalian buku
"""

from app.repositories import book_repository, loan_repository
from app.factories import model_factory
from app.validators import loan_validator
from app.observers import event_subject, EventType


class LoanService:
    """
    Facade untuk operasi Loan (Peminjaman)
    
    Pattern: Facade
    Menyederhanakan akses ke subsystem Loan yang kompleks
    """
    
    def __init__(self):
        """
        Inisialisasi service dengan dependencies
        """
        self.loan_repository = loan_repository
        self.book_repository = book_repository
        self.factory = model_factory
        self.validator = loan_validator
        self.event_subject = event_subject
    
    def get_all_loans(self, filters=None):
        """
        Mendapatkan semua peminjaman
        
        Args:
            filters (dict): Optional filters
                - status: 'borrowed', 'returned', 'overdue'
                - book_id: Filter by book
                - borrower_name: Filter by borrower
        
        Returns:
            dict: Response dengan list peminjaman
        """
        try:
            loans = self.loan_repository.find_all(filters)
            total = self.loan_repository.count(filters)
            
            return {
                'success': True,
                'data': [loan.to_dict() for loan in loans],
                'total': total,
                'message': 'Data peminjaman berhasil diambil'
            }
        except Exception as e:
            self.event_subject.notify(EventType.SYSTEM_ERROR, {'message': str(e)})
            return {
                'success': False,
                'message': f'Gagal mengambil data peminjaman: {str(e)}',
                'data': []
            }
    
    def get_loan_by_id(self, loan_id):
        """
        Mendapatkan detail peminjaman berdasarkan ID
        
        Args:
            loan_id: ID peminjaman
        
        Returns:
            dict: Response dengan detail peminjaman
        """
        try:
            loan = self.loan_repository.find_by_id(loan_id)
            
            if not loan:
                return {
                    'success': False,
                    'message': f'Peminjaman dengan ID {loan_id} tidak ditemukan',
                    'data': None
                }
            
            return {
                'success': True,
                'data': loan.to_dict(),
                'message': 'Detail peminjaman berhasil diambil'
            }
        except Exception as e:
            self.event_subject.notify(EventType.SYSTEM_ERROR, {'message': str(e)})
            return {
                'success': False,
                'message': f'Gagal mengambil detail peminjaman: {str(e)}',
                'data': None
            }
    
    def create_loan(self, data):
        """
        Membuat peminjaman baru
        
        Alur:
        1. Validasi input
        2. Cek ketersediaan buku
        3. Create Loan object
        4. Kurangi available count di buku
        5. Simpan peminjaman
        6. Notify Observers
        
        Args:
            data (dict): Data peminjaman
        
        Returns:
            dict: Response dengan hasil operasi
        """
        try:
            # Step 1: Validasi input
            is_valid, errors = self.validator.validate(data)
            if not is_valid:
                return {
                    'success': False,
                    'message': 'Validasi gagal',
                    'errors': errors
                }
            
            # Step 2: Cek ketersediaan buku
            book = self.book_repository.find_by_id(data['book_id'])
            if not book:
                return {
                    'success': False,
                    'message': 'Buku tidak ditemukan',
                    'errors': {'book_id': 'Buku tidak ditemukan'}
                }
            
            if book.available <= 0:
                return {
                    'success': False,
                    'message': 'Buku tidak tersedia',
                    'errors': {'book_id': 'Semua buku sedang dipinjam'}
                }
            
            # Step 3: Create Loan object
            loan = self.factory.create_loan(data)
            
            # Step 4: Kurangi available count
            book.available -= 1
            self.book_repository.update(book)
            
            # Step 5: Simpan peminjaman
            saved_loan = self.loan_repository.save(loan)
            
            # Step 6: Notify Observers
            self.event_subject.notify(
                EventType.LOAN_CREATED,
                {'loan': saved_loan.to_dict()}
            )
            
            return {
                'success': True,
                'data': saved_loan.to_dict(),
                'message': 'Peminjaman berhasil dibuat'
            }
            
        except ValueError as e:
            return {
                'success': False,
                'message': str(e),
                'errors': {}
            }
        except Exception as e:
            self.event_subject.notify(EventType.SYSTEM_ERROR, {'message': str(e)})
            return {
                'success': False,
                'message': f'Gagal membuat peminjaman: {str(e)}',
                'errors': {}
            }
    
    def return_book(self, loan_id, return_date=None):
        """
        Proses pengembalian buku
        
        Args:
            loan_id: ID peminjaman
            return_date: Tanggal pengembalian (optional, default: today)
        
        Returns:
            dict: Response dengan hasil operasi
        """
        try:
            # Validasi
            is_valid, errors = self.validator.validate_return(loan_id)
            if not is_valid:
                return {
                    'success': False,
                    'message': 'Validasi gagal',
                    'errors': errors
                }
            
            # Ambil data loan
            loan = self.loan_repository.find_by_id(loan_id)
            
            # Update loan status
            loan.mark_as_returned(return_date)
            self.loan_repository.update(loan)
            
            # Tambah available count di buku
            book = self.book_repository.find_by_id(loan.book_id)
            if book:
                book.available = min(book.stock, book.available + 1)
                self.book_repository.update(book)
            
            # Notify Observers
            self.event_subject.notify(
                EventType.LOAN_RETURNED,
                {'loan': loan.to_dict()}
            )
            
            return {
                'success': True,
                'data': loan.to_dict(),
                'message': 'Buku berhasil dikembalikan'
            }
            
        except Exception as e:
            self.event_subject.notify(EventType.SYSTEM_ERROR, {'message': str(e)})
            return {
                'success': False,
                'message': f'Gagal mengembalikan buku: {str(e)}',
                'errors': {}
            }
    
    def get_overdue_loans(self):
        """
        Mendapatkan daftar peminjaman yang terlambat
        
        Returns:
            dict: Response dengan daftar peminjaman terlambat
        """
        try:
            loans = self.loan_repository.find_overdue_loans()
            
            return {
                'success': True,
                'data': [loan.to_dict() for loan in loans],
                'total': len(loans),
                'message': f'Ditemukan {len(loans)} peminjaman terlambat'
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Gagal mengambil data: {str(e)}',
                'data': []
            }
    
    def get_loans_by_borrower(self, borrower_name):
        """
        Mendapatkan peminjaman berdasarkan nama peminjam
        
        Args:
            borrower_name: Nama peminjam
        
        Returns:
            dict: Response dengan daftar peminjaman
        """
        try:
            loans = self.loan_repository.find_by_borrower(borrower_name)
            
            return {
                'success': True,
                'data': [loan.to_dict() for loan in loans],
                'total': len(loans),
                'message': f'Ditemukan {len(loans)} peminjaman'
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Gagal mengambil data: {str(e)}',
                'data': []
            }


# Singleton instance
loan_service = LoanService()
