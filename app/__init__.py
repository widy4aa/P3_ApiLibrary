"""
Inisialisasi aplikasi Flask

Library Book Management API
Aplikasi REST API untuk manajemen buku perpustakaan
"""

from flask import Flask, jsonify
from flask_cors import CORS

from app.config import Config
from app.database import db_connection, db


def create_app(config_class=Config):
    """
    Application Factory Pattern
    Membuat dan mengkonfigurasi instance Flask app
    
    Args:
        config_class: Kelas konfigurasi yang akan digunakan
    
    Returns:
        Flask app instance
    """
    # Inisialisasi Flask
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Inisialisasi CORS
    CORS(app)
    
    # Inisialisasi database menggunakan Singleton
    db_connection.init_app(app)
    
    # Import dan register blueprints (controllers)
    from app.controllers import book_bp, loan_bp, statistics_bp
    
    app.register_blueprint(book_bp)
    app.register_blueprint(loan_bp)
    app.register_blueprint(statistics_bp)
    
    # Root endpoint
    @app.route('/')
    def index():
        """Root endpoint - API info"""
        return jsonify({
            'name': 'Library Book Management API',
            'version': '1.0.0',
            'description': 'REST API untuk manajemen buku perpustakaan',
            'endpoints': {
                'books': '/api/books',
                'loans': '/api/loans',
                'statistics': '/api/statistics'
            },
            'documentation': 'Lihat file README.md untuk dokumentasi lengkap'
        })
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        """Health check endpoint"""
        return jsonify({
            'status': 'healthy',
            'message': 'API is running'
        })
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'message': 'Endpoint tidak ditemukan'
        }), 404
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'message': 'Method tidak diizinkan'
        }), 405
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            'success': False,
            'message': 'Internal server error'
        }), 500
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app
