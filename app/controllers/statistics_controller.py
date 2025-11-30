"""
Statistics Controller - REST API endpoints untuk statistik perpustakaan
"""

from flask import Blueprint, jsonify
from app.services import statistics_service


# Buat Blueprint untuk statistics routes
statistics_bp = Blueprint('statistics', __name__, url_prefix='/api/statistics')


@statistics_bp.route('', methods=['GET'])
def get_statistics():
    """
    GET /api/statistics
    Mendapatkan statistik lengkap perpustakaan
    
    Returns:
        JSON: Statistik buku dan peminjaman
    """
    result = statistics_service.get_library_statistics()
    
    status_code = 200 if result['success'] else 500
    return jsonify(result), status_code


@statistics_bp.route('/categories', methods=['GET'])
def get_category_statistics():
    """
    GET /api/statistics/categories
    Mendapatkan statistik per kategori
    
    Returns:
        JSON: Statistik per kategori buku
    """
    result = statistics_service.get_category_statistics()
    
    status_code = 200 if result['success'] else 500
    return jsonify(result), status_code
