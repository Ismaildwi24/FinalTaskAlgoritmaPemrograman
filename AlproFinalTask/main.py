"""
Main Application - Program Pembelajaran Algoritma & Struktur Data
"""
import sys
from PySide6.QtWidgets import QApplication, QStackedWidget
from PySide6.QtCore import Qt

from ui.pages.welcome_page import WelcomePage
from ui.pages.menu_page import MenuPage
from ui.pages.huffman_page import HuffmanPage
from ui.pages.bst_page import BSTPage
from ui.pages.traversal_page import TraversalPage
from ui.pages.dijkstra_page import DijkstraPage


def load_stylesheet():
    """Load dark theme stylesheet"""
    try:
        with open('ui/styles/dark.qss', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return ""


def main():
    app = QApplication(sys.argv)
    
    # Load stylesheet
    stylesheet = load_stylesheet()
    if stylesheet:
        app.setStyleSheet(stylesheet)
    
    # Window utama menggunakan QStackedWidget untuk navigasi
    window = QStackedWidget()
    window.setWindowTitle("Program Pembelajaran Algoritma & Struktur Data")
    # Set full screen saat pertama kali dibuka
    window.showFullScreen()
    window.setStyleSheet("""
        QStackedWidget {
            background-color: #0f172a;
        }
    """)
    
    # Buat semua halaman
    welcome_page = WelcomePage(window)
    menu_page = MenuPage(window)
    huffman_page = HuffmanPage(window)
    bst_page = BSTPage(window)
    traversal_page = TraversalPage(window)
    dijkstra_page = DijkstraPage(window)
    
    # Tambahkan semua halaman ke stacked widget
    window.addWidget(welcome_page)      # Index 0
    window.addWidget(menu_page)         # Index 1
    window.addWidget(huffman_page)      # Index 2
    window.addWidget(bst_page)          # Index 3
    window.addWidget(traversal_page)    # Index 4
    window.addWidget(dijkstra_page)     # Index 5
    
    # Navigasi dari Welcome Page
    welcome_page.btn_masuk.clicked.connect(
        lambda: window.setCurrentIndex(1)  # Menu Page
    )
    
    # Navigasi dari Menu Page ke halaman pembelajaran
    menu_page.menu_buttons['huffman'].clicked.connect(
        lambda: window.setCurrentIndex(2)  # Huffman Page
    )
    menu_page.menu_buttons['bst'].clicked.connect(
        lambda: window.setCurrentIndex(3)  # BST Page
    )
    menu_page.menu_buttons['traversal'].clicked.connect(
        lambda: window.setCurrentIndex(4)  # Traversal Page
    )
    menu_page.menu_buttons['dijkstra'].clicked.connect(
        lambda: window.setCurrentIndex(5)  # Dijkstra Page
    )
    
    # Navigasi Sidebar - Home (kembali ke menu)
    menu_page.sidebar.btn_home.clicked.connect(
        lambda: window.setCurrentIndex(1)  # Menu Page
    )
    # Tombol Exit/Logout (btn_exit dan btn_logout adalah alias yang sama)
    menu_page.sidebar.btn_exit.clicked.connect(app.quit)
    if hasattr(menu_page.sidebar, 'btn_logout'):
        menu_page.sidebar.btn_logout.clicked.connect(app.quit)
    
    # Sidebar untuk halaman pembelajaran
    def go_to_menu():
        window.setCurrentIndex(1)  # Menu Page
    
    for page in [huffman_page, bst_page, traversal_page, dijkstra_page]:
        page.sidebar.btn_home.clicked.connect(go_to_menu)
        # Tombol Exit/Logout (btn_exit dan btn_logout adalah alias yang sama)
        page.sidebar.btn_exit.clicked.connect(app.quit)
        if hasattr(page.sidebar, 'btn_logout'):
            page.sidebar.btn_logout.clicked.connect(app.quit)
    
    # Tampilkan welcome page sebagai halaman awal
    window.setCurrentIndex(0)
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()