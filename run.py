"""
Entry point untuk menjalankan aplikasi Flask

Library Book Management API
===========================
Aplikasi REST API untuk manajemen buku perpustakaan
dengan arsitektur MVC dan implementasi 6 Design Patterns

Cara menjalankan:
    python run.py
    
Atau:
    flask run
"""

import os
from app import create_app

# Buat instance aplikasi
app = create_app()

if __name__ == '__main__':
    # Konfigurasi server
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_ENV', 'development') == 'development'
    
    print(f"""
    ╔══════════════════════════════════════════════════════════╗
    ║       Library Book Management API v1.0.0                  ║
    ╠══════════════════════════════════════════════════════════╣
    ║  Server berjalan di: http://localhost:{port}               ║
    ║  Mode: {'Development' if debug else 'Production'}                                     ║
    ║                                                          ║
    ║  Endpoints:                                              ║
    ║  - Books:      http://localhost:{port}/api/books           ║
    ║  - Loans:      http://localhost:{port}/api/loans           ║
    ║  - Statistics: http://localhost:{port}/api/statistics      ║
    ║                                                          ║
    ║  Dokumentasi: Lihat README.md                            ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    # Jalankan server
    app.run(host=host, port=port, debug=debug)
