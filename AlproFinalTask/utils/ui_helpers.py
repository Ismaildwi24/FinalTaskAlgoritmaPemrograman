"""
Helper functions untuk styling UI yang konsisten
DEPRECATED: Gunakan ui.components.card.SectionCard dan ui.components.header.PageHeader
File ini tetap ada untuk backward compatibility
"""
from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel, QTextEdit
from PySide6.QtCore import Qt
from PySide6.QtGui import QTextOption


def create_section_card(title_text, content_text):
    """
    Membuat card untuk section penjelasan dengan font lebih besar dan justify
    DEPRECATED: Gunakan ui.components.card.SectionCard
    """
    card = QFrame()
    card.setStyleSheet("""
        QFrame {
            background-color: #1e293b;
            border-radius: 12px;
            padding: 25px;
        }
    """)
    
    layout = QVBoxLayout(card)
    layout.setSpacing(20)
    
    title = QLabel(title_text)
    title.setStyleSheet("""
        QLabel {
            font-size: 28px;
            font-weight: bold;
            color: #e2e8f0;
        }
    """)
    
    content = QTextEdit()
    content.setReadOnly(True)
    content.setPlainText(content_text)
    content.setWordWrapMode(QTextOption.WrapAtWordBoundaryOrAnywhere)
    content.setStyleSheet("""
        QTextEdit {
            font-size: 18px;
            color: #cbd5e1;
            line-height: 1.8;
            background-color: transparent;
            border: none;
            padding: 0px;
            font-family: 'Segoe UI', Arial, sans-serif;
        }
    """)
    # Set alignment to justify
    content.setAlignment(Qt.AlignJustify)
    
    layout.addWidget(title)
    layout.addWidget(content)
    
    return card