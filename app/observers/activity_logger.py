"""
Activity Logger - Concrete Observer untuk logging aktivitas

Implementasi Observer Pattern untuk auto-logging setiap event
"""

import os
import logging
from datetime import datetime
from app.observers.event_observer import EventObserver, EventType, event_subject


class ActivityLogger(EventObserver):
    """
    Concrete Observer untuk logging aktivitas sistem
    
    Pattern: Observer
    Otomatis mencatat semua aktivitas penting ke file log
    """
    
    def __init__(self, log_file='logs/app.log'):
        """
        Inisialisasi logger
        
        Args:
            log_file: Path ke file log
        """
        self.log_file = log_file
        self._setup_logger()
    
    def _setup_logger(self):
        """
        Setup konfigurasi logging
        """
        # Buat direktori logs jika belum ada
        log_dir = os.path.dirname(self.log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # Konfigurasi logger
        self.logger = logging.getLogger('LibraryAPI')
        self.logger.setLevel(logging.INFO)
        
        # Hindari duplicate handlers
        if not self.logger.handlers:
            # File handler
            file_handler = logging.FileHandler(self.log_file, encoding='utf-8')
            file_handler.setLevel(logging.INFO)
            
            # Console handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            
            # Format log
            formatter = logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)
            
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)
    
    def get_subscribed_events(self):
        """
        Mendapatkan daftar event yang disubscribe
        Logger subscribe ke semua event
        
        Returns:
            List[EventType]: Semua event types
        """
        return list(EventType)  # Subscribe ke semua events
    
    def update(self, event_type, data):
        """
        Handler ketika menerima notifikasi event
        
        Args:
            event_type (EventType): Jenis event
            data (dict): Data terkait event
        """
        # Format message berdasarkan event type
        message = self._format_message(event_type, data)
        
        # Log dengan level yang sesuai
        if event_type == EventType.SYSTEM_ERROR:
            self.logger.error(message)
        elif event_type == EventType.SYSTEM_WARNING:
            self.logger.warning(message)
        else:
            self.logger.info(message)
    
    def _format_message(self, event_type, data):
        """
        Format pesan log berdasarkan event type
        
        Args:
            event_type: Jenis event
            data: Data event
        
        Returns:
            str: Formatted log message
        """
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        if event_type == EventType.BOOK_CREATED:
            book_info = data.get('book', {})
            return f"[BOOK_CREATED] Buku baru ditambahkan: '{book_info.get('title', 'N/A')}' (ID: {book_info.get('id', 'N/A')})"
        
        elif event_type == EventType.BOOK_UPDATED:
            book_info = data.get('book', {})
            return f"[BOOK_UPDATED] Buku diupdate: '{book_info.get('title', 'N/A')}' (ID: {book_info.get('id', 'N/A')})"
        
        elif event_type == EventType.BOOK_DELETED:
            return f"[BOOK_DELETED] Buku dihapus (ID: {data.get('book_id', 'N/A')})"
        
        elif event_type == EventType.LOAN_CREATED:
            loan_info = data.get('loan', {})
            return f"[LOAN_CREATED] Peminjaman baru: Buku '{loan_info.get('book_title', 'N/A')}' oleh {loan_info.get('borrower_name', 'N/A')}"
        
        elif event_type == EventType.LOAN_RETURNED:
            loan_info = data.get('loan', {})
            return f"[LOAN_RETURNED] Buku dikembalikan: '{loan_info.get('book_title', 'N/A')}' oleh {loan_info.get('borrower_name', 'N/A')}"
        
        elif event_type == EventType.SYSTEM_ERROR:
            return f"[ERROR] {data.get('message', 'Unknown error')}"
        
        elif event_type == EventType.SYSTEM_WARNING:
            return f"[WARNING] {data.get('message', 'Unknown warning')}"
        
        else:
            return f"[{event_type.value.upper()}] {data}"
    
    def log_custom(self, message, level='info'):
        """
        Log pesan custom
        
        Args:
            message: Pesan yang akan di-log
            level: Level log ('info', 'warning', 'error')
        """
        if level == 'error':
            self.logger.error(message)
        elif level == 'warning':
            self.logger.warning(message)
        else:
            self.logger.info(message)


# Buat singleton instance dan daftarkan ke event subject
activity_logger = ActivityLogger()
event_subject.attach(activity_logger)
