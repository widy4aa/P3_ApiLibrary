"""
Statistics Service - Service untuk kalkulasi statistik perpustakaan
"""

from app.repositories import book_repository, loan_repository


class StatisticsService:
    """
    Service untuk menghasilkan statistik perpustakaan
    """
    
    def __init__(self):
        """
        Inisialisasi service
        """
        self.book_repository = book_repository
        self.loan_repository = loan_repository
    
    def get_library_statistics(self):
        """
        Mendapatkan statistik lengkap perpustakaan
        
        Returns:
            dict: Response dengan statistik
        """
        try:
            # Statistik buku
            total_books = self.book_repository.count()
            available_books = self.book_repository.count({'available_only': True})
            categories = self.book_repository.get_categories()
            
            # Statistik peminjaman
            loan_stats = self.loan_repository.get_loan_statistics()
            
            return {
                'success': True,
                'data': {
                    'books': {
                        'total': total_books,
                        'available': available_books,
                        'borrowed': total_books - available_books,
                        'categories_count': len(categories),
                        'categories': categories
                    },
                    'loans': loan_stats
                },
                'message': 'Statistik berhasil diambil'
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Gagal mengambil statistik: {str(e)}',
                'data': None
            }
    
    def get_category_statistics(self):
        """
        Mendapatkan statistik per kategori
        
        Returns:
            dict: Response dengan statistik kategori
        """
        try:
            categories = self.book_repository.get_categories()
            
            category_stats = []
            for category in categories:
                total = self.book_repository.count({'category': category})
                available = self.book_repository.count({
                    'category': category, 
                    'available_only': True
                })
                
                category_stats.append({
                    'category': category,
                    'total_books': total,
                    'available': available,
                    'borrowed': total - available
                })
            
            return {
                'success': True,
                'data': category_stats,
                'message': 'Statistik kategori berhasil diambil'
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Gagal mengambil statistik: {str(e)}',
                'data': []
            }


# Singleton instance
statistics_service = StatisticsService()
