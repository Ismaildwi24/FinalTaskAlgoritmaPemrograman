"""
Sidebar component untuk navigasi dengan divider dan ikon yang jelas
Skema warna hijau untuk tema pembelajaran
"""
from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QFrame
from PySide6.QtCore import Qt


class Sidebar(QWidget):
    """Sidebar dengan tombol Home dan Logout, dengan divider vertikal"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(90)
        self.setStyleSheet("""
            QWidget {
                background-color: #1e293b;
                border-right: 3px solid #475569;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(25)
        layout.setContentsMargins(15, 25, 15, 25)
        
        # Tombol Home dengan icon rumah
        self.btn_home = QPushButton("🏠")
        self.btn_home.setFixedSize(60, 60)
        self.btn_home.setToolTip("Kembali ke Menu")
        self.btn_home.setStyleSheet("""
            QPushButton {
                background-color: #2d3748;
                border: 2px solid #475569;
                border-radius: 12px;
                font-size: 28px;
                color: #e2e8f0;
            }
            QPushButton:hover {
                background-color: #374151;
                border: 2px solid #10b981;
            }
            QPushButton:pressed {
                background-color: #4b5563;
            }
        """)
        
        # Spacer untuk push tombol logout/exit ke bawah
        layout.addWidget(self.btn_home)
        layout.addStretch()
        
        # Tombol Exit/Logout dengan ikon pintu terbuka yang jelas di bagian paling bawah
        # Menggunakan satu tombol yang jelas untuk keluar aplikasi
        self.btn_exit = QPushButton("🚪")
        self.btn_exit.setFixedSize(60, 60)
        self.btn_exit.setToolTip("Keluar dari Aplikasi / Exit")
        self.btn_exit.setStyleSheet("""
            QPushButton {
                background-color: #7f1d1d;
                border: 2px solid #dc2626;
                border-radius: 12px;
                font-size: 28px;
                color: #ffffff;
            }
            QPushButton:hover {
                background-color: #991b1b;
                border: 2px solid #ef4444;
                transform: scale(1.05);
            }
            QPushButton:pressed {
                background-color: #991b1b;
                border: 2px solid #dc2626;
            }
        """)
        
        # Alias untuk kompatibilitas dengan kode yang ada
        self.btn_logout = self.btn_exit
        
        # Tambahkan tombol exit di bagian bawah sidebar
        layout.addWidget(self.btn_exit)