# Dokumen Perancangan Aplikasi
# Library Book Management API

---

## 1. STRUKTUR FOLDER (MVC Architecture)

```
P3/
│
├── app/
│   ├── __init__.py                      # Inisialisasi Flask app
│   │
│   ├── config/
│   │   ├── __init__.py
│   │   └── config.py                    # Konfigurasi aplikasi
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   └── connection.py                # Singleton: Database Connection
│   │
│   ├── models/                          # MODEL Layer
│   │   ├── __init__.py
│   │   ├── book.py                      # Model Book
│   │   └── loan.py                      # Model Loan
│   │
│   ├── factories/                       # Creational Pattern: Factory
│   │   ├── __init__.py
│   │   └── model_factory.py             # Factory untuk membuat model objects
│   │
│   ├── repositories/                    # Structural Pattern: Adapter
│   │   ├── __init__.py
│   │   ├── base_repository.py           # Interface Repository
│   │   ├── book_repository.py           # Book Repository Adapter
│   │   └── loan_repository.py           # Loan Repository Adapter
│   │
│   ├── validators/                      # Behavioral Pattern: Strategy
│   │   ├── __init__.py
│   │   ├── validation_strategy.py       # Strategy Interface
│   │   ├── book_validator.py            # Book Validation Strategy
│   │   └── loan_validator.py            # Loan Validation Strategy
│   │
│   ├── observers/                       # Behavioral Pattern: Observer
│   │   ├── __init__.py
│   │   ├── event_observer.py            # Observer Interface
│   │   └── activity_logger.py           # Concrete Observer untuk logging
│   │
│   ├── services/                        # Structural Pattern: Facade
│   │   ├── __init__.py
│   │   ├── book_service.py              # Facade untuk Book operations
│   │   ├── loan_service.py              # Facade untuk Loan operations
│   │   └── statistics_service.py        # Service untuk statistik
│   │
│   ├── controllers/                     # CONTROLLER Layer
│   │   ├── __init__.py
│   │   ├── book_controller.py           # Book API endpoints
│   │   ├── loan_controller.py           # Loan API endpoints
│   │   └── statistics_controller.py     # Statistics endpoints
│   │
│   └── utils/
│       ├── __init__.py
│       └── response_helper.py           # Helper untuk format response
│
├── logs/
│   └── app.log                          # File log aktivitas
│
├── instance/                            # (Optional) SQLite file for local quick dev; production uses PostgreSQL
│   └── library.db                       # Legacy/dev-only SQLite database
│
├── tests/                               # Unit tests (optional)
│   ├── __init__.py
│   └── test_api.py
│
├── .env                                 # Environment variables
├── .gitignore
├── requirements.txt                     # Python dependencies
├── run.py                               # Entry point aplikasi
├── README.md                            # Dokumentasi utama
├── SRS_Library_Management_API.md        # Dokumen SRS
├── DESIGN_DOCUMENT.md                   # Dokumen ini
└── DESIGN_PATTERNS_EXPLANATION.md       # Penjelasan design patterns
```

---

## 2. PENJELASAN STRUKTUR

### 2.1 Root Directory
- **run.py**: File utama untuk menjalankan aplikasi Flask
- **requirements.txt**: Daftar dependencies Python
- **.env**: Konfigurasi environment (database URI, secret key, dll)
- **README.md**: Dokumentasi cara instalasi dan penggunaan

### 2.2 app/ Directory
Direktori utama aplikasi yang berisi semua komponen

#### config/
- **config.py**: Konfigurasi Flask (database, secret key, CORS, dll)

#### database/
- **connection.py**: **[SINGLETON PATTERN]** - Mengelola single instance database connection

#### models/ (MODEL)
- **book.py**: Model/Entity untuk tabel Books
- **loan.py**: Model/Entity untuk tabel Loans
- Representasi struktur data dan database schema

#### factories/ (CREATIONAL)
- **model_factory.py**: **[FACTORY METHOD PATTERN]** - Factory untuk membuat instance model objects secara konsisten

#### repositories/ (STRUCTURAL - ADAPTER)
- **base_repository.py**: Interface repository (abstract class)
- **book_repository.py**: **[ADAPTER PATTERN]** - Adapter untuk operasi database Book
- **loan_repository.py**: **[ADAPTER PATTERN]** - Adapter untuk operasi database Loan
- Abstraksi layer database agar mudah diganti

#### validators/ (BEHAVIORAL - STRATEGY)
- **validation_strategy.py**: Interface validation strategy
- **book_validator.py**: **[STRATEGY PATTERN]** - Strategi validasi untuk Book
- **loan_validator.py**: **[STRATEGY PATTERN]** - Strategi validasi untuk Loan
- Memungkinkan berbagai strategi validasi yang dapat ditukar

#### observers/ (BEHAVIORAL - OBSERVER)
- **event_observer.py**: Interface observer
- **activity_logger.py**: **[OBSERVER PATTERN]** - Observer yang log semua aktivitas
- Auto-logging setiap ada event (create, update, delete)

#### services/ (STRUCTURAL - FACADE)
- **book_service.py**: **[FACADE PATTERN]** - Facade untuk business logic Book
- **loan_service.py**: **[FACADE PATTERN]** - Facade untuk business logic Loan
- **statistics_service.py**: Service untuk kalkulasi statistik
- Menyederhanakan interface kompleks, orchestrate multiple operations

#### controllers/ (CONTROLLER)
- **book_controller.py**: REST API endpoints untuk Book
- **loan_controller.py**: REST API endpoints untuk Loan
- **statistics_controller.py**: REST API endpoints untuk Statistics
- Menangani HTTP request/response, routing

#### utils/
- **response_helper.py**: Helper functions untuk standarisasi response JSON

---

## 3. MAPPING DESIGN PATTERNS

| Design Pattern | Lokasi File | Komponen | Tujuan |
|----------------|-------------|----------|--------|
| **Singleton** | `database/connection.py` | DatabaseConnection | Satu instance koneksi DB |
| **Factory Method** | `factories/model_factory.py` | ModelFactory | Konsisten membuat objects |
| **Adapter** | `repositories/*.py` | Repository classes | Abstraksi database ops |
| **Facade** | `services/*.py` | Service classes | Simplifikasi business logic |
| **Strategy** | `validators/*.py` | Validation strategies | Validasi yang fleksibel |
| **Observer** | `observers/*.py` | ActivityLogger | Auto-logging events |

---

## 4. SEQUENCE DIAGRAM - POST /api/books

```
┌────────┐      ┌──────────────┐      ┌─────────────┐      ┌──────────────┐      ┌────────────┐      ┌──────────┐
│ Client │      │BookController│      │BookValidator│      │ BookService  │      │BookFactory │      │BookRepo  │
└───┬────┘      └──────┬───────┘      └──────┬──────┘      └──────┬───────┘      └─────┬──────┘      └────┬─────┘
    │                  │                     │                    │                    │                  │
    │ POST /api/books  │                     │                    │                    │                  │
    ├─────────────────►│                     │                    │                    │                  │
    │                  │                     │                    │                    │                  │
    │                  │  validate(data)     │                    │                    │                  │
    │                  ├────────────────────►│                    │                    │                  │
    │                  │                     │                    │                    │                  │
    │                  │  validation_result  │                    │                    │                  │
    │                  │◄────────────────────┤                    │                    │                  │
    │                  │                     │                    │                    │                  │
    │                  │  create_book(data)  │                    │                    │                  │
    │                  ├─────────────────────┼───────────────────►│                    │                  │
    │                  │                     │                    │                    │                  │
    │                  │                     │                    │  create_book(data) │                  │
    │                  │                     │                    ├───────────────────►│                  │
    │                  │                     │                    │                    │                  │
    │                  │                     │                    │   Book object      │                  │
    │                  │                     │                    │◄───────────────────┤                  │
    │                  │                     │                    │                    │                  │
    │                  │                     │                    │  save(book_obj)    │                  │
    │                  │                     │                    ├───────────────────────────────────────►│
    │                  │                     │                    │                    │                  │
    │                  │                     │                    │                    │    db.add()      │
    │                  │                     │                    │                    │    db.commit()   │
    │                  │                     │                    │                    │                  │
    │                  │                     │                    │   saved_book       │                  │
    │                  │                     │                    │◄───────────────────────────────────────┤
    │                  │                     │                    │                    │                  │
    │                  │                     │    notify_observers(event)              │                  │
    │                  │                     │                    │                    │                  │
    │                  │                     │          [ActivityLogger logs event]     │                  │
    │                  │                     │                    │                    │                  │
    │                  │   return book_data  │                    │                    │                  │
    │                  │◄────────────────────┼────────────────────┤                    │                  │
    │                  │                     │                    │                    │                  │
    │  201 Created     │                     │                    │                    │                  │
    │  + JSON response │                     │                    │                    │                  │
    │◄─────────────────┤                     │                    │                    │                  │
    │                  │                     │                    │                    │                  │
```

**Keterangan:**
1. Client POST request dengan JSON body
2. Controller terima request
3. Controller panggil **Strategy** (BookValidator) untuk validasi
4. Controller panggil **Facade** (BookService)
5. Service panggil **Factory** untuk create Book object
6. Service panggil **Adapter** (BookRepository) untuk save
7. Repository simpan ke database via Singleton connection
8. Service trigger **Observer** (ActivityLogger)
9. Return response ke client

---

## 5. DATA FLOW ARCHITECTURE

```
┌───────────────────────────────────────────────────────────────┐
│                      HTTP REQUEST                             │
│              (JSON Body, Headers, Method)                     │
└───────────────────────┬───────────────────────────────────────┘
                        │
                        ▼
        ┌───────────────────────────────┐
        │      CONTROLLER LAYER         │
        │  ┌─────────────────────────┐  │
        │  │  1. Parse Request       │  │
        │  │  2. Validate (Strategy) │  │ ◄── Strategy Pattern
        │  │  3. Call Service        │  │
        │  └─────────────────────────┘  │
        └───────────────┬───────────────┘
                        │
                        ▼
        ┌───────────────────────────────┐
        │      SERVICE LAYER (Facade)   │
        │  ┌─────────────────────────┐  │
        │  │  1. Business Logic      │  │ ◄── Facade Pattern
        │  │  2. Use Factory         │  │ ◄── Factory Pattern
        │  │  3. Call Repository     │  │
        │  │  4. Trigger Observers   │  │ ◄── Observer Pattern
        │  └─────────────────────────┘  │
        └───────────────┬───────────────┘
                        │
                        ▼
        ┌───────────────────────────────┐
        │   REPOSITORY LAYER (Adapter)  │
        │  ┌─────────────────────────┐  │
        │  │  1. Abstract DB Ops     │  │ ◄── Adapter Pattern
        │  │  2. Query Builder       │  │
        │  │  3. Use Singleton DB    │  │ ◄── Singleton Pattern
        │  └─────────────────────────┘  │
        └───────────────┬───────────────┘
                        │
                        ▼
        ┌───────────────────────────────┐
        │   DATABASE (PostgreSQL)       │
        │ Connected via Singleton (SQLAlchemy) │
        └───────────────────────────────┘
                        │
                        ▼
        ┌───────────────────────────────┐
        │      RESPONSE FORMATION       │
        │   (JSON, HTTP Status Code)    │
        └───────────────────────────────┘
```

---

## 6. DATABASE SCHEMA DETAIL (PostgreSQL)

Skema aktual berjalan di PostgreSQL (bukan lagi SQLite). Contoh DDL berikut selaras dengan model saat ini.

### Table: books
```sql
CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    author VARCHAR(100) NOT NULL,
    isbn VARCHAR(20) UNIQUE NOT NULL,
    year INT NOT NULL,
    category VARCHAR(50) NOT NULL,
    stock INT NOT NULL DEFAULT 0,
    available INT NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_deleted BOOLEAN DEFAULT FALSE
);

-- Indexes
CREATE INDEX idx_books_isbn ON books(isbn);
CREATE INDEX idx_books_category ON books(category);
CREATE INDEX idx_books_title ON books(title);
```

### Table: loans
```sql
CREATE TABLE loans (
    id SERIAL PRIMARY KEY,
    book_id INT NOT NULL REFERENCES books(id),
    borrower_name VARCHAR(100) NOT NULL,
    loan_date DATE NOT NULL,
    due_date DATE NOT NULL,
    return_date DATE,
    status VARCHAR(20) NOT NULL DEFAULT 'borrowed' CHECK (status IN ('borrowed','returned','overdue')),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_loans_book_id ON loans(book_id);
CREATE INDEX idx_loans_status ON loans(status);
CREATE INDEX idx_loans_borrower ON loans(borrower_name);
CREATE INDEX idx_loans_due_date ON loans(due_date);
```

---

## 7. API REQUEST/RESPONSE EXAMPLES

### Tambah Buku - POST /api/books

**Request:**
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

**Response (201 Created):**
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
        "created_at": "2025-11-30T10:30:00"
    }
}
```

### Pinjam Buku - POST /api/loans

**Request:**
```json
{
    "book_id": 1,
    "borrower_name": "John Doe",
    "loan_date": "2025-11-30",
    "due_date": "2025-12-14"
}
```

**Response (201 Created):**
```json
{
    "success": true,
    "message": "Buku berhasil dipinjam",
    "data": {
        "loan_id": 1,
        "book_id": 1,
        "book_title": "Clean Code",
        "borrower_name": "John Doe",
        "loan_date": "2025-11-30",
        "due_date": "2025-12-14",
        "status": "active"
    }
}
```

### Error Response (400 Bad Request)
```json
{
    "success": false,
    "message": "Validation error",
    "errors": {
        "isbn": "ISBN sudah terdaftar",
        "year": "Tahun harus antara 1000-2100"
    }
}
```

---

## 8. DESIGN DECISIONS

### 8.1 Mengapa PostgreSQL untuk Production (SQLite opsional untuk dev)?
- PostgreSQL: kuat, mendukung concurrency, indexing lanjutan, integritas referensial kuat
- Skalabilitas & ekstensi (JSONB, Full Text Search) siap untuk fitur lanjutan
- SQLite tetap bisa dipakai lokal untuk eksperimen cepat, tetapi bukan target deployment

### 8.2 Mengapa MVC?
- Separation of concerns yang jelas
- Mudah testing masing-masing layer
- Scalable dan maintainable
- Industry standard

### 8.3 Mengapa 6 Design Patterns?
- **Singleton**: Satu sumber kebenaran untuk session DB SQLAlchemy
- **Factory**: Konsisten & terpusat membuat entity (Book/Loan)
- **Adapter**: Isolasi akses DB → mudah ganti/memperluas storage layer
- **Facade**: Controller cukup memanggil satu metode; orkestrasi kompleks disembunyikan
- **Strategy**: Validasi entity fleksibel & dapat diganti tanpa ubah service
- **Observer**: Logging/event handling terlepas dari business logic utama

### 8.4 Soft Delete vs Hard Delete
- Menggunakan soft delete (flag `is_deleted`)
- Alasan: Audit trail, data recovery, compliance

---

## 9. CLASS DIAGRAM (Simplified Relationships)

```
┌──────────────┐      1    ┌──────────────┐
│    Book      │──────────►│     Loan     │
├──────────────┤           ├──────────────┤
│ id           │           │ id           │
│ title        │           │ book_id (FK) │
│ author       │           │ borrower_name│
│ isbn         │           │ loan_date    │
│ year         │           │ due_date     │
│ category     │           │ return_date  │
│ stock        │           │ status       │
│ available    │           │ notes        │
└──────────────┘           └──────────────┘
    ▲                            ▲
    │ uses                       │ uses
    │                            │
┌──────────────┐  Facade   ┌────────────────┐
│ BookService  │◄────────►│ LoanService    │
└──────────────┘           └────────────────┘
    ▲                            ▲
    │ Adapter                    │ Adapter
    │                            │
┌──────────────┐           ┌──────────────┐
│BookRepository│           │LoanRepository│
└──────────────┘           └──────────────┘
    ▲                            ▲
    │ Factory                    │ Factory
    │                            │
     ┌────────────────────────────────┐
     │        ModelFactory            │
     └────────────────────────────────┘
    ▲                            ▲
    │ Strategy                   │ Strategy
    │                            │
┌──────────────┐           ┌──────────────┐
│BookValidator │           │LoanValidator │
└──────────────┘           └──────────────┘
    ▲                            ▲
    │ Observer notify            │ Observer notify
    └──────────────┬─────────────┘
             ▼
          ┌──────────────┐
          │ActivityLogger│
          └──────────────┘
```

## 10. SECURITY CONSIDERATIONS

1. **Input Validation**: Semua input divalidasi sebelum diproses
2. **SQL Injection Prevention**: Menggunakan SQLAlchemy ORM (parameterized queries)
3. **Error Handling**: Error messages tidak expose sensitive info
4. **CORS**: Dikonfigurasi sesuai kebutuhan
5. **Data Sanitization**: Semua input di-sanitize

---

## 11. SCALABILITY PLANNING

### Horizontal Scaling
- Stateless API design
- Database connection pooling
- Load balancer ready

### Vertical Scaling
- Efficient query optimization
- Indexing strategy
- Caching layer (future: Redis)

### Future Enhancements
- Authentication & Authorization (JWT)
- Rate limiting
- API versioning
- Caching layer
- Message queue untuk async tasks
- Containerization (Docker)
- CI/CD pipeline

---

## 12. IMPLEMENTATION SUMMARY (Assignment Mapping)

1. Rancang (Design): Class diagram & sequence diagram menunjukkan relasi & alur. Patterns ditempatkan pada layer yang memaksimalkan loose coupling.
2. Implementasi: Controllers memanggil Facade Services → Services orkestrasi Strategy (validasi), Factory (pembuatan objek), Adapter (persistensi), Observer (event logging) melalui Singleton DB.
3. Penjelasan: Masing-masing pattern dibahas di `DESIGN_PATTERNS_EXPLANATION.md` (intent, participants, manfaat) memastikan 2 Creational (Singleton, Factory), 2 Structural (Adapter, Facade), 2 Behavioral (Strategy, Observer).

**Dokumen ini merupakan blueprint lengkap untuk implementasi aplikasi (versi PostgreSQL).**
