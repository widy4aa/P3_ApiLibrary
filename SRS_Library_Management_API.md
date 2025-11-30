# Software Requirements Specification (SRS)
# Library Book Management API

**Versi Dokumen:** 1.0  
**Tanggal:** 30 November 2025  
**Dibuat oleh:** System Architect Team

---

## 1. PENDAHULUAN

### 1.1 Tujuan Dokumen
Dokumen ini bertujuan untuk menjelaskan spesifikasi kebutuhan perangkat lunak (Software Requirements Specification) untuk sistem API manajemen buku perpustakaan (Library Book Management System). Dokumen ini ditujukan untuk pengembang, penguji, dan stakeholder terkait.

### 1.2 Tujuan Sistem
Library Book Management API adalah sistem berbasis REST API yang dirancang untuk:
- Mengelola data koleksi buku perpustakaan secara digital
- Memfasilitasi proses peminjaman dan pengembalian buku
- Menyediakan layanan pencarian dan filtering buku
- Memberikan laporan statistik perpustakaan
- Menyediakan interface API yang dapat diintegrasikan dengan berbagai client aplikasi

### 1.3 Ruang Lingkup
Sistem ini mencakup:
- **Manajemen Buku**: CRUD (Create, Read, Update, Delete) data buku
- **Peminjaman**: Sistem peminjaman buku oleh pengguna
- **Pengembalian**: Proses return buku yang dipinjam
- **Pencarian**: Fitur search dan filter buku berdasarkan kriteria
- **Statistik**: Dashboard data statistik perpustakaan
- **Logging**: Tracking aktivitas sistem

Batasan sistem:
- Tidak mencakup antarmuka pengguna (UI) front-end
- Tidak mencakup sistem pembayaran denda
- Tidak mencakup manajemen user authentication (simplified version)

### 1.4 Definisi, Akronim, dan Singkatan

| Istilah | Definisi |
|---------|----------|
| API | Application Programming Interface - Interface untuk komunikasi antar aplikasi |
| REST | Representational State Transfer - Arsitektur web service |
| CRUD | Create, Read, Update, Delete - Operasi dasar database |
| MVC | Model-View-Controller - Pola arsitektur aplikasi |
| JSON | JavaScript Object Notation - Format pertukaran data |
| HTTP | Hypertext Transfer Protocol - Protokol komunikasi web |
| ISBN | International Standard Book Number - Kode unik buku |
| DTO | Data Transfer Object - Objek untuk transfer data |
| ORM | Object-Relational Mapping - Teknik mapping objek ke database |

---

## 2. DESKRIPSI UMUM SISTEM

### 2.1 Perspektif Produk
Library Book Management API adalah sistem standalone yang menyediakan layanan backend untuk aplikasi perpustakaan. Sistem ini dirancang dengan arsitektur RESTful API yang dapat diakses oleh berbagai client (web, mobile, desktop) melalui protokol HTTP/HTTPS.

### 2.2 Fungsi Utama Produk
1. Manajemen data buku (tambah, edit, hapus, lihat)
2. Sistem peminjaman buku
3. Sistem pengembalian buku
4. Pencarian dan filtering buku
5. Statistik dan reporting

### 2.3 Karakteristik Pengguna
- **Administrator**: Mengelola data buku, monitoring sistem
- **API Consumer**: Aplikasi client yang mengkonsumsi API
- **Developer**: Pengembang yang mengintegrasikan sistem

### 2.4 Lingkungan Operasi
- **Platform**: Cross-platform (Windows, Linux, MacOS)
- **Runtime**: Python 3.8 atau lebih tinggi
- **Web Framework**: Flask 2.x
- **Database**: SQLite (development), dapat diganti PostgreSQL/MySQL (production)
- **Protocol**: HTTP/HTTPS
- **Data Format**: JSON

---

## 3. KEBUTUHAN FUNGSIONAL

### FR-01: Tambah Buku Baru
**Deskripsi**: Sistem harus dapat menambahkan data buku baru ke dalam koleksi perpustakaan.  
**Input**: Judul, penulis, ISBN, tahun terbit, kategori, jumlah stok  
**Proses**: Validasi data → Simpan ke database → Return response  
**Output**: Konfirmasi berhasil/gagal dengan detail buku  
**Priority**: High

### FR-02: Lihat Daftar Semua Buku
**Deskripsi**: Sistem harus dapat menampilkan daftar semua buku yang tersedia.  
**Input**: Query parameters (pagination, filter)  
**Proses**: Query database → Format data → Return list  
**Output**: Array JSON berisi data buku dengan pagination  
**Priority**: High

### FR-03: Lihat Detail Buku Spesifik
**Deskripsi**: Sistem harus dapat menampilkan detail buku berdasarkan ID.  
**Input**: Book ID  
**Proses**: Query database by ID → Return detail  
**Output**: JSON object detail buku  
**Priority**: High

### FR-04: Update Data Buku
**Deskripsi**: Sistem harus dapat mengupdate informasi buku yang sudah ada.  
**Input**: Book ID, field yang diupdate  
**Proses**: Validasi ID → Update database → Return updated data  
**Output**: Konfirmasi update dengan data terbaru  
**Priority**: High

### FR-05: Hapus Buku
**Deskripsi**: Sistem harus dapat menghapus buku dari sistem (soft delete).  
**Input**: Book ID  
**Proses**: Validasi ID → Tandai sebagai deleted → Update database  
**Output**: Konfirmasi penghapusan  
**Priority**: Medium

### FR-06: Pencarian Buku
**Deskripsi**: Sistem harus dapat mencari buku berdasarkan kata kunci.  
**Input**: Keyword (judul, penulis, kategori)  
**Proses**: Full-text search → Filter hasil → Return matches  
**Output**: List buku yang sesuai kriteria pencarian  
**Priority**: High

### FR-07: Pinjam Buku
**Deskripsi**: Sistem harus dapat memproses peminjaman buku.  
**Input**: Book ID, borrower name, tanggal pinjam  
**Proses**: Cek ketersediaan → Update stok → Create loan record  
**Output**: Konfirmasi peminjaman dengan loan ID  
**Priority**: High

### FR-08: Kembalikan Buku
**Deskripsi**: Sistem harus dapat memproses pengembalian buku.  
**Input**: Loan ID, tanggal kembali  
**Proses**: Validasi loan → Update stok → Update loan status  
**Output**: Konfirmasi pengembalian  
**Priority**: High

### FR-09: Lihat Riwayat Peminjaman
**Deskripsi**: Sistem harus dapat menampilkan riwayat peminjaman buku.  
**Input**: Filter parameters (status, date range)  
**Proses**: Query loan records → Format data  
**Output**: List riwayat peminjaman  
**Priority**: Medium

### FR-10: Statistik Perpustakaan
**Deskripsi**: Sistem harus dapat menampilkan statistik perpustakaan.  
**Input**: Date range (optional)  
**Proses**: Agregasi data → Calculate statistics  
**Output**: JSON berisi total buku, buku dipinjam, kategori populer, dll  
**Priority**: Medium

### FR-11: Filter Buku Berdasarkan Kategori
**Deskripsi**: Sistem harus dapat memfilter buku berdasarkan kategori.  
**Input**: Category name  
**Proses**: Query by category → Return filtered list  
**Output**: List buku dalam kategori tertentu  
**Priority**: Medium

### FR-12: Cek Ketersediaan Buku
**Deskripsi**: Sistem harus dapat mengecek apakah buku tersedia untuk dipinjam.  
**Input**: Book ID  
**Proses**: Query stok → Calculate available copies  
**Output**: Status ketersediaan (available/not available) dengan jumlah  
**Priority**: High

---

## 4. KEBUTUHAN NON-FUNGSIONAL

### NFR-01: Performance
- Response time API harus < 200ms untuk 95% request
- Sistem harus dapat menangani minimal 100 concurrent requests
- Database query optimization untuk operasi CRUD

### NFR-02: Reliability
- System uptime minimal 99% (excluding maintenance)
- Data consistency harus terjaga dalam semua operasi
- Automatic error recovery mechanism

### NFR-03: Scalability
- Arsitektur modular yang mudah di-scale
- Support untuk horizontal scaling
- Database dapat diganti dengan enterprise database (PostgreSQL, MySQL)

### NFR-04: Maintainability
- Kode terstruktur dengan arsitektur MVC
- Implementasi design patterns untuk code reusability
- Comprehensive code comments dalam Bahasa Indonesia
- Clear separation of concerns

### NFR-05: Security
- Input validation untuk semua endpoint
- SQL injection prevention melalui parameterized queries
- Error handling yang tidak expose sensitive information
- Data sanitization

### NFR-06: Usability
- RESTful API design yang konsisten
- Clear HTTP status codes
- Descriptive error messages
- Comprehensive API documentation

### NFR-07: Portability
- Cross-platform compatibility (Windows, Linux, MacOS)
- Minimal dependencies
- Environment-based configuration
- Docker support (future enhancement)

### NFR-08: Code Quality
- Minimal 6 design patterns implementation
- Clean code principles
- Modular architecture
- Testability

### NFR-09: Documentation
- Inline code comments
- API endpoint documentation
- Setup and deployment guide
- Design pattern explanation

### NFR-10: Data Integrity
- Foreign key constraints
- Data validation before persistence
- Transaction support for critical operations
- Soft delete implementation untuk audit trail

---

## 5. ARSITEKTUR SISTEM

### 5.1 Arsitektur MVC (Model-View-Controller)

```
┌─────────────────────────────────────────┐
│          CLIENT (Postman/App)           │
└────────────────┬────────────────────────┘
                 │ HTTP Request
                 ▼
┌─────────────────────────────────────────┐
│         CONTROLLER LAYER                │
│  (Routes, Request Handling, Validation) │
│  - BookController                       │
│  - LoanController                       │
│  - StatisticsController                 │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│         SERVICE LAYER (Facade)          │
│  (Business Logic, Design Patterns)      │
│  - BookService                          │
│  - LoanService                          │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│         MODEL LAYER                     │
│  (Data Models, Database Operations)     │
│  - Book Model                           │
│  - Loan Model                           │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│         DATABASE (SQLite)               │
└─────────────────────────────────────────┘
```

**Penjelasan Layers:**

- **Controller**: Menerima HTTP request, validasi input, memanggil service, return response
- **Service**: Business logic, orchestrasi operasi, implementasi design patterns
- **Model**: Representasi data, database operations, ORM mapping
- **Database**: Persistence layer (SQLite untuk development)

### 5.2 Design Patterns Implementation

#### Creational Patterns

**1. Singleton Pattern**
- **Komponen**: Database Connection Manager
- **Tujuan**: Memastikan hanya satu instance koneksi database
- **Lokasi**: `app/database/connection.py`

**2. Factory Method Pattern**
- **Komponen**: Model Object Factory
- **Tujuan**: Membuat instance model objects secara konsisten
- **Lokasi**: `app/factories/model_factory.py`

#### Structural Patterns

**3. Facade Pattern**
- **Komponen**: Service Layer
- **Tujuan**: Menyederhanakan interface untuk operasi kompleks
- **Lokasi**: `app/services/`

**4. Adapter Pattern**
- **Komponen**: Repository Adapter
- **Tujuan**: Abstraksi database operations, mudah switch database
- **Lokasi**: `app/repositories/`

#### Behavioral Patterns

**5. Observer Pattern**
- **Komponen**: Event Logger System
- **Tujuan**: Logging aktivitas sistem secara otomatis
- **Lokasi**: `app/observers/event_logger.py`

**6. Strategy Pattern**
- **Komponen**: Validation Strategy
- **Tujuan**: Berbagai strategi validasi input yang dapat ditukar
- **Lokasi**: `app/validators/validation_strategy.py`

---

## 6. DIAGRAM

### 6.1 Use Case Diagram

```
┌──────────────────────────────────────────────────────┐
│         Library Book Management System               │
│                                                       │
│  ┌─────────────┐                                     │
│  │   API       │                                     │
│  │  Consumer   │────────┐                           │
│  │  (Client)   │        │                           │
│  └─────────────┘        │                           │
│                         │                           │
│                         ├──► Tambah Buku            │
│                         │                           │
│                         ├──► Lihat Daftar Buku      │
│                         │                           │
│                         ├──► Update Buku            │
│                         │                           │
│                         ├──► Hapus Buku             │
│                         │                           │
│                         ├──► Pencarian Buku         │
│                         │                           │
│                         ├──► Pinjam Buku            │
│                         │                           │
│                         ├──► Kembalikan Buku        │
│                         │                           │
│                         ├──► Lihat Statistik        │
│                         │                           │
│                         └──► Cek Ketersediaan       │
│                                                       │
└──────────────────────────────────────────────────────┘
```

### 6.2 Class Diagram

```
┌─────────────────────────┐
│   DatabaseConnection    │  ← Singleton Pattern
│   (Singleton)           │
├─────────────────────────┤
│ - instance: DB          │
│ - connection: SQLAlchemy│
├─────────────────────────┤
│ + get_instance()        │
│ + get_connection()      │
└─────────────────────────┘

┌─────────────────────────┐
│   ModelFactory          │  ← Factory Pattern
├─────────────────────────┤
│ + create_book()         │
│ + create_loan()         │
└─────────────────────────┘
         │
         │ creates
         ▼
┌─────────────────────────┐       ┌─────────────────────────┐
│      Book (Model)       │       │     Loan (Model)        │
├─────────────────────────┤       ├─────────────────────────┤
│ - id: int               │       │ - id: int               │
│ - title: string         │       │ - book_id: int          │
│ - author: string        │◄──────│ - borrower_name: str    │
│ - isbn: string          │       │ - loan_date: date       │
│ - year: int             │       │ - return_date: date     │
│ - category: string      │       │ - status: string        │
│ - stock: int            │       └─────────────────────────┘
│ - available: int        │
│ - created_at: datetime  │
│ - is_deleted: bool      │
└─────────────────────────┘

┌─────────────────────────┐
│  IRepository (Interface)│  ← Adapter Pattern
├─────────────────────────┤
│ + find_all()            │
│ + find_by_id()          │
│ + save()                │
│ + update()              │
│ + delete()              │
└─────────────────────────┘
         ▲
         │ implements
         │
┌────────┴──────────┐
│                   │
│  BookRepository   │  LoanRepository
│                   │

┌─────────────────────────┐
│   BookService (Facade)  │  ← Facade Pattern
├─────────────────────────┤
│ - repository            │
│ - validator             │
│ - observer              │
├─────────────────────────┤
│ + get_all_books()       │
│ + get_book_by_id()      │
│ + create_book()         │
│ + update_book()         │
│ + delete_book()         │
│ + search_books()        │
└─────────────────────────┘

┌─────────────────────────┐
│  IValidationStrategy    │  ← Strategy Pattern
├─────────────────────────┤
│ + validate()            │
└─────────────────────────┘
         ▲
         │
┌────────┴──────────────┐
│                       │
│ BookValidationStrategy│  LoanValidationStrategy
│                       │

┌─────────────────────────┐
│   EventObserver         │  ← Observer Pattern
├─────────────────────────┤
│ + update()              │
└─────────────────────────┘
         ▲
         │
┌────────┴──────────────┐
│                       │
│  ActivityLogger       │  StatisticsObserver
│                       │

┌─────────────────────────┐
│   BookController        │
├─────────────────────────┤
│ - service: BookService  │
├─────────────────────────┤
│ + index()               │
│ + show()                │
│ + store()               │
│ + update()              │
│ + destroy()             │
└─────────────────────────┘
```

### 6.3 Entity Relationship Diagram (ERD)

```
┌─────────────────────────────────┐
│          BOOKS                  │
├─────────────────────────────────┤
│ PK  id (INTEGER)                │
│     title (VARCHAR)             │
│     author (VARCHAR)            │
│     isbn (VARCHAR) UNIQUE       │
│     year (INTEGER)              │
│     category (VARCHAR)          │
│     stock (INTEGER)             │
│     available (INTEGER)         │
│     created_at (DATETIME)       │
│     updated_at (DATETIME)       │
│     is_deleted (BOOLEAN)        │
└─────────────────────────────────┘
              │
              │ 1
              │
              │
              │ *
              ▼
┌─────────────────────────────────┐
│          LOANS                  │
├─────────────────────────────────┤
│ PK  id (INTEGER)                │
│ FK  book_id (INTEGER)           │
│     borrower_name (VARCHAR)     │
│     loan_date (DATE)            │
│     due_date (DATE)             │
│     return_date (DATE)          │
│     status (VARCHAR)            │
│       - 'active'                │
│       - 'returned'              │
│     created_at (DATETIME)       │
└─────────────────────────────────┘

Relationship: One Book can have Many Loans (1:N)
```

### 6.4 Workflow Request-Response API

```
CLIENT                CONTROLLER              SERVICE              REPOSITORY           DATABASE
  │                       │                      │                      │                   │
  │  POST /api/books      │                      │                      │                   │
  ├──────────────────────►│                      │                      │                   │
  │                       │                      │                      │                   │
  │                       │  1. Validate Input   │                      │                   │
  │                       │     (Strategy)       │                      │                   │
  │                       │                      │                      │                   │
  │                       │  2. Call Service     │                      │                   │
  │                       ├─────────────────────►│                      │                   │
  │                       │                      │                      │                   │
  │                       │                      │  3. Create Book      │                   │
  │                       │                      │     (Factory)        │                   │
  │                       │                      │                      │                   │
  │                       │                      │  4. Save to DB       │                   │
  │                       │                      ├─────────────────────►│                   │
  │                       │                      │                      │                   │
  │                       │                      │                      │  5. INSERT Query  │
  │                       │                      │                      ├──────────────────►│
  │                       │                      │                      │                   │
  │                       │                      │                      │  6. Return ID     │
  │                       │                      │                      │◄──────────────────┤
  │                       │                      │                      │                   │
  │                       │                      │  7. Notify Observers │                   │
  │                       │                      │     (Observer)       │                   │
  │                       │                      │                      │                   │
  │                       │  8. Return Result    │                      │                   │
  │                       │◄─────────────────────┤                      │                   │
  │                       │                      │                      │                   │
  │  9. JSON Response     │                      │                      │                   │
  │◄──────────────────────┤                      │                      │                   │
  │  201 Created          │                      │                      │                   │
  │                       │                      │                      │                   │
```

**Alur Detail:**
1. Client mengirim HTTP POST request dengan JSON body
2. Controller menerima request dan melakukan validasi (Strategy Pattern)
3. Controller memanggil Service layer (Facade Pattern)
4. Service menggunakan Factory untuk membuat object Book
5. Service memanggil Repository untuk menyimpan data
6. Repository menggunakan Adapter untuk akses database
7. Database menyimpan data dan return ID
8. Service memicu Observer untuk logging
9. Controller mengembalikan response JSON ke client

---

## 7. TEKNOLOGI DAN TOOLS

### 7.1 Backend
- **Framework**: Flask 2.3.x
- **ORM**: SQLAlchemy 2.x
- **Database**: SQLite (dev), PostgreSQL (production-ready)
- **Python Version**: 3.8+

### 7.2 Development Tools
- **API Testing**: Postman
- **Version Control**: Git
- **IDE**: VS Code, PyCharm
- **Virtual Environment**: venv

### 7.3 Dependencies
```
Flask==2.3.0
Flask-SQLAlchemy==3.0.0
Flask-CORS==4.0.0
python-dotenv==1.0.0
```

---

## 8. API ENDPOINT SPECIFICATION

### Base URL
```
http://localhost:5000/api
```

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /books | Mendapatkan semua buku |
| GET | /books/:id | Mendapatkan detail buku |
| POST | /books | Menambah buku baru |
| PUT | /books/:id | Update buku |
| DELETE | /books/:id | Hapus buku (soft delete) |
| GET | /books/search | Pencarian buku |
| GET | /books/category/:category | Filter by category |
| POST | /loans | Pinjam buku |
| PUT | /loans/:id/return | Kembalikan buku |
| GET | /loans | Lihat semua peminjaman |
| GET | /statistics | Statistik perpustakaan |

---

## 9. KESIMPULAN

Library Book Management API adalah sistem yang dirancang dengan arsitektur MVC yang solid dan implementasi 6 design patterns untuk memastikan:
- **Maintainability**: Kode mudah di-maintain
- **Scalability**: Mudah dikembangkan
- **Reusability**: Komponen dapat digunakan ulang
- **Testability**: Mudah diuji
- **Best Practices**: Mengikuti standar industri

Sistem ini siap diimplementasikan dan dapat digunakan sebagai backend untuk berbagai aplikasi perpustakaan.

---

**Dokumen ini merupakan spesifikasi teknis lengkap untuk pengembangan Library Book Management API.**
