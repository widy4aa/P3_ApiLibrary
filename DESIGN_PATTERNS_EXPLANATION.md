# Penjelasan Implementasi Design Patterns

Dokumen ini menjelaskan secara detail implementasi 6 Design Patterns dalam aplikasi Library Book Management API.

---

## Daftar Design Patterns

| No | Pattern | Kategori | File | Tujuan |
|----|---------|----------|------|--------|
| 1 | Singleton | Creational | `database/connection.py` | Single database connection |
| 2 | Factory Method | Creational | `factories/model_factory.py` | Consistent object creation |
| 3 | Adapter | Structural | `repositories/*.py` | Database abstraction |
| 4 | Facade | Structural | `services/*.py` | Simplified interface |
| 5 | Strategy | Behavioral | `validators/*.py` | Flexible validation |
| 6 | Observer | Behavioral | `observers/*.py` | Event-driven logging |

---

## 1. SINGLETON PATTERN (Creational)

### Lokasi File
`app/database/connection.py`

### Tujuan
Memastikan hanya ada **SATU instance** koneksi database di seluruh aplikasi. Ini menghemat resource dan mencegah masalah multiple database connections.

### Diagram

```
┌──────────────────────────────────────┐
│        DatabaseConnection            │
│         (Singleton)                  │
├──────────────────────────────────────┤
│ - _instance: DatabaseConnection      │  ← Private class variable
│ - _lock: Lock                        │  ← Thread safety
│ - db: SQLAlchemy                     │
├──────────────────────────────────────┤
│ + __new__(): DatabaseConnection      │  ← Returns same instance
│ + get_db(): SQLAlchemy               │
│ + init_app(app)                      │
│ + create_tables(app)                 │
└──────────────────────────────────────┘
         │
         │ returns same instance
         ▼
    ┌─────────┐
    │   db    │ ← Single SQLAlchemy instance
    └─────────┘
```

### Implementasi Kode

```python
class DatabaseConnection:
    _instance = None  # Private: menyimpan singleton instance
    _lock = Lock()    # Thread safety
    
    def __new__(cls):
        """
        Override __new__ untuk implementasi Singleton
        Double-checked locking untuk thread safety
        """
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance.db = SQLAlchemy()
        return cls._instance
    
    def get_db(self):
        return self.db

# Penggunaan:
db_connection = DatabaseConnection()  # Selalu return instance yang sama
db = db_connection.get_db()
```

### Cara Kerja

1. Pertama kali `DatabaseConnection()` dipanggil, instance baru dibuat
2. Instance disimpan di `_instance` class variable
3. Pemanggilan berikutnya mengembalikan instance yang sama
4. `Lock()` memastikan thread-safe di environment multi-threaded

### Manfaat

- ✅ Hemat memory dan resource
- ✅ Konsistensi koneksi database
- ✅ Mencegah connection pool exhaustion
- ✅ Centralized database management

---

## 2. FACTORY METHOD PATTERN (Creational)

### Lokasi File
`app/factories/model_factory.py`

### Tujuan
Menyediakan **interface terpusat** untuk membuat object Model (Book, Loan). Ini memastikan konsistensi dalam pembuatan object dan memudahkan perubahan logic creation di satu tempat.

### Diagram

```
┌──────────────────────────────────────┐
│           ModelFactory               │
├──────────────────────────────────────┤
│ + create_book(data): Book            │
│ + create_loan(data): Loan            │
│ + update_book(book, data): Book      │
└──────────────────────────────────────┘
         │                  │
         │ creates          │ creates
         ▼                  ▼
    ┌─────────┐        ┌─────────┐
    │  Book   │        │  Loan   │
    └─────────┘        └─────────┘
```

### Implementasi Kode

```python
class ModelFactory:
    
    @staticmethod
    def create_book(data):
        """
        Factory method untuk membuat Book object
        """
        # Extract dan validate data
        title = data.get('title', '').strip()
        author = data.get('author', '').strip()
        isbn = data.get('isbn', '').strip()
        year = int(data.get('year', 0))
        category = data.get('category', '').strip()
        stock = int(data.get('stock', 0))
        
        # Basic validation
        if not all([title, author, isbn, category]):
            raise ValueError("Semua field wajib diisi")
        
        # Create dan return Book instance
        return Book(
            title=title,
            author=author,
            isbn=isbn,
            year=year,
            category=category,
            stock=stock
        )
    
    @staticmethod
    def create_loan(data):
        """
        Factory method untuk membuat Loan object
        """
        book_id = int(data.get('book_id', 0))
        borrower_name = data.get('borrower_name', '').strip()
        loan_date = datetime.strptime(data['loan_date'], '%Y-%m-%d').date()
        
        return Loan(
            book_id=book_id,
            borrower_name=borrower_name,
            loan_date=loan_date
        )

# Penggunaan:
book = model_factory.create_book({
    'title': 'Clean Code',
    'author': 'Robert Martin',
    ...
})
```

### Cara Kerja

1. Client memanggil `create_book(data)` dengan dictionary data
2. Factory melakukan pre-processing (strip, conversion)
3. Factory melakukan basic validation
4. Factory membuat dan mengembalikan object Book/Loan

### Manfaat

- ✅ Konsistensi pembuatan object
- ✅ Centralized creation logic
- ✅ Mudah menambah validation/transformation
- ✅ Single point of change

---

## 3. ADAPTER PATTERN (Structural)

### Lokasi File
- `app/repositories/base_repository.py` (Interface)
- `app/repositories/book_repository.py`
- `app/repositories/loan_repository.py`

### Tujuan
**Mengabstraksi operasi database** sehingga business logic tidak bergantung pada implementasi database spesifik. Ini memudahkan pergantian database (SQLite → PostgreSQL → MongoDB) tanpa mengubah kode di layer lain.

### Diagram

```
┌────────────────────────────────────────────────────────┐
│                  BaseRepository                        │
│                   (Interface)                          │
├────────────────────────────────────────────────────────┤
│ + find_all(filters) : List                             │
│ + find_by_id(id) : Model                               │
│ + save(entity) : Model                                 │
│ + update(entity) : Model                               │
│ + delete(id) : bool                                    │
│ + count(filters) : int                                 │
└────────────────────────────────────────────────────────┘
                    ▲                    ▲
                    │                    │
         implements │                    │ implements
                    │                    │
    ┌───────────────┴──┐        ┌───────┴───────────┐
    │  BookRepository  │        │  LoanRepository   │
    │   (SQLAlchemy)   │        │   (SQLAlchemy)    │
    └──────────────────┘        └───────────────────┘
            │                           │
            │                           │
            ▼                           ▼
    ┌──────────────────────────────────────────────┐
    │            PostgreSQL Database                │
    │     (awalnya SQLite untuk dev cepat)          │
    └──────────────────────────────────────────────┘
```

### Implementasi Kode

```python
# Interface (Abstract Base Class)
class BaseRepository(ABC):
    
    @abstractmethod
    def find_all(self, filters=None):
        pass
    
    @abstractmethod
    def find_by_id(self, id):
        pass
    
    @abstractmethod
    def save(self, entity):
        pass
    
    @abstractmethod
    def update(self, entity):
        pass
    
    @abstractmethod
    def delete(self, id):
        pass


# Concrete Adapter untuk SQLAlchemy
class BookRepository(BaseRepository):
    
    def find_all(self, filters=None):
        query = Book.query.filter_by(is_deleted=False)
        
        if filters and 'category' in filters:
            query = query.filter(Book.category.ilike(f"%{filters['category']}%"))
        
        return query.all()
    
    def find_by_id(self, id):
        return Book.query.filter_by(id=id, is_deleted=False).first()
    
    def save(self, book):
        db.session.add(book)
        db.session.commit()
        return book
    
    def update(self, book):
        db.session.commit()
        return book
    
    def delete(self, id):
        book = self.find_by_id(id)
        if book:
            book.is_deleted = True  # Soft delete
            db.session.commit()
            return True
        return False

# Penggunaan di Service:
class BookService:
    def __init__(self):
        self.repository = book_repository  # Adapter
    
    def get_all_books(self):
        return self.repository.find_all()  # Tidak peduli implementasi
```

### Cara Kerja

1. `BaseRepository` mendefinisikan interface standar
2. `BookRepository` mengadaptasi SQLAlchemy ke interface tersebut
3. Service layer menggunakan interface, bukan implementasi konkret
4. Jika ganti database, cukup buat adapter baru

### Manfaat

- ✅ Database-agnostic business logic
- ✅ Mudah switch database
- ✅ Testable (bisa mock repository)
- ✅ Separation of concerns

---

## 4. FACADE PATTERN (Structural)

### Lokasi File
- `app/services/book_service.py`
- `app/services/loan_service.py`
- `app/services/statistics_service.py`

### Tujuan
**Menyederhanakan interface** untuk subsystem yang kompleks. Service layer menyembunyikan kompleksitas interaksi antara Repository, Factory, Validator, dan Observer dari Controller.

### Diagram

```
┌──────────────────────────────────────────────────────────────────┐
│                         BookService                               │
│                          (FACADE)                                 │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Controller hanya perlu memanggil:                               │
│  - get_all_books()                                               │
│  - create_book(data)                                             │
│  - update_book(id, data)                                         │
│  - delete_book(id)                                               │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
         │              │              │              │
         │              │              │              │
         ▼              ▼              ▼              ▼
    ┌─────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
    │Validator│   │ Factory  │   │Repository│   │ Observer │
    │(Strategy)   │          │   │ (Adapter)│   │          │
    └─────────┘   └──────────┘   └──────────┘   └──────────┘
```

### Implementasi Kode

```python
class BookService:
    """
    FACADE untuk operasi Book
    Menyembunyikan kompleksitas dari Controller
    """
    
    def __init__(self):
        self.repository = book_repository    # Adapter
        self.factory = model_factory         # Factory
        self.validator = book_validator      # Strategy
        self.event_subject = event_subject   # Observer
    
    def create_book(self, data):
        """
        Facade method - menyederhanakan proses kompleks:
        1. Validasi → 2. Create object → 3. Save → 4. Notify
        """
        try:
            # Step 1: Validasi menggunakan Strategy Pattern
            is_valid, errors = self.validator.validate(data)
            if not is_valid:
                return {'success': False, 'errors': errors}
            
            # Step 2: Create menggunakan Factory Pattern
            book = self.factory.create_book(data)
            
            # Step 3: Simpan menggunakan Repository Adapter
            saved_book = self.repository.save(book)
            
            # Step 4: Notify Observers
            self.event_subject.notify(EventType.BOOK_CREATED, 
                                      {'book': saved_book.to_dict()})
            
            return {'success': True, 'data': saved_book.to_dict()}
            
        except Exception as e:
            return {'success': False, 'message': str(e)}

# Di Controller - sangat sederhana:
@book_bp.route('', methods=['POST'])
def create_book():
    data = request.get_json()
    result = book_service.create_book(data)  # Facade call
    return jsonify(result), 201 if result['success'] else 400
```

### Cara Kerja

1. Controller memanggil satu method di Service
2. Service orchestrate multiple subsystems:
   - Validator untuk validasi
   - Factory untuk object creation
   - Repository untuk database
   - Observer untuk logging
3. Controller tidak perlu tahu detail internal

### Manfaat

- ✅ Simplified interface
- ✅ Reduced coupling
- ✅ Centralized business logic
- ✅ Easier to test dan maintain

---

## 5. STRATEGY PATTERN (Behavioral)

### Lokasi File
- `app/validators/validation_strategy.py` (Interface)
- `app/validators/book_validator.py`
- `app/validators/loan_validator.py`

### Tujuan
Mendefinisikan **keluarga algoritma validasi** yang dapat dipertukarkan. Setiap entity (Book, Loan) memiliki strategi validasi sendiri yang dapat diganti tanpa mengubah client code.

### Diagram

```
┌──────────────────────────────────────────────────────┐
│             ValidationStrategy                        │
│               (Interface)                             │
├──────────────────────────────────────────────────────┤
│ + validate(data) : (bool, dict)                      │
│ # _check_required_fields(data, fields) : dict        │
│ # _check_string_length(value, name, min, max) : str  │
└──────────────────────────────────────────────────────┘
                    ▲                    ▲
                    │                    │
         implements │                    │ implements
                    │                    │
    ┌───────────────┴──────┐    ┌───────┴────────────────┐
    │ BookValidationStrategy│    │ LoanValidationStrategy │
    ├──────────────────────┤    ├────────────────────────┤
    │ - validate ISBN      │    │ - validate book_id     │
    │ - validate year      │    │ - validate dates       │
    │ - validate stock     │    │ - validate duration    │
    └──────────────────────┘    └────────────────────────┘
```

### Implementasi Kode

```python
# Interface Strategy
class ValidationStrategy(ABC):
    
    @abstractmethod
    def validate(self, data):
        """
        Returns: (is_valid: bool, errors: dict)
        """
        pass
    
    def _check_required_fields(self, data, required_fields):
        errors = {}
        for field in required_fields:
            if field not in data or not data[field]:
                errors[field] = f'{field} wajib diisi'
        return errors


# Concrete Strategy untuk Book
class BookValidationStrategy(ValidationStrategy):
    
    REQUIRED_FIELDS = ['title', 'author', 'isbn', 'year', 'category', 'stock']
    
    def validate(self, data, is_update=False):
        errors = {}
        
        if not is_update:
            errors.update(self._check_required_fields(data, self.REQUIRED_FIELDS))
        
        # Validasi spesifik Book
        if 'isbn' in data:
            isbn_error = self._validate_isbn(data['isbn'], data.get('id'))
            if isbn_error:
                errors['isbn'] = isbn_error
        
        if 'year' in data:
            year_error = self._validate_year(data['year'])
            if year_error:
                errors['year'] = year_error
        
        return (len(errors) == 0, errors)
    
    def _validate_isbn(self, isbn, book_id=None):
        existing = book_repository.find_by_isbn(isbn)
        if existing and (book_id is None or existing.id != book_id):
            return 'ISBN sudah terdaftar'
        return None
    
    def _validate_year(self, year):
        if int(year) > datetime.now().year + 1:
            return 'Tahun tidak valid'
        return None


# Concrete Strategy untuk Loan
class LoanValidationStrategy(ValidationStrategy):
    
    def validate(self, data):
        errors = {}
        
        # Cek ketersediaan buku
        book = book_repository.find_by_id(data.get('book_id'))
        if not book:
            errors['book_id'] = 'Buku tidak ditemukan'
        elif book.available <= 0:
            errors['book_id'] = 'Buku tidak tersedia'
        
        return (len(errors) == 0, errors)


# Penggunaan - Strategy bisa diganti:
class BookService:
    def __init__(self, validator=None):
        self.validator = validator or book_validator
    
    def create_book(self, data):
        is_valid, errors = self.validator.validate(data)
        # ...
```

### Cara Kerja

1. `ValidationStrategy` mendefinisikan interface `validate()`
2. Setiap entity punya Concrete Strategy dengan rules sendiri
3. Service menggunakan interface, tidak hardcode strategy
4. Strategy bisa diganti runtime jika diperlukan

### Manfaat

- ✅ Open/Closed Principle - mudah tambah validator baru
- ✅ Single Responsibility - setiap validator fokus satu entity
- ✅ Testable - validator bisa ditest terpisah
- ✅ Flexible - bisa swap strategy

---

## 6. OBSERVER PATTERN (Behavioral)

### Lokasi File
- `app/observers/event_observer.py` (Interface & Subject)
- `app/observers/activity_logger.py` (Concrete Observer)

### Tujuan
Mendefinisikan **mekanisme subscription** untuk memberitahu multiple objects ketika ada event. Dalam aplikasi ini, digunakan untuk **auto-logging** setiap aktivitas (create, update, delete book/loan).

### Diagram

```
┌──────────────────────────────────────────────────────────────┐
│                     EventSubject                              │
│                     (Publisher)                               │
├──────────────────────────────────────────────────────────────┤
│ - _observers: Dict[EventType, List[Observer]]                │
├──────────────────────────────────────────────────────────────┤
│ + attach(observer)                                           │
│ + detach(observer)                                           │
│ + notify(event_type, data)  ────────────────────────────┐    │
└──────────────────────────────────────────────────────────────┘
                                                          │
                      notifies all observers              │
                                                          ▼
    ┌─────────────────────────────────────────────────────────────┐
    │                    EventObserver                             │
    │                    (Interface)                               │
    ├─────────────────────────────────────────────────────────────┤
    │ + update(event_type, data)                                  │
    │ + get_subscribed_events(): List[EventType]                  │
    └─────────────────────────────────────────────────────────────┘
                               ▲
                               │ implements
                               │
                ┌──────────────┴──────────────┐
                │       ActivityLogger         │
                │    (Concrete Observer)       │
                ├─────────────────────────────┤
                │ - logger: Logger            │
                │ + update(event, data)       │ ──► Write to logs/app.log
                │ + get_subscribed_events()   │
                └─────────────────────────────┘
```

### Event Types

```python
class EventType(Enum):
    BOOK_CREATED = "book_created"
    BOOK_UPDATED = "book_updated"
    BOOK_DELETED = "book_deleted"
    LOAN_CREATED = "loan_created"
    LOAN_RETURNED = "loan_returned"
    SYSTEM_ERROR = "system_error"
    SYSTEM_WARNING = "system_warning"
```

### Implementasi Kode

```python
# Interface Observer
class EventObserver(ABC):
    
    @abstractmethod
    def update(self, event_type, data):
        """Dipanggil ketika ada event"""
        pass
    
    @abstractmethod
    def get_subscribed_events(self):
        """Events yang di-subscribe"""
        pass


# Subject (Publisher)
class EventSubject:
    
    def __init__(self):
        self._observers = {}  # event_type -> list of observers
    
    def attach(self, observer):
        """Daftarkan observer"""
        for event_type in observer.get_subscribed_events():
            if event_type not in self._observers:
                self._observers[event_type] = []
            self._observers[event_type].append(observer)
    
    def detach(self, observer):
        """Hapus observer"""
        for event_type in observer.get_subscribed_events():
            if observer in self._observers.get(event_type, []):
                self._observers[event_type].remove(observer)
    
    def notify(self, event_type, data=None):
        """Beritahu semua observer"""
        for observer in self._observers.get(event_type, []):
            observer.update(event_type, data or {})


# Concrete Observer - Activity Logger
class ActivityLogger(EventObserver):
    
    def __init__(self, log_file='logs/app.log'):
        self._setup_logger()
    
    def get_subscribed_events(self):
        return list(EventType)  # Subscribe semua events
    
    def update(self, event_type, data):
        """Handler ketika event terjadi"""
        message = self._format_message(event_type, data)
        self.logger.info(message)
    
    def _format_message(self, event_type, data):
        if event_type == EventType.BOOK_CREATED:
            book = data.get('book', {})
            return f"[BOOK_CREATED] Buku '{book.get('title')}' ditambahkan"
        elif event_type == EventType.LOAN_CREATED:
            loan = data.get('loan', {})
            return f"[LOAN] {loan.get('borrower_name')} meminjam buku"
        # ... dst


# Setup - register observer
event_subject = EventSubject()
activity_logger = ActivityLogger()
event_subject.attach(activity_logger)


# Penggunaan di Service:
class BookService:
    def create_book(self, data):
        book = self.repository.save(...)
        
        # Trigger observer - auto logging!
        self.event_subject.notify(
            EventType.BOOK_CREATED,
            {'book': book.to_dict()}
        )
```

### Contoh Log Output

```
2025-11-30 10:00:00 - INFO - [BOOK_CREATED] Buku 'Clean Code' ditambahkan
2025-11-30 10:05:00 - INFO - [LOAN_CREATED] John Doe meminjam buku
2025-11-30 10:30:00 - INFO - [BOOK_UPDATED] Buku 'Clean Code' diupdate
2025-11-30 11:00:00 - INFO - [LOAN_RETURNED] John Doe mengembalikan buku
```

### Cara Kerja

1. `EventSubject` (Publisher) mengelola daftar observers
2. Observers mendaftarkan diri via `attach()`
3. Ketika ada event, Service memanggil `notify(event_type, data)`
4. Subject memberitahu semua observer yang subscribe event tersebut
5. Observer (ActivityLogger) menulis ke file log

### Manfaat

- ✅ Loose coupling - Service tidak tahu siapa yang listening
- ✅ Extensible - mudah tambah observer baru (email notif, analytics, dll)
- ✅ Automatic - logging terjadi otomatis tanpa manual call
- ✅ Multiple observers untuk satu event

---

## Ringkasan Alur Design Patterns

```
┌──────────────────────────────────────────────────────────────────┐
│                     POST /api/books                               │
└──────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────┐
│                    BookController                                 │
│                    (parse request)                                │
└──────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────┐
│                    BookService [FACADE]                          │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ 1. validator.validate(data)        [STRATEGY]             │   │
│  │ 2. factory.create_book(data)       [FACTORY]              │   │
│  │ 3. repository.save(book)           [ADAPTER] ────┐        │   │
│  │ 4. event_subject.notify(...)       [OBSERVER]    │        │   │
│  └──────────────────────────────────────────────────┼────────┘   │
└─────────────────────────────────────────────────────┼────────────┘
                                                      │
                                                      ▼
                              ┌──────────────────────────────────────┐
                              │      DatabaseConnection              │
                              │         [SINGLETON]                  │
                              │                                      │
                              │    Only ONE instance!                │
                              └──────────────────────────────────────┘
                                              │
                                              ▼
                                        ┌──────────┐
                                        │PostgreSQL│
                                        │ Database │
                                        └──────────┘
```

---

## Kesimpulan

Keenam design patterns ini bekerja sama untuk menciptakan aplikasi yang:

1. **Maintainable** - Perubahan terisolasi di layer yang tepat
2. **Testable** - Setiap komponen bisa ditest terpisah
3. **Scalable** - Mudah menambah fitur baru
4. **Flexible** - Komponen bisa diganti tanpa breaking changes
5. **Clean** - Separation of concerns yang jelas

---

**Dokumen ini dibuat untuk keperluan pembelajaran Design Patterns dalam konteks aplikasi nyata.**
