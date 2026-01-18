import sys
import os

# ==========================================
# SETUP PATH UNTUK IMPORT
# ==========================================
if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, "../../"))
    sys.path.insert(0, project_root)

from PySide6.QtWidgets import (
    QWidget, QLabel, QPushButton, QHBoxLayout, 
    QVBoxLayout, QFrame, QGraphicsDropShadowEffect,
    QApplication
)
from PySide6.QtCore import Qt, QSize, QRectF
from PySide6.QtGui import QPainter, QPen, QBrush, QColor

# Mencoba import Sidebar, jika gagal pakai dummy
try:
    from ui.components.sidebar import Sidebar
except ImportError:
    class Sidebar(QWidget):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.setFixedWidth(250)
            self.setStyleSheet("background-color: #0f172a;")

# ==========================================
# KONFIGURASI WARNA & STYLE
# ==========================================
COLOR_BG = "#0b1220"       # Dark Blue Background
COLOR_ACCENT = "#00e5ff"   # Neon Cyan
COLOR_TEXT = "#ffffff"     # White
COLOR_CARD_BG = "rgba(11, 18, 32, 0.6)" # Semi-transparent dark
GLOW_RADIUS = 25

class IconWidget(QFrame):
    """
    Widget ikon vektor yang digambar secara manual dengan QPainter.
    """
    def __init__(self, icon_type, color=QColor(COLOR_ACCENT)):
        super().__init__()
        self.icon_type = icon_type
        self.color = color
        self.setFixedSize(90, 90)
        self.setStyleSheet("background-color: transparent;")
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Pen Style (Neon Outline)
        pen = QPen(self.color, 3)
        pen.setCapStyle(Qt.RoundCap)
        pen.setJoinStyle(Qt.RoundJoin)
        painter.setPen(pen)
        
        # Brush Style (Semi-transparent fill)
        brush_color = QColor(self.color)
        brush_color.setAlpha(40) 
        brush = QBrush(brush_color)

        if self.icon_type == "huffman":
            # Icon Chip / Kompresi
            rect = QRectF(25, 25, 40, 40)
            painter.drawRoundedRect(rect, 8, 8)
            # Jalur
            painter.drawLine(15, 35, 25, 35)
            painter.drawLine(15, 45, 25, 45)
            painter.drawLine(15, 55, 25, 55)
            painter.drawLine(65, 35, 75, 35)
            painter.drawLine(65, 45, 75, 45)
            painter.drawLine(65, 55, 75, 55)
            # Inti
            painter.fillRect(QRectF(38, 38, 14, 14), brush)

        elif self.icon_type == "bst":
            # Icon Binary Tree
            painter.drawEllipse(40, 15, 10, 10) # Root
            painter.drawEllipse(25, 40, 10, 10) # Left
            painter.drawEllipse(55, 40, 10, 10) # Right
            painter.drawEllipse(15, 65, 10, 10) # L-L
            painter.drawEllipse(35, 65, 10, 10) # L-R
            
            painter.drawLine(41, 24, 30, 41)
            painter.drawLine(49, 24, 60, 41)
            painter.drawLine(26, 49, 20, 65)
            painter.drawLine(29, 49, 40, 65)

        elif self.icon_type == "traversal":
            # Icon Tree dengan Panah Alur
            painter.drawEllipse(40, 15, 10, 10)
            painter.drawEllipse(25, 40, 10, 10)
            painter.drawEllipse(55, 40, 10, 10)
            
            painter.drawLine(41, 24, 30, 41)
            painter.drawLine(49, 24, 60, 41)
            
            # Panah melengkung (Traversal)
            path = QPen(self.color, 2, Qt.DashLine)
            painter.setPen(path)
            painter.drawArc(20, 55, 50, 20, 0, -180 * 16)
            # Kepala panah
            painter.setPen(QPen(self.color, 3))
            painter.drawLine(65, 60, 70, 65)
            painter.drawLine(65, 70, 70, 65)

        elif self.icon_type == "dijkstra":
            # Icon Graph
            nodes = [(25, 25), (65, 25), (25, 65), (65, 65)]
            for x, y in nodes:
                painter.drawEllipse(x-6, y-6, 12, 12)
            # Edges
            painter.drawLine(31, 25, 59, 25)
            painter.drawLine(25, 31, 25, 59)
            painter.drawLine(31, 65, 59, 65)
            painter.drawLine(65, 31, 65, 59)
            painter.drawLine(29, 29, 61, 61)
            
        painter.end()

class MenuButton(QPushButton):
    """
    Tombol Menu Kustom dengan efek Glow dan Layout Vertikal
    """
    def __init__(self, text, icon_key, parent=None):
        super().__init__(parent)
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedSize(240, 280) 
        
        # Layout Internal Tombol
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 40, 20, 40)
        layout.setSpacing(20)
        
        # Icon
        self.icon_widget = IconWidget(icon_key)
        layout.addWidget(self.icon_widget, alignment=Qt.AlignCenter)
        
        # Label Text
        self.label = QLabel(text)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setWordWrap(True)
        self.label.setStyleSheet(f"""
            QLabel {{
                color: {COLOR_TEXT};
                font-size: 20px;
                font-weight: 700;
                background: transparent;
                border: none;
            }}
        """)
        layout.addWidget(self.label, alignment=Qt.AlignTop)
        
        # Efek Glow (Shadow)
        self.glow = QGraphicsDropShadowEffect(self)
        self.glow.setBlurRadius(0) 
        self.glow.setColor(QColor(COLOR_ACCENT))
        self.glow.setOffset(0, 0)
        self.setGraphicsEffect(self.glow)
        
        # Styling
        self.default_style = f"""
            QPushButton {{
                background-color: {COLOR_CARD_BG};
                border: 2px solid rgba(0, 229, 255, 0.3);
                border-radius: 24px;
            }}
        """
        self.hover_style = f"""
            QPushButton {{
                background-color: rgba(0, 229, 255, 0.1);
                border: 2px solid {COLOR_ACCENT};
                border-radius: 24px;
            }}
        """
        self.setStyleSheet(self.default_style)

    def enterEvent(self, event):
        """Efek saat mouse masuk"""
        self.setStyleSheet(self.hover_style)
        self.glow.setBlurRadius(GLOW_RADIUS) 
        super().enterEvent(event)

    def leaveEvent(self, event):
        """Efek saat mouse keluar"""
        self.setStyleSheet(self.default_style)
        self.glow.setBlurRadius(0) 
        super().leaveEvent(event)


class MenuPage(QWidget):
    """
    Halaman Utama dengan 4 Pilihan Pembelajaran
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        
        # Main Layout
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 1. Sidebar
        self.sidebar = Sidebar()
        main_layout.addWidget(self.sidebar)
        
        # 2. Area Konten Utama
        content_widget = QWidget()
        content_widget.setStyleSheet(f"background-color: {COLOR_BG};")
        
        # Layout Konten
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(60, 60, 60, 50)
        content_layout.setSpacing(40)
        
        # === HEADER ===
        header_layout = QVBoxLayout()
        header_layout.setSpacing(10)
        
        title = QLabel("Pilih Pembelajaran")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"""
            QLabel {{
                font-size: 42px;
                font-weight: 800;
                color: {COLOR_TEXT};
                letter-spacing: 1px;
            }}
        """)
        
        # (Glow effect dihapus sesuai permintaan sebelumnya)

        subtitle = QLabel("Silakan pilih algoritma yang ingin Anda pelajari secara visual.")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("font-size: 16px; color: #94a3b8;")
        
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        
        content_layout.addLayout(header_layout)
        content_layout.addSpacing(30)
        
        # === MENU BUTTONS (HORIZONTAL) ===
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(30)
        buttons_layout.setAlignment(Qt.AlignCenter)
        
        self.menu_buttons = {}
        
        # Data Menu
        menu_items = [
            ("Huffman\nCoding", "huffman"),
            ("Binary\nSearch Tree", "bst"),
            ("Binary\nTraversal", "traversal"),
            ("Algoritma\nDijkstra", "dijkstra")
        ]
        
        for name, key in menu_items:
            btn = MenuButton(name, key)
            buttons_layout.addWidget(btn)
            self.menu_buttons[key] = btn
            
        content_layout.addLayout(buttons_layout)
        
        # === SPACER UTAMA ===
        # Mendorong konten ke atas agar tidak melayang di tengah jika window sangat tinggi
        content_layout.addStretch()
        
        main_layout.addWidget(content_widget)

# ==========================================
# BLOCK TESTING
# ==========================================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MenuPage()
    window.setWindowTitle("Menu Page Preview")
    window.resize(1200, 800)
    window.show()
    sys.exit(app.exec())