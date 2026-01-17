from PySide6.QtWidgets import (
    QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout,
    QGraphicsDropShadowEffect
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPixmap


# =========================
# CONSTANT
# =========================
BG_COLOR = "#0b1220"


# =========================
# GLOW HELPER
# =========================
def add_glow(widget, color, blur=50):
    glow = QGraphicsDropShadowEffect(widget)
    glow.setBlurRadius(blur)
    glow.setColor(color)
    glow.setOffset(0, 0)
    widget.setGraphicsEffect(glow)


# =========================
# WELCOME PAGE
# =========================
class WelcomePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # 1. Beri nama objek agar CSS bisa menargetkan hanya widget utama ini
        self.setObjectName("WelcomePage")

        # 2. PERBAIKAN STYLESHEET
        # Gunakan #WelcomePage untuk mewarnai background utama saja.
        # Gunakan QWidget { background: transparent; } agar container anak (left/right) tidak menumpuk warna.
        self.setStyleSheet(f"""
            #WelcomePage {{
                background-color: {BG_COLOR};
            }}
            QWidget {{
                background: transparent;
            }}
        """)

        main = QHBoxLayout(self)
        main.setContentsMargins(80, 60, 80, 60)
        main.setSpacing(100)

        # ================= LEFT =================
        left = QWidget(self)
        left_layout = QVBoxLayout(left)
        left_layout.setAlignment(Qt.AlignCenter)
        left_layout.setSpacing(35)

        title = QLabel("Belajar Algoritma\n& Struktur Data")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                font-size: 72px;
                font-weight: 800;
                color: white;
                line-height: 1.2;
                padding: 10px;
                background: transparent; 
            }
        """)
        add_glow(title, QColor(255, 255, 255, 180), 50)

        desc = QLabel(
            "Platform interaktif untuk memahami algoritma\n"
            "secara bertahap dan visual."
        )
        desc.setAlignment(Qt.AlignCenter)
        desc.setStyleSheet("""
            QLabel {
                font-size: 20px;
                color: #ffffff;
                line-height: 1.6;
                background: transparent;
            }
        """)

        self.btn_masuk = QPushButton("Masuk")
        self.btn_masuk.setFixedSize(220, 64)
        # Button tetap akan memiliki warnanya sendiri karena style ini menimpa global transparent
        self.btn_masuk.setStyleSheet("""
            QPushButton {
                background-color: #2563eb;
                color: white;
                font-size: 20px;
                font-weight: 700;
                border-radius: 18px;
            }
            QPushButton:hover {
                background-color: #3b82f6;
            }
            QPushButton:pressed {
                background-color: #1e40af;
            }
        """)
        add_glow(self.btn_masuk, QColor(59, 130, 246, 220), 45)

        left_layout.addWidget(title)
        left_layout.addWidget(desc)
        left_layout.addSpacing(15)
        left_layout.addWidget(self.btn_masuk, alignment=Qt.AlignCenter)

        # ================= RIGHT =================
        right = QWidget(self)
        right_layout = QVBoxLayout(right)
        right_layout.setAlignment(Qt.AlignCenter)

        image_label = QLabel()
        image_label.setAlignment(Qt.AlignCenter)

        pixmap = QPixmap("assets/visual.png")
        if not pixmap.isNull():
            image_label.setPixmap(
                pixmap.scaled(
                    550, 550,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
            )
        else:
            image_label.setText("Visual Image")
            image_label.setStyleSheet("color: white; font-size: 20px;")

        add_glow(image_label, QColor(99, 102, 241, 160), 70)
        right_layout.addWidget(image_label)

        # ================= ADD TO MAIN =================
        main.addWidget(left, 1)
        main.addWidget(right, 1)
