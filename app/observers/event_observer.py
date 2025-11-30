"""
DESIGN PATTERN: OBSERVER
Event Observer - Interface untuk sistem notifikasi event

Tujuan:
- Loose coupling antara event producer dan consumer
- Automatic notification ketika ada perubahan
- Extensible - mudah menambah observer baru
- Mendukung multiple observers untuk satu event
"""

from abc import ABC, abstractmethod
from enum import Enum


class EventType(Enum):
    """
    Enum untuk jenis-jenis event yang dapat diamati
    """
    # Book events
    BOOK_CREATED = "book_created"
    BOOK_UPDATED = "book_updated"
    BOOK_DELETED = "book_deleted"
    
    # Loan events
    LOAN_CREATED = "loan_created"
    LOAN_RETURNED = "loan_returned"
    
    # System events
    SYSTEM_ERROR = "system_error"
    SYSTEM_WARNING = "system_warning"


class EventObserver(ABC):
    """
    Abstract Observer untuk menerima notifikasi event
    
    Pattern: Observer
    Interface yang harus diimplementasikan oleh semua observer
    """
    
    @abstractmethod
    def update(self, event_type, data):
        """
        Method yang dipanggil ketika ada event
        
        Args:
            event_type (EventType): Jenis event
            data (dict): Data terkait event
        """
        pass
    
    @abstractmethod
    def get_subscribed_events(self):
        """
        Mendapatkan daftar event yang disubscribe
        
        Returns:
            List[EventType]: Daftar event types
        """
        pass


class EventSubject:
    """
    Subject (Publisher) yang mengelola observers
    
    Pattern: Observer
    Mengelola registrasi dan notifikasi ke observers
    """
    
    def __init__(self):
        """
        Inisialisasi Subject dengan empty observer list
        """
        self._observers = {}  # Dict of event_type -> list of observers
    
    def attach(self, observer):
        """
        Menambahkan observer ke subject
        
        Args:
            observer (EventObserver): Observer yang akan didaftarkan
        """
        for event_type in observer.get_subscribed_events():
            if event_type not in self._observers:
                self._observers[event_type] = []
            if observer not in self._observers[event_type]:
                self._observers[event_type].append(observer)
    
    def detach(self, observer):
        """
        Menghapus observer dari subject
        
        Args:
            observer (EventObserver): Observer yang akan dihapus
        """
        for event_type in observer.get_subscribed_events():
            if event_type in self._observers:
                if observer in self._observers[event_type]:
                    self._observers[event_type].remove(observer)
    
    def notify(self, event_type, data=None):
        """
        Memberitahu semua observer yang terdaftar untuk event tertentu
        
        Args:
            event_type (EventType): Jenis event
            data (dict): Data terkait event
        """
        if event_type in self._observers:
            for observer in self._observers[event_type]:
                try:
                    observer.update(event_type, data or {})
                except Exception as e:
                    # Log error tapi jangan stop notifikasi ke observer lain
                    print(f"Error notifying observer: {e}")
    
    def get_observer_count(self, event_type=None):
        """
        Mendapatkan jumlah observer
        
        Args:
            event_type: Optional, filter by event type
        
        Returns:
            int: Jumlah observer
        """
        if event_type:
            return len(self._observers.get(event_type, []))
        return sum(len(obs) for obs in self._observers.values())


# Singleton event subject untuk digunakan di seluruh aplikasi
event_subject = EventSubject()
