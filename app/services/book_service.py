"""
DESIGN PATTERN: FACADE
Book Service - Menyederhanakan operasi kompleks Book

Tujuan:
- Menyediakan interface sederhana untuk operasi kompleks
- Orchestrate multiple components (repository, validator, observer)
- Business logic terpusat
- Client tidak perlu tahu detail implementasi internal
"""

from app.repositories import book_repository
from app.factories import model_factory
from app.validators import book_validator
from app.observers import event_subject, EventType


class BookService:
    """
    Facade untuk operasi Book
    
    Pattern: Facade
    Menyederhanakan akses ke subsystem Book yang kompleks
    """
    
    def __init__(self):
        """
        Inisialisasi service dengan dependencies
        """
        self.repository = book_repository
        self.factory = model_factory
        self.validator = book_validator
        self.event_subject = event_subject
    
    def get_all_books(self, filters=None):
        """
        Mendapatkan semua buku
        
        Args:
            filters (dict): Optional filters
                - category: Filter by category
                - available_only: Hanya buku tersedia
                - limit: Batasi hasil
                - offset: Skip records
        
        Returns:
            dict: Response dengan list buku
        """
        try:
            books = self.repository.find_all(filters)
            total = self.repository.count(filters)
            
            return {
                'success': True,
                'data': [book.to_dict() for book in books],
                'total': total,
                'message': 'Data buku berhasil diambil'
            }
        except Exception as e:
            self.event_subject.notify(EventType.SYSTEM_ERROR, {'message': str(e)})
            return {
                'success': False,
                'message': f'Gagal mengambil data buku: {str(e)}',
                'data': []
            }
    
    def get_book_by_id(self, book_id):
        """
        Mendapatkan detail buku berdasarkan ID
        
        Args:
            book_id: ID buku
        
        Returns:
            dict: Response dengan detail buku
        """
        try:
            book = self.repository.find_by_id(book_id)
            
            if not book:
                return {
                    'success': False,
                    'message': f'Buku dengan ID {book_id} tidak ditemukan',
                    'data': None
                }
            
            return {
                'success': True,
                'data': book.to_dict(),
                'message': 'Detail buku berhasil diambil'
            }
        except Exception as e:
            self.event_subject.notify(EventType.SYSTEM_ERROR, {'message': str(e)})
            return {
                'success': False,
                'message': f'Gagal mengambil detail buku: {str(e)}',
                'data': None
            }
    
    def create_book(self, data):
        """
        Membuat buku baru
        
        Alur:
        1. Validasi input menggunakan Strategy Pattern
        2. Create Book object menggunakan Factory Pattern
        3. Simpan ke database via Repository Adapter
        4. Notify Observers
        
        Args:
            data (dict): Data buku baru
        
        Returns:
            dict: Response dengan hasil operasi
        """
        try:
            # Step 1: Validasi menggunakan Strategy Pattern
            is_valid, errors = self.validator.validate(data)
            if not is_valid:
                return {
                    'success': False,
                    'message': 'Validasi gagal',
                    'errors': errors
                }
            
            # Step 2: Create menggunakan Factory Pattern
            book = self.factory.create_book(data)
            
            # Step 3: Simpan menggunakan Repository Adapter
            saved_book = self.repository.save(book)
            
            # Step 4: Notify Observers
            self.event_subject.notify(
                EventType.BOOK_CREATED, 
                {'book': saved_book.to_dict()}
            )
            
            return {
                'success': True,
                'data': saved_book.to_dict(),
                'message': 'Buku berhasil ditambahkan'
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
                'message': f'Gagal menambahkan buku: {str(e)}',
                'errors': {}
            }
    
    def update_book(self, book_id, data):
        """
        Update buku yang sudah ada
        
        Args:
            book_id: ID buku yang akan diupdate
            data (dict): Data yang akan diupdate
        
        Returns:
            dict: Response dengan hasil operasi
        """
        try:
            # Cek apakah buku ada
            book = self.repository.find_by_id(book_id)
            if not book:
                return {
                    'success': False,
                    'message': f'Buku dengan ID {book_id} tidak ditemukan',
                    'data': None
                }
            
            # Tambahkan ID untuk validasi ISBN
            data['id'] = book_id
            
            # Validasi (is_update=True untuk partial validation)
            is_valid, errors = self.validator.validate(data, is_update=True)
            if not is_valid:
                return {
                    'success': False,
                    'message': 'Validasi gagal',
                    'errors': errors
                }
            
            # Update menggunakan Factory
            updated_book = self.factory.update_book(book, data)
            
            # Simpan perubahan
            self.repository.update(updated_book)
            
            # Notify Observers
            self.event_subject.notify(
                EventType.BOOK_UPDATED,
                {'book': updated_book.to_dict()}
            )
            
            return {
                'success': True,
                'data': updated_book.to_dict(),
                'message': 'Buku berhasil diupdate'
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
                'message': f'Gagal mengupdate buku: {str(e)}',
                'errors': {}
            }
    
    def delete_book(self, book_id):
        """
        Hapus buku (soft delete)
        
        Args:
            book_id: ID buku yang akan dihapus
        
        Returns:
            dict: Response dengan hasil operasi
        """
        try:
            # Cek apakah buku ada
            book = self.repository.find_by_id(book_id)
            if not book:
                return {
                    'success': False,
                    'message': f'Buku dengan ID {book_id} tidak ditemukan'
                }
            
            # Soft delete
            success = self.repository.delete(book_id)
            
            if success:
                # Notify Observers
                self.event_subject.notify(
                    EventType.BOOK_DELETED,
                    {'book_id': book_id, 'book_title': book.title}
                )
                
                return {
                    'success': True,
                    'message': f'Buku "{book.title}" berhasil dihapus'
                }
            else:
                return {
                    'success': False,
                    'message': 'Gagal menghapus buku'
                }
                
        except Exception as e:
            self.event_subject.notify(EventType.SYSTEM_ERROR, {'message': str(e)})
            return {
                'success': False,
                'message': f'Gagal menghapus buku: {str(e)}'
            }
    
    def search_books(self, keyword):
        """
        Mencari buku berdasarkan keyword
        
        Args:
            keyword: Kata kunci pencarian
        
        Returns:
            dict: Response dengan hasil pencarian
        """
        try:
            if not keyword or len(keyword.strip()) < 2:
                return {
                    'success': False,
                    'message': 'Kata kunci pencarian minimal 2 karakter',
                    'data': []
                }
            
            books = self.repository.search(keyword.strip())
            
            return {
                'success': True,
                'data': [book.to_dict() for book in books],
                'total': len(books),
                'keyword': keyword,
                'message': f'Ditemukan {len(books)} buku'
            }
            
        except Exception as e:
            self.event_subject.notify(EventType.SYSTEM_ERROR, {'message': str(e)})
            return {
                'success': False,
                'message': f'Gagal mencari buku: {str(e)}',
                'data': []
            }
    
    def get_categories(self):
        """
        Mendapatkan daftar kategori buku
        
        Returns:
            dict: Response dengan daftar kategori
        """
        try:
            categories = self.repository.get_categories()
            
            return {
                'success': True,
                'data': categories,
                'total': len(categories),
                'message': 'Daftar kategori berhasil diambil'
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Gagal mengambil kategori: {str(e)}',
                'data': []
            }
    
    def check_availability(self, book_id):
        """
        Cek ketersediaan buku
        
        Args:
            book_id: ID buku
        
        Returns:
            dict: Response dengan status ketersediaan
        """
        try:
            book = self.repository.find_by_id(book_id)
            
            if not book:
                return {
                    'success': False,
                    'message': f'Buku dengan ID {book_id} tidak ditemukan',
                    'data': None
                }
            
            return {
                'success': True,
                'data': {
                    'book_id': book.id,
                    'title': book.title,
                    'total_stock': book.stock,
                    'available': book.available,
                    'borrowed': book.stock - book.available,
                    'is_available': book.available > 0
                },
                'message': 'Status ketersediaan berhasil diambil'
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Gagal mengecek ketersediaan: {str(e)}',
                'data': None
            }


# Singleton instance
book_service = BookService()
