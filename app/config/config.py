"""
Konfigurasi aplikasi Flask
Mengelola environment variables dan settings aplikasi
"""

import os
from dotenv import load_dotenv

# Load environment variables dari file .env
load_dotenv()


class Config:
    """
    Kelas konfigurasi utama aplikasi
    Mengambil nilai dari environment variables
    """
    
    # Secret key untuk session management
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-please-change')
    
    # Database configuration - Default ke PostgreSQL
    # Format PostgreSQL dengan driver psycopg: postgresql+psycopg://username:password@host:port/database_name
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URI', 
        'postgresql+psycopg://postgres:postgres@localhost:5432/library_db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable modification tracking untuk performa
    
    # PostgreSQL specific settings
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,           # Jumlah koneksi dalam pool
        'pool_recycle': 3600,      # Recycle koneksi setiap 1 jam
        'pool_pre_ping': True,     # Cek koneksi sebelum digunakan
    }
    
    # CORS configuration
    CORS_HEADERS = 'Content-Type'
    
    # JSON configuration
    JSON_SORT_KEYS = False  # Tidak sort keys di JSON response
    JSONIFY_PRETTYPRINT_REGULAR = True  # Pretty print JSON di development
    
    # Application settings
    DEBUG = os.getenv('FLASK_ENV') == 'development'
    TESTING = False
    
    # Pagination
    ITEMS_PER_PAGE = 10
    
    # Logging
    LOG_FILE = 'logs/app.log'


class DevelopmentConfig(Config):
    """Konfigurasi untuk development"""
    DEBUG = True


class ProductionConfig(Config):
    """Konfigurasi untuk production"""
    DEBUG = False
    TESTING = False
    
    # Production - lebih banyak pool connections
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 20,
        'pool_recycle': 1800,
        'pool_pre_ping': True,
    }


class TestingConfig(Config):
    """Konfigurasi untuk testing"""
    TESTING = True
    # Bisa pakai SQLite untuk testing
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'TEST_DATABASE_URI', 
        'sqlite:///test_library.db'
    )


# Dictionary untuk memilih config berdasarkan environment
config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
