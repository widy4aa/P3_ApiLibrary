"""
Book Controller - REST API endpoints untuk manajemen buku

Menghandle HTTP request/response untuk operasi Book
"""

from flask import Blueprint, request, jsonify
from app.services import book_service
from app.repositories import book_repository


# Buat Blueprint untuk book routes
book_bp = Blueprint('books', __name__, url_prefix='/api/books')


@book_bp.route('', methods=['GET'])
def get_all_books():
    """
    GET /api/books
    Mendapatkan daftar semua buku
    
    Query Parameters:
        - category: Filter berdasarkan kategori
        - available_only: (true/false) Hanya buku yang tersedia
        - limit: Batasi jumlah hasil
        - offset: Skip sejumlah record
        - order_by: (title/year/created_at) Urutan sorting
    
    Returns:
        JSON: List buku dengan pagination info
    """
    # Parse query parameters
    filters = {}
    
    category = request.args.get('category')
    if category:
        filters['category'] = category
    
    available_only = request.args.get('available_only', '').lower() == 'true'
    if available_only:
        filters['available_only'] = True
    
    limit = request.args.get('limit')
    if limit:
        try:
            filters['limit'] = int(limit)
        except ValueError:
            pass
    
    offset = request.args.get('offset')
    if offset:
        try:
            filters['offset'] = int(offset)
        except ValueError:
            pass
    
    order_by = request.args.get('order_by')
    if order_by in ['title', 'year', 'created_at']:
        filters['order_by'] = order_by
    
    # Panggil service
    result = book_service.get_all_books(filters if filters else None)
    
    status_code = 200 if result['success'] else 500
    return jsonify(result), status_code


@book_bp.route('/isbn/<isbn>', methods=['GET'])
def get_book_by_isbn(isbn):
    """
    GET /api/books/isbn/:isbn
    Mendapatkan detail buku berdasarkan ISBN
    
    Path Parameters:
        - isbn: ISBN buku
    
    Returns:
        JSON: Detail buku
    """
    book = book_repository.find_by_isbn(isbn)
    
    if book:
        return jsonify({
            'success': True,
            'message': 'Buku ditemukan',
            'data': {
                'id': book.id,
                'title': book.title,
                'author': book.author,
                'isbn': book.isbn,
                'year': book.year,
                'category': book.category,
                'stock': book.stock,
                'available': book.available,
                'created_at': book.created_at.isoformat() if book.created_at else None,
                'updated_at': book.updated_at.isoformat() if book.updated_at else None
            }
        }), 200
    else:
        return jsonify({
            'success': False,
            'message': f'Buku dengan ISBN {isbn} tidak ditemukan'
        }), 404


@book_bp.route('/search', methods=['GET'])
def search_books():
    """
    GET /api/books/search?q=keyword
    Mencari buku berdasarkan keyword
    
    Query Parameters:
        - q: Kata kunci pencarian
    
    Returns:
        JSON: List buku yang cocok
    """
    keyword = request.args.get('q', '')
    
    result = book_service.search_books(keyword)
    
    status_code = 200 if result['success'] else 400
    return jsonify(result), status_code


@book_bp.route('/categories', methods=['GET'])
def get_categories():
    """
    GET /api/books/categories
    Mendapatkan daftar kategori buku
    
    Returns:
        JSON: List kategori
    """
    result = book_service.get_categories()
    
    status_code = 200 if result['success'] else 500
    return jsonify(result), status_code


@book_bp.route('/category/<category>', methods=['GET'])
def get_books_by_category(category):
    """
    GET /api/books/category/:category
    Mendapatkan buku berdasarkan kategori
    
    Path Parameters:
        - category: Nama kategori
    
    Returns:
        JSON: List buku dalam kategori
    """
    result = book_service.get_all_books({'category': category})
    
    status_code = 200 if result['success'] else 500
    return jsonify(result), status_code


@book_bp.route('/<int:book_id>', methods=['GET'])
def get_book(book_id):
    """
    GET /api/books/:id
    Mendapatkan detail buku berdasarkan ID
    
    Path Parameters:
        - book_id: ID buku
    
    Returns:
        JSON: Detail buku
    """
    result = book_service.get_book_by_id(book_id)
    
    if result['success']:
        return jsonify(result), 200
    else:
        return jsonify(result), 404


@book_bp.route('/<int:book_id>/availability', methods=['GET'])
def check_availability(book_id):
    """
    GET /api/books/:id/availability
    Mengecek ketersediaan buku
    
    Path Parameters:
        - book_id: ID buku
    
    Returns:
        JSON: Status ketersediaan
    """
    result = book_service.check_availability(book_id)
    
    if result['success']:
        return jsonify(result), 200
    else:
        return jsonify(result), 404


@book_bp.route('', methods=['POST'])
def create_book():
    """
    POST /api/books
    Menambahkan buku baru
    
    Request Body (JSON):
        - title: Judul buku (required)
        - author: Penulis (required)
        - isbn: ISBN (required, unique)
        - year: Tahun terbit (required)
        - category: Kategori (required)
        - stock: Jumlah stok (required)
    
    Returns:
        JSON: Data buku yang dibuat
    """
    # Validasi content type
    if not request.is_json:
        return jsonify({
            'success': False,
            'message': 'Content-Type harus application/json'
        }), 400
    
    data = request.get_json()
    
    if not data:
        return jsonify({
            'success': False,
            'message': 'Request body tidak boleh kosong'
        }), 400
    
    result = book_service.create_book(data)
    
    if result['success']:
        return jsonify(result), 201
    else:
        return jsonify(result), 400


@book_bp.route('/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    """
    PUT /api/books/:id
    Update data buku
    
    Path Parameters:
        - book_id: ID buku
    
    Request Body (JSON):
        - title: Judul buku (optional)
        - author: Penulis (optional)
        - isbn: ISBN (optional)
        - year: Tahun terbit (optional)
        - category: Kategori (optional)
        - stock: Jumlah stok (optional)
    
    Returns:
        JSON: Data buku yang diupdate
    """
    if not request.is_json:
        return jsonify({
            'success': False,
            'message': 'Content-Type harus application/json'
        }), 400
    
    data = request.get_json()
    
    if not data:
        return jsonify({
            'success': False,
            'message': 'Request body tidak boleh kosong'
        }), 400
    
    result = book_service.update_book(book_id, data)
    
    if result['success']:
        return jsonify(result), 200
    elif 'tidak ditemukan' in result.get('message', ''):
        return jsonify(result), 404
    else:
        return jsonify(result), 400


@book_bp.route('/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    """
    DELETE /api/books/:id
    Menghapus buku (soft delete)
    
    Path Parameters:
        - book_id: ID buku
    
    Returns:
        JSON: Konfirmasi penghapusan
    """
    result = book_service.delete_book(book_id)
    
    if result['success']:
        return jsonify(result), 200
    else:
        return jsonify(result), 404
