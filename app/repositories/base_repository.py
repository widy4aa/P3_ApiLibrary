
"""
DESIGN PATTERN: ADAPTER
Base Repository - Interface untuk data access layer

Tujuan:
- Abstraksi operasi database
- Memudahkan pergantian database (SQLite → PostgreSQL → MySQL)
- Separation of concerns antara business logic dan data access
- Consistent interface untuk semua repository
"""

from abc import ABC, abstractmethod


class BaseRepository(ABC):
    """
    Abstract Base Class untuk Repository
    
    Pattern: Adapter
    Menyediakan interface standar untuk operasi CRUD database
    Semua repository harus mengimplementasikan interface ini
    """
    
    @abstractmethod
    def find_all(self, filters=None):
        """
        Mendapatkan semua records
        
        Args:
            filters: Optional dictionary untuk filtering
        
        Returns:
            List of model objects
        """
        pass
    
    @abstractmethod
    def find_by_id(self, id):
        """
        Mendapatkan record berdasarkan ID
        
        Args:
            id: Primary key
        
        Returns:
            Model object atau None
        """
        pass
    
    @abstractmethod
    def save(self, entity):
        """
        Menyimpan entity baru ke database
        
        Args:
            entity: Model object yang akan disimpan
        
        Returns:
            Saved model object dengan ID
        """
        pass
    
    @abstractmethod
    def update(self, entity):
        """
        Update entity yang sudah ada
        
        Args:
            entity: Model object yang akan diupdate
        
        Returns:
            Updated model object
        """
        pass
    
    @abstractmethod
    def delete(self, id):
        """
        Hapus entity (soft delete)
        
        Args:
            id: Primary key dari entity yang akan dihapus
        
        Returns:
            Boolean: True jika berhasil
        """
        pass
    
    @abstractmethod
    def count(self, filters=None):
        """
        Menghitung jumlah records
        
        Args:
            filters: Optional dictionary untuk filtering
        
        Returns:
            Integer: jumlah records
        """
        pass
