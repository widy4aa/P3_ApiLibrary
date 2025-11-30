"""
DESIGN PATTERN: STRATEGY
Validation Strategy - Interface untuk strategi validasi

Tujuan:
- Memisahkan algoritma validasi dari context
- Memungkinkan pergantian strategi validasi secara dinamis
- Flexible dan extensible validation rules
- Open/Closed principle compliant
"""

from abc import ABC, abstractmethod


class ValidationStrategy(ABC):
    """
    Abstract Strategy untuk validasi input
    
    Pattern: Strategy
    Mendefinisikan interface untuk berbagai strategi validasi
    """
    
    @abstractmethod
    def validate(self, data):
        """
        Validasi data input
        
        Args:
            data (dict): Data yang akan divalidasi
        
        Returns:
            tuple: (is_valid: bool, errors: dict)
                - is_valid: True jika valid
                - errors: Dictionary berisi pesan error per field
        """
        pass
    
    def _check_required_fields(self, data, required_fields):
        """
        Helper method untuk cek field yang wajib
        
        Args:
            data: Dictionary data
            required_fields: List field yang wajib
        
        Returns:
            dict: Error messages per field
        """
        errors = {}
        for field in required_fields:
            if field not in data or data[field] is None or data[field] == '':
                errors[field] = f'{field} wajib diisi'
        return errors
    
    def _check_string_length(self, value, field_name, min_len=1, max_len=None):
        """
        Helper method untuk validasi panjang string
        
        Args:
            value: String yang akan dicek
            field_name: Nama field untuk error message
            min_len: Minimum panjang
            max_len: Maximum panjang
        
        Returns:
            str or None: Error message atau None jika valid
        """
        if not value or not isinstance(value, str):
            return f'{field_name} harus berupa text'
        
        value = value.strip()
        
        if len(value) < min_len:
            return f'{field_name} minimal {min_len} karakter'
        
        if max_len and len(value) > max_len:
            return f'{field_name} maksimal {max_len} karakter'
        
        return None
