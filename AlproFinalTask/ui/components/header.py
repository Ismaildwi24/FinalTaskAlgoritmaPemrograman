"""
Header Component - Komponen header untuk halaman
"""
from PySide6.QtWidgets import QLabel


class PageHeader(QLabel):
    """Header untuk halaman pembelajaran"""
    
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("""
            QLabel {
                font-size: 40px;
                font-weight: bold;
                color: #e2e8f0;
                padding: 10px;
            }
        """)