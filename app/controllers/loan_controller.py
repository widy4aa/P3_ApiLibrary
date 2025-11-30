"""
Loan Controller - REST API endpoints untuk manajemen peminjaman

Menghandle HTTP request/response untuk operasi Loan
"""

from flask import Blueprint, request, jsonify
from app.services import loan_service


# Buat Blueprint untuk loan routes
loan_bp = Blueprint('loans', __name__, url_prefix='/api/loans')


@loan_bp.route('', methods=['GET'])
def get_all_loans():
    """
    GET /api/loans
    Mendapatkan daftar semua peminjaman
    
    Query Parameters:
        - status: Filter by status ('borrowed', 'returned', 'overdue')
        - book_id: Filter by book ID
        - borrower_name: Filter by borrower name
        - limit: Batasi jumlah hasil
        - offset: Skip sejumlah record
    
    Returns:
        JSON: List peminjaman
    """
    filters = {}
    
    status = request.args.get('status')
    if status in ['borrowed', 'returned', 'overdue']:
        filters['status'] = status
    
    book_id = request.args.get('book_id')
    if book_id:
        try:
            filters['book_id'] = int(book_id)
        except ValueError:
            pass
    
    borrower_name = request.args.get('borrower_name')
    if borrower_name:
        filters['borrower_name'] = borrower_name
    
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
    
    result = loan_service.get_all_loans(filters if filters else None)
    
    status_code = 200 if result['success'] else 500
    return jsonify(result), status_code


@loan_bp.route('/<int:loan_id>', methods=['GET'])
def get_loan(loan_id):
    """
    GET /api/loans/:id
    Mendapatkan detail peminjaman berdasarkan ID
    
    Path Parameters:
        - loan_id: ID peminjaman
    
    Returns:
        JSON: Detail peminjaman
    """
    result = loan_service.get_loan_by_id(loan_id)
    
    if result['success']:
        return jsonify(result), 200
    else:
        return jsonify(result), 404


@loan_bp.route('', methods=['POST'])
def create_loan():
    """
    POST /api/loans
    Membuat peminjaman baru
    
    Request Body (JSON):
        - book_id: ID buku yang dipinjam (required)
        - borrower_name: Nama peminjam (required)
        - loan_date: Tanggal pinjam YYYY-MM-DD (required)
        - due_date: Tanggal jatuh tempo YYYY-MM-DD (optional, default: 14 hari)
    
    Returns:
        JSON: Data peminjaman yang dibuat
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
    
    result = loan_service.create_loan(data)
    
    if result['success']:
        return jsonify(result), 201
    else:
        return jsonify(result), 400


@loan_bp.route('/<int:loan_id>', methods=['PUT'])
def update_loan(loan_id):
    """
    PUT /api/loans/:id
    Update data peminjaman (perpanjang, dll)
    
    Path Parameters:
        - loan_id: ID peminjaman
    
    Request Body (JSON):
        - due_date: Tanggal jatuh tempo baru (optional)
        - notes: Catatan (optional)
    
    Returns:
        JSON: Data peminjaman yang diupdate
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
    
    # Get existing loan
    loan_result = loan_service.get_loan_by_id(loan_id)
    if not loan_result['success']:
        return jsonify(loan_result), 404
    
    # Update loan via repository
    from app.repositories import loan_repository
    loan = loan_repository.find_by_id(loan_id)
    
    if 'due_date' in data:
        from datetime import datetime
        try:
            loan.due_date = datetime.strptime(data['due_date'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({
                'success': False,
                'message': 'Format due_date tidak valid. Gunakan YYYY-MM-DD'
            }), 400
    
    if 'notes' in data:
        loan.notes = data['notes']
    
    loan_repository.update(loan)
    
    return jsonify({
        'success': True,
        'message': 'Peminjaman berhasil diupdate',
        'data': {
            'id': loan.id,
            'book_id': loan.book_id,
            'borrower_name': loan.borrower_name,
            'loan_date': loan.loan_date.isoformat() if loan.loan_date else None,
            'due_date': loan.due_date.isoformat() if loan.due_date else None,
            'return_date': loan.return_date.isoformat() if loan.return_date else None,
            'status': loan.status,
            'notes': loan.notes
        }
    }), 200


@loan_bp.route('/<int:loan_id>/return', methods=['PUT'])
def return_book(loan_id):
    """
    PUT /api/loans/:id/return
    Proses pengembalian buku
    
    Path Parameters:
        - loan_id: ID peminjaman
    
    Request Body (JSON, optional):
        - return_date: Tanggal pengembalian YYYY-MM-DD (default: today)
    
    Returns:
        JSON: Data peminjaman yang diupdate
    """
    return_date = None
    
    if request.is_json:
        data = request.get_json()
        if data and 'return_date' in data:
            return_date = data['return_date']
    
    result = loan_service.return_book(loan_id, return_date)
    
    if result['success']:
        return jsonify(result), 200
    elif 'tidak ditemukan' in result.get('message', ''):
        return jsonify(result), 404
    else:
        return jsonify(result), 400


@loan_bp.route('/<int:loan_id>', methods=['DELETE'])
def delete_loan(loan_id):
    """
    DELETE /api/loans/:id
    Menghapus data peminjaman
    
    Path Parameters:
        - loan_id: ID peminjaman
    
    Returns:
        JSON: Konfirmasi penghapusan
    """
    from app.repositories import loan_repository
    
    loan = loan_repository.find_by_id(loan_id)
    if not loan:
        return jsonify({
            'success': False,
            'message': f'Peminjaman dengan ID {loan_id} tidak ditemukan'
        }), 404
    
    success = loan_repository.delete(loan_id)
    
    if success:
        return jsonify({
            'success': True,
            'message': 'Peminjaman berhasil dihapus'
        }), 200
    else:
        return jsonify({
            'success': False,
            'message': 'Gagal menghapus peminjaman'
        }), 500


@loan_bp.route('/overdue', methods=['GET'])
def get_overdue_loans():
    """
    GET /api/loans/overdue
    Mendapatkan daftar peminjaman yang terlambat
    
    Returns:
        JSON: List peminjaman terlambat
    """
    result = loan_service.get_overdue_loans()
    
    status_code = 200 if result['success'] else 500
    return jsonify(result), status_code


@loan_bp.route('/borrower/<borrower_name>', methods=['GET'])
def get_loans_by_borrower(borrower_name):
    """
    GET /api/loans/borrower/:borrower_name
    Mendapatkan peminjaman berdasarkan nama peminjam
    
    Path Parameters:
        - borrower_name: Nama peminjam
    
    Returns:
        JSON: List peminjaman
    """
    result = loan_service.get_loans_by_borrower(borrower_name)
    
    status_code = 200 if result['success'] else 500
    return jsonify(result), status_code


@loan_bp.route('/borrowed', methods=['GET'])
def get_borrowed_loans():
    """
    GET /api/loans/borrowed
    Mendapatkan semua peminjaman yang sedang berjalan
    
    Returns:
        JSON: List peminjaman borrowed
    """
    result = loan_service.get_all_loans({'status': 'borrowed'})
    
    status_code = 200 if result['success'] else 500
    return jsonify(result), status_code
