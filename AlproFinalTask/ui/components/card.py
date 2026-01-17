"""
Card Component - Komponen card untuk section penjelasan
Skema warna hijau untuk tema pembelajaran
"""
from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel, QTextEdit
from PySide6.QtCore import Qt
from PySide6.QtGui import QTextOption


class SectionCard(QFrame):
    """Card untuk section penjelasan dengan font lebih besar dan justify"""
    
    def __init__(self, title_text, content_text, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QFrame {
                background-color: #1e293b;
                border-radius: 12px;
                padding: 25px;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(25, 25, 25, 25)
        
        # Title
        title = QLabel(title_text)
        title.setStyleSheet("""
            QLabel {
                font-size: 28px;
                font-weight: bold;
                color: #e2e8f0;
            }
        """)
        
        # Content dengan justify - menggunakan QLabel agar tidak scroll terpisah
        content = QLabel(content_text)
        content.setWordWrap(True)
        content.setAlignment(Qt.AlignJustify)
        content.setStyleSheet("""
            QLabel {
                font-size: 18px;
                color: #cbd5e1;
                line-height: 1.8;
                background-color: transparent;
                padding: 0px;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
        """)
        
        layout.addWidget(title)
        layout.addWidget(content)
        
        self.title_label = title
        self.content_label = content