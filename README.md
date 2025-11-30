# Library Book Management API

Aplikasi REST API untuk manajemen buku perpustakaan dengan arsitektur MVC dan implementasi 6 Design Patterns.

## 📚 Daftar Isi

1. [Tentang Aplikasi](#tentang-aplikasi)
2. [Fitur](#fitur)
3. [Arsitektur & Design Patterns](#arsitektur--design-patterns)
4. [Instalasi](#instalasi)
5. [Setup PostgreSQL](#setup-postgresql)
6. [Menjalankan Aplikasi](#menjalankan-aplikasi)
7. [Dokumentasi API](#dokumentasi-api)
8. [Testing dengan Postman](#testing-dengan-postman)
9. [Struktur Folder](#struktur-folder)

---

## 📖 Tentang Aplikasi

Library Book Management API adalah sistem backend berbasis REST API untuk mengelola koleksi buku perpustakaan. Aplikasi ini dibangun menggunakan:

- **Framework**: Flask 2.3
- **Database**: PostgreSQL
- **Architecture**: MVC (Model-View-Controller)
- **Design Patterns**: 6 patterns (Singleton, Factory, Adapter, Facade, Strategy, Observer)

---

## ✨ Fitur

### Manajemen Buku
- ✅ Tambah buku baru
- ✅ Lihat daftar semua buku
- ✅ Lihat detail buku
- ✅ Update informasi buku
- ✅ Hapus buku (soft delete)
- ✅ Pencarian buku
- ✅ Filter berdasarkan kategori
- ✅ Cek ketersediaan buku

### Peminjaman Buku
- ✅ Pinjam buku
- ✅ Kembalikan buku
- ✅ Lihat daftar peminjaman
- ✅ Lihat peminjaman terlambat
- ✅ Filter berdasarkan status/peminjam

### Statistik
- ✅ Total buku dan ketersediaan
- ✅ Statistik peminjaman
- ✅ Statistik per kategori

---

## 🏗️ Arsitektur & Design Patterns

### MVC Architecture
```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ CONTROLLER  │────►│   SERVICE   │────►│    MODEL    │
│  (Routes)   │     │  (Facade)   │     │  (Entity)   │
└─────────────┘     └─────────────┘     └─────────────┘
```

### Design Patterns Implemented

| Pattern | Type | Lokasi | Fungsi |
|---------|------|--------|--------|
| **Singleton** | Creational | `database/connection.py` | Single database connection |
| **Factory Method** | Creational | `factories/model_factory.py` | Konsisten membuat objects |
| **Adapter** | Structural | `repositories/*.py` | Abstraksi database operations |
| **Facade** | Structural | `services/*.py` | Simplifikasi business logic |
| **Strategy** | Behavioral | `validators/*.py` | Flexible validation rules |
| **Observer** | Behavioral | `observers/*.py` | Auto-logging events |

---

## 🔧 Instalasi

### Prasyarat
- Python 3.8 atau lebih tinggi
- pip (Python package manager)
- **PostgreSQL 12 atau lebih tinggi**

### Langkah Instalasi

1. **Clone atau download project**
   ```bash
   cd C:\Users\widy4aa\Desktop\P3
   ```

2. **Buat virtual environment (opsional tapi direkomendasikan)**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

---

## 🐘 Setup PostgreSQL

### 1. Install PostgreSQL

**Windows:**
- Download dari https://www.postgresql.org/download/windows/
- Jalankan installer dan ikuti petunjuk
- Ingat password yang Anda set untuk user `postgres`

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
```

**MacOS:**
```bash
brew install postgresql
brew services start postgresql
```

### 2. Buat Database

Buka terminal/command prompt dan jalankan:

**Windows (menggunakan psql):**
```cmd
psql -U postgres
```

**Linux/MacOS:**
```bash
sudo -u postgres psql
```

Kemudian jalankan perintah SQL:
```sql
-- Buat database
CREATE DATABASE library_db;

-- Verifikasi database dibuat
\l

-- Keluar dari psql
\q
```

### 3. Konfigurasi Environment

Edit file `.env` sesuai konfigurasi PostgreSQL Anda:
```
# PostgreSQL Database Configuration
# Format: postgresql+psycopg://username:password@host:port/database_name
DATABASE_URI=postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5432/library_db
```

Ganti `YOUR_PASSWORD` dengan password PostgreSQL Anda.

### 4. Inisialisasi Tabel Database

```bash
python init_db.py
```

Untuk menambahkan data sample:
```bash
python init_db.py --seed
```

---

## 🚀 Menjalankan Aplikasi

### Development Mode
```bash
python run.py
```

Atau menggunakan Flask CLI:
```bash
flask run
```

Server akan berjalan di: `http://localhost:5000`

### Verifikasi
Buka browser atau Postman dan akses:
```
GET http://localhost:5000
```

Response yang diharapkan:
```json
{
    "name": "Library Book Management API",
    "version": "1.0.0",
    "description": "REST API untuk manajemen buku perpustakaan",
    "endpoints": {
        "books": "/api/books",
        "loans": "/api/loans",
        "statistics": "/api/statistics"
    }
}
```

---

## 📡 Dokumentasi API

### Base URL
```
http://localhost:5000/api
```

### Endpoints Overview

| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| GET | `/api/books` | Daftar semua buku |
| GET | `/api/books/isbn/:isbn` | Detail buku berdasarkan ISBN |
| GET | `/api/books/:id` | Detail buku |
| POST | `/api/books` | Tambah buku |
| PUT | `/api/books/:id` | Update buku |
| DELETE | `/api/books/:id` | Hapus buku |
| GET | `/api/books/search?q=keyword` | Cari buku |
| GET | `/api/books/categories` | Daftar kategori |
| GET | `/api/books/category/:category` | Buku per kategori |
| GET | `/api/books/:id/availability` | Cek ketersediaan |
| GET | `/api/loans` | Daftar peminjaman |
| GET | `/api/loans/:id` | Detail peminjaman |
| PUT | `/api/loans/:id` | Update peminjaman (perpanjang/catatan) |
| POST | `/api/loans` | Buat peminjaman |
| PUT | `/api/loans/:id/return` | Kembalikan buku |
| DELETE | `/api/loans/:id` | Hapus peminjaman |
| GET | `/api/loans/overdue` | Peminjaman terlambat |
| GET | `/api/loans/borrowed` | Peminjaman yang sedang berjalan |
| GET | `/api/statistics` | Statistik perpustakaan |
| GET | `/api/statistics/categories` | Statistik per kategori |

---

## 🧪 Testing dengan Postman

### 1. Tambah Buku Baru

**Request:**
```
POST http://localhost:5000/api/books
Content-Type: application/json
```

**Body:**
```json
{
    "title": "Clean Code",
    "author": "Robert C. Martin",
    "isbn": "978-0132350884",
    "year": 2008,
    "category": "Programming",
    "stock": 5
}
```

**Response Sukses (201):**
```json
{
    "success": true,
    "message": "Buku berhasil ditambahkan",
    "data": {
        "id": 1,
        "title": "Clean Code",
        "author": "Robert C. Martin",
        "isbn": "978-0132350884",
        "year": 2008,
        "category": "Programming",
        "stock": 5,
        "available": 5,
        "created_at": "2025-11-30T10:00:00",
        "updated_at": "2025-11-30T10:00:00",
        "is_deleted": false
    }
}
```

**Response Error (400):**
```json
{
    "success": false,
    "message": "Validasi gagal",
    "errors": {
        "isbn": "ISBN sudah terdaftar di sistem",
        "year": "Tahun tidak boleh lebih dari 2026"
    }
}
```

---

### 2. Lihat Semua Buku

**Request:**
```
GET http://localhost:5000/api/books
```

**Query Parameters (opsional):**
- `category`: Filter by kategori
- `available_only`: true/false
- `limit`: Batasi hasil (contoh: 10)
- `offset`: Skip records (contoh: 0)
- `order_by`: title/year/created_at

**Contoh:**
```
GET http://localhost:5000/api/books?category=Programming&available_only=true&limit=10
```

**Response:**
```json
{
    "success": true,
    "message": "Data buku berhasil diambil",
    "data": [
        {
            "id": 1,
            "title": "Clean Code",
            "author": "Robert C. Martin",
            ...
        }
    ],
    "total": 1
}
```

---

### 3. Lihat Detail Buku

**Request:**
```
GET http://localhost:5000/api/books/1
```

**Response:**
```json
{
    "success": true,
    "message": "Detail buku berhasil diambil",
    "data": {
        "id": 1,
        "title": "Clean Code",
        "author": "Robert C. Martin",
        "isbn": "978-0132350884",
        "year": 2008,
        "category": "Programming",
        "stock": 5,
        "available": 5,
        "created_at": "2025-11-30T10:00:00",
        "updated_at": "2025-11-30T10:00:00",
        "is_deleted": false
    }
}
```

---

### 4. Update Buku

**Request:**
```
PUT http://localhost:5000/api/books/1
Content-Type: application/json
```

**Body (partial update):**
```json
{
    "stock": 10,
    "category": "Software Engineering"
}
```

**Response:**
```json
{
    "success": true,
    "message": "Buku berhasil diupdate",
    "data": {
        "id": 1,
        "title": "Clean Code",
        "stock": 10,
        "category": "Software Engineering",
        ...
    }
}
```

---

### 5. Hapus Buku

**Request:**
```
DELETE http://localhost:5000/api/books/1
```

**Response:**
```json
{
    "success": true,
    "message": "Buku \"Clean Code\" berhasil dihapus"
}
```

---

### 6. Cari Buku

**Request:**
```
GET http://localhost:5000/api/books/search?q=python
```

**Response:**
```json
{
    "success": true,
    "message": "Ditemukan 2 buku",
    "keyword": "python",
    "data": [...],
    "total": 2
}
```

---

### 7. Pinjam Buku

**Request:**
```
POST http://localhost:5000/api/loans
Content-Type: application/json
```

**Body:**
```json
{
    "book_id": 1,
    "borrower_name": "John Doe",
    "loan_date": "2025-11-30",
    "due_date": "2025-12-14"
}
```

**Response Sukses (201):**
```json
{
    "success": true,
    "message": "Peminjaman berhasil dibuat",
    "data": {
        "id": 1,
        "book_id": 1,
        "book_title": "Clean Code",
        "borrower_name": "John Doe",
        "loan_date": "2025-11-30",
        "due_date": "2025-12-14",
        "return_date": null,
        "status": "borrowed",
        "is_overdue": false,
        "created_at": "2025-11-30T10:30:00"
    }
}
```

**Response Error (400):**
```json
{
    "success": false,
    "message": "Validasi gagal",
    "errors": {
        "book_id": "Buku tidak tersedia (semua sedang dipinjam)"
    }
}
```

---

### 8. Kembalikan Buku

**Request:**
```
PUT http://localhost:5000/api/loans/1/return
Content-Type: application/json
```

**Body (opsional):**
```json
{
    "return_date": "2025-12-10"
}
```

**Response:**
```json
{
    "success": true,
    "message": "Buku berhasil dikembalikan",
    "data": {
        "id": 1,
        "book_id": 1,
        "book_title": "Clean Code",
        "borrower_name": "John Doe",
        "loan_date": "2025-11-30",
        "due_date": "2025-12-14",
        "return_date": "2025-12-10",
        "status": "returned",
        "is_overdue": false,
        "created_at": "2025-11-30T10:30:00"
    }
}
```

---

### 9. Lihat Statistik

**Request:**
```
GET http://localhost:5000/api/statistics
```

**Response:**
```json
{
    "success": true,
    "message": "Statistik berhasil diambil",
    "data": {
        "books": {
            "total": 10,
            "available": 7,
            "borrowed": 3,
            "categories_count": 4,
            "categories": ["Programming", "Fiction", "Science", "History"]
        },
        "loans": {
            "total_loans": 15,
            "active_loans": 3,
            "returned_loans": 12,
            "overdue_loans": 1
        }
    }
}
```

---

### 10. Update Peminjaman (Perpanjangan / Catatan)

**Request:**
```
PUT http://localhost:5000/api/loans/1
Content-Type: application/json
```

**Body (salah satu / keduanya):**
```json
{
    "due_date": "2025-12-20",
    "notes": "Diperpanjang karena kebutuhan riset"
}
```

**Response:**
```json
{
    "success": true,
    "message": "Peminjaman berhasil diupdate",
    "data": {
        "id": 1,
        "book_id": 1,
        "borrower_name": "John Doe",
        "loan_date": "2025-11-30",
        "due_date": "2025-12-20",
        "return_date": null,
        "status": "borrowed",
        "notes": "Diperpanjang karena kebutuhan riset"
    }
}
```

---

### 11. Hapus Peminjaman

**Request:**
```
DELETE http://localhost:5000/api/loans/1
```

**Response:**
```json
{
    "success": true,
    "message": "Peminjaman berhasil dihapus"
}
```
 
---

## 📁 Struktur Folder

```
P3/
├── app/
│   ├── __init__.py              # App factory
│   ├── config/
│   │   ├── __init__.py
│   │   └── config.py            # Konfigurasi
│   ├── database/
│   │   ├── __init__.py
│   │   └── connection.py        # [SINGLETON] DB connection
│   ├── models/
│   │   ├── __init__.py
│   │   ├── book.py              # Model Book
│   │   └── loan.py              # Model Loan
│   ├── factories/
│   │   ├── __init__.py
│   │   └── model_factory.py     # [FACTORY] Object creation
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── base_repository.py   # [ADAPTER] Interface
│   │   ├── book_repository.py   # Book data access
│   │   └── loan_repository.py   # Loan data access
│   ├── validators/
│   │   ├── __init__.py
│   │   ├── validation_strategy.py  # [STRATEGY] Interface
│   │   ├── book_validator.py    # Book validation
│   │   └── loan_validator.py    # Loan validation
│   ├── observers/
│   │   ├── __init__.py
│   │   ├── event_observer.py    # [OBSERVER] Interface
│   │   └── activity_logger.py   # Activity logging
│   ├── services/
│   │   ├── __init__.py
│   │   ├── book_service.py      # [FACADE] Book operations
│   │   ├── loan_service.py      # [FACADE] Loan operations
│   │   └── statistics_service.py
│   ├── controllers/
│   │   ├── __init__.py
│   │   ├── book_controller.py   # Book endpoints
│   │   ├── loan_controller.py   # Loan endpoints
│   │   └── statistics_controller.py
│   └── utils/
│       ├── __init__.py
│       └── response_helper.py
├── logs/
│   └── app.log                  # Activity logs
├── instance/
│   └── library.db               # SQLite database
├── .env                         # Environment config
├── .gitignore
├── requirements.txt
├── run.py                       # Entry point
├── README.md                    # Dokumentasi ini
├── SRS_Library_Management_API.md
├── DESIGN_DOCUMENT.md
└── DESIGN_PATTERNS_EXPLANATION.md
```

---

## 📝 Catatan

### HTTP Status Codes
- `200`: Success
- `201`: Created
- `400`: Bad Request (validation error)
- `404`: Not Found
- `500`: Internal Server Error

### Tips Penggunaan Postman
1. Set `Content-Type: application/json` untuk POST/PUT requests
2. Gunakan raw JSON body
3. Import collection dari file jika tersedia
4. Gunakan environment variables untuk base URL

---

## 📄 Lisensi

MIT License - Feel free to use and modify.

---

**Dibuat dengan ❤️ untuk pembelajaran Design Patterns dan Flask API**
