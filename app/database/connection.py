"""
DESIGN PATTERN: SINGLETON
Database Connection Manager menggunakan Singleton Pattern

Tujuan:
- Memastikan hanya ada SATU instance koneksi database
- Menghemat resource dan mencegah multiple connections
- Thread-safe implementation
"""

from flask_sqlalchemy import SQLAlchemy
from threading import Lock


class DatabaseConnection:
    """
    Singleton class untuk mengelola database connection
    
    Pattern: Singleton
    Garantir bahwa hanya ada satu instance SQLAlchemy di seluruh aplikasi
    """
    
    _instance = None  # Private class variable untuk menyimpan singleton instance
    _lock = Lock()    # Lock untuk thread safety
    
    def __new__(cls):
        """
        Override __new__ untuk implementasi Singleton
        Menggunakan double-checked locking untuk thread safety
        """
        if cls._instance is None:
            with cls._lock:
                # Double-check untuk thread safety
                if cls._instance is None:
                    cls._instance = super(DatabaseConnection, cls).__new__(cls)
                    # Inisialisasi SQLAlchemy hanya sekali
                    cls._instance.db = SQLAlchemy()
                    cls._instance._initialized = False
        return cls._instance
    
    def init_app(self, app):
        """
        Inisialisasi database dengan Flask app
        
        Args:
            app: Flask application instance
        """
        if not self._initialized:
            self.db.init_app(app)
            self._initialized = True
    
    def get_db(self):
        """
        Mendapatkan instance SQLAlchemy
        
        Returns:
            SQLAlchemy instance
        """
        return self.db
    
    def create_tables(self, app):
        """
        Membuat semua tabel di database
        
        Args:
            app: Flask application instance
        """
        with app.app_context():
            self.db.create_all()
    
    def drop_tables(self, app):
        """
        Menghapus semua tabel (untuk testing/reset)
        
        Args:
            app: Flask application instance
        """
        with app.app_context():
            self.db.drop_all()


# Singleton instance yang akan digunakan di seluruh aplikasi
db_connection = DatabaseConnection()
db = db_connection.get_db()


def get_db_instance():
    """
    Helper function untuk mendapatkan database instance
    
    Returns:
        SQLAlchemy instance
    """
    return db
