import sys
import os
import heapq
from collections import Counter

# ==========================================
# SETUP PATH UNTUK IMPORT
# ==========================================
if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, "../../"))
    sys.path.insert(0, project_root)

from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, 
    QFrame, QScrollArea, QTextEdit, QTableWidget, 
    QTableWidgetItem, QHeaderView, QGraphicsDropShadowEffect,
    QApplication, QPushButton, QSizePolicy
)
from PySide6.QtCore import Qt, QRectF, QPropertyAnimation, QParallelAnimationGroup
from PySide6.QtGui import QColor, QPainter, QPen, QBrush, QFont

# Mencoba import Sidebar
try:
    from ui.components.sidebar import Sidebar
except ImportError:
    class Sidebar(QWidget):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.setFixedWidth(80) 
            self.setStyleSheet("background-color: #0f172a; border-right: 1px solid #1e293b;")

# ==========================================
# KONFIGURASI STYLE
# ==========================================
COLOR_BG = "#0b1220"
COLOR_ACCENT = "#00e5ff"  # Cyan Neon
COLOR_PANEL = "rgba(15, 23, 42, 0.8)"
COLOR_TEXT_MAIN = "#ffffff"
COLOR_TEXT_SEC = "#94a3b8"

# ==========================================
# LOGIC CLASS: HUFFMAN NODE
# ==========================================
class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        if self.freq == other.freq:
            if self.char and other.char:
                return self.char < other.char
            return False 
        return self.freq < other.freq
        
    def __str__(self):
        if self.char:
            return f"[{self.char}:{self.freq}]"
        return f"[Sum:{self.freq}]"

# ==========================================
# UI HELPER: NORMAL NEON PANEL
# ==========================================
class NeonPanel(QFrame):
    def __init__(self, title=None, parent=None):
        super().__init__(parent)
        self.setObjectName("NeonPanel")
        self.setStyleSheet(f"""
            QFrame#NeonPanel {{
                background-color: {COLOR_PANEL};
                border: 1px solid {COLOR_ACCENT};
                border-radius: 15px;
            }}
            QLabel {{
                color: {COLOR_TEXT_MAIN};
                border: none;
                background: transparent;
            }}
        """)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(15)
        
        if title:
            self.title_lbl = QLabel(title)
            self.title_lbl.setFont(QFont("Segoe UI", 14, QFont.Bold))
            self.title_lbl.setStyleSheet(f"color: {COLOR_ACCENT}; letter-spacing: 1px;")
            line = QFrame()
            line.setFrameShape(QFrame.HLine)
            line.setStyleSheet(f"background-color: {COLOR_ACCENT}; max-height: 1px;")
            self.layout.addWidget(self.title_lbl)
            self.layout.addWidget(line)

    def add_content(self, widget):
        self.layout.addWidget(widget)

# ==========================================
# UI HELPER: COLLAPSIBLE NEON PANEL (DROPDOWN)
# ==========================================
class CollapsibleNeonPanel(QFrame):
    """
    Panel Neon yang bisa dibuka/tutup (Dropdown) untuk menghemat ruang.
    """
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.is_expanded = False # Default tertutup
        self.title_text = title
        
        self.setObjectName("CollapsiblePanel")
        self.setStyleSheet(f"""
            QFrame#CollapsiblePanel {{
                background-color: {COLOR_PANEL};
                border: 1px solid {COLOR_ACCENT};
                border-radius: 15px;
            }}
        """)
        
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # 1. Header (Tombol Toggle)
        self.toggle_btn = QPushButton(f"▶ {title} (Klik untuk detail)")
        self.toggle_btn.setCursor(Qt.PointingHandCursor)
        self.toggle_btn.setStyleSheet(f"""
            QPushButton {{
                text-align: left;
                padding: 15px 20px;
                background-color: transparent;
                color: {COLOR_ACCENT};
                font-family: "Segoe UI";
                font-size: 14px;
                font-weight: bold;
                border: none;
                border-radius: 15px;
            }}
            QPushButton:hover {{
                background-color: rgba(0, 229, 255, 0.1);
            }}
        """)
        self.toggle_btn.clicked.connect(self.toggle_content)
        self.main_layout.addWidget(self.toggle_btn)
        
        # 2. Content Area (Container)
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(20, 0, 20, 20) # Padding content
        self.content_layout.setSpacing(10)
        
        # Default Sembunyi
        self.content_widget.setVisible(self.is_expanded)
        self.main_layout.addWidget(self.content_widget)

    def add_content(self, widget):
        self.content_layout.addWidget(widget)
        
    def toggle_content(self):
        self.is_expanded = not self.is_expanded
        
        # Animasi Toggle Icon
        arrow = "▼" if self.is_expanded else "▶"
        status = "(Klik untuk tutup)" if self.is_expanded else "(Klik untuk detail)"
        self.toggle_btn.setText(f"{arrow} {self.title_text} {status}")
        
        # Show/Hide Content
        self.content_widget.setVisible(self.is_expanded)


# ==========================================
# WIDGET 1: STATIC DIAGRAM (PREVIEW)
# ==========================================
class DiagramCanvas(QWidget):
    """Visualisasi statis untuk panel penjelasan"""
    def __init__(self):
        super().__init__()
        self.setMinimumHeight(200)
        self.setStyleSheet("background: transparent;")
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        pen_line = QPen(QColor(COLOR_ACCENT), 2)
        pen_node = QPen(QColor(COLOR_ACCENT), 3)
        brush_node = QBrush(QColor(0, 229, 255, 40))
        
        cx, cy = self.width() // 2, 50
        lx, ly = cx - 60, 130
        rx, ry = cx + 60, 130
        
        painter.setPen(pen_line)
        painter.drawLine(cx, cy+20, lx, ly-20)
        painter.drawLine(cx, cy+20, rx, ry-20)
        
        painter.setPen(pen_node)
        painter.setBrush(brush_node)
        
        r = 25
        painter.drawEllipse(cx-r, cy-r, r*2, r*2)
        painter.drawEllipse(lx-r, ly-r, r*2, r*2)
        painter.drawEllipse(rx-r, ry-r, r*2, r*2)
        
        painter.setPen(QPen(QColor("white")))
        font = QFont("Arial", 10, QFont.Bold)
        painter.setFont(font)
        
        painter.drawText(QRectF(cx-25, cy-25, 50, 50), Qt.AlignCenter, "7")
        painter.drawText(QRectF(lx-25, ly-25, 50, 50), Qt.AlignCenter, "A:5")
        painter.drawText(QRectF(rx-25, ry-25, 50, 50), Qt.AlignCenter, "B:2")
        
        painter.setPen(QPen(QColor(COLOR_ACCENT)))
        painter.drawText(cx - 40, cy + 50, "0")
        painter.drawText(cx + 30, cy + 50, "1")

# ==========================================
# WIDGET 2: DYNAMIC TREE VISUALIZATION
# ==========================================
class DynamicHuffmanTree(QWidget):
    def __init__(self):
        super().__init__()
        self.root = None
        self.setMinimumHeight(400)
        self.setStyleSheet("background-color: transparent;")

    def set_tree(self, root):
        self.root = root
        self.update() 

    def paintEvent(self, event):
        if not self.root:
            return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        self.draw_node(painter, self.root, self.width() // 2, 50, self.width() // 4, 0)

    def draw_node(self, painter, node, x, y, dx, dy):
        pen_line = QPen(QColor(COLOR_ACCENT), 2)
        painter.setPen(pen_line)
        vertical_gap = 70 

        if node.left:
            painter.drawLine(x, y + 20, x - dx, y + vertical_gap - 20)
            mid_x, mid_y = (x + (x - dx)) / 2, (y + 20 + y + vertical_gap - 20) / 2
            painter.drawText(int(mid_x) - 10, int(mid_y), "0")
            self.draw_node(painter, node.left, x - dx, y + vertical_gap, dx / 2, dy + 1)

        if node.right:
            painter.drawLine(x, y + 20, x + dx, y + vertical_gap - 20)
            mid_x, mid_y = (x + (x + dx)) / 2, (y + 20 + y + vertical_gap - 20) / 2
            painter.drawText(int(mid_x) + 5, int(mid_y), "1")
            self.draw_node(painter, node.right, x + dx, y + vertical_gap, dx / 2, dy + 1)

        pen_node = QPen(QColor(COLOR_ACCENT), 3)
        brush_node = QBrush(QColor(0, 229, 255, 40)) 
        painter.setPen(pen_node)
        painter.setBrush(brush_node)
        
        radius = 20
        painter.drawEllipse(x - radius, y - radius, radius * 2, radius * 2)

        painter.setPen(QPen(QColor("white")))
        font = QFont("Arial", 8, QFont.Bold)
        painter.setFont(font)
        
        if node.char:
            label = f"{node.char}:{node.freq}"
        else:
            label = str(node.freq)
        painter.drawText(QRectF(x - 25, y - 25, 50, 50), Qt.AlignCenter, label)


# ==========================================
# MAIN PAGE CLASS
# ==========================================
class HuffmanPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # --- Layout Utama ---
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        self.sidebar = Sidebar()
        main_layout.addWidget(self.sidebar)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet(f"""
            QScrollArea {{ border: none; background-color: {COLOR_BG}; }}
            QScrollBar:vertical {{ background: {COLOR_BG}; width: 10px; }}
            QScrollBar::handle:vertical {{ background: #1e293b; border-radius: 5px; }}
        """)
        
        content_widget = QWidget()
        content_widget.setStyleSheet(f"background-color: {COLOR_BG};")
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(40, 40, 40, 40)
        content_layout.setSpacing(30)
        
        # =================================================================
        # PANEL 1: EXPLANATION (Collapsible)
        # =================================================================
        panel_explain = CollapsibleNeonPanel("Algorithm Explanation")
        
        lbl_text = QLabel(
            "Huffman Coding adalah algoritma kompresi data lossless yang populer. "
            "Algoritma ini memberikan kode biner variabel-panjang ke karakter input, "
            "di mana panjang kode didasarkan pada frekuensi karakter tersebut.\n\n"
            "Karakter yang paling sering muncul mendapatkan kode terkecil, sedangkan "
            "karakter yang jarang muncul mendapatkan kode yang lebih panjang."
        )
        lbl_text.setWordWrap(True)
        lbl_text.setStyleSheet(f"font-size: 16px; color: {COLOR_TEXT_SEC}; line-height: 1.5;")
        panel_explain.add_content(lbl_text)
        content_layout.addWidget(panel_explain)
        
        # --- PANEL 2: VISUAL DIAGRAM (Collapsible) ---
        panel_visual = CollapsibleNeonPanel("Visual Diagram (Preview)")
        canvas = DiagramCanvas()
        panel_visual.add_content(canvas)
        content_layout.addWidget(panel_visual)
        
        # --- PANEL 3: REAL-WORLD USE (Collapsible) ---
        panel_use = CollapsibleNeonPanel("Real-world Use") 
        lbl_use = QLabel(
            "• Format kompresi ZIP (Deflate)\n"
            "• Kompresi gambar JPEG (tahap akhir)\n"
            "• Kompresi audio MP3"
        )
        lbl_use.setStyleSheet(f"font-size: 15px; color: {COLOR_TEXT_MAIN}; font-weight: 500;")
        panel_use.add_content(lbl_use)
        content_layout.addWidget(panel_use)
        
        # --- PANEL 4: INTERACTIVE SIMULATION ---
        panel_sim = NeonPanel("Interactive Simulation")
        
        sim_layout = QHBoxLayout()
        sim_layout.setSpacing(20)
        
        # Input
        input_group = QVBoxLayout()
        lbl_in = QLabel("Input Text")
        lbl_in.setStyleSheet(f"color: {COLOR_ACCENT}; font-weight: bold;")
        self.txt_input = QTextEdit()
        self.txt_input.setPlaceholderText("Masukkan teks (Cth: KASUR RUSAK)")
        self.txt_input.setStyleSheet(f"""
            QTextEdit {{
                background-color: #0f172a; border: 1px solid #334155;
                color: white; border-radius: 8px; padding: 10px;
            }}
            QTextEdit:focus {{ border: 1px solid {COLOR_ACCENT}; }}
        """)
        btn_process = QPushButton("Encode Now")
        btn_process.setCursor(Qt.PointingHandCursor)
        btn_process.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLOR_ACCENT}; color: black;
                font-weight: bold; border-radius: 8px; padding: 10px;
            }}
            QPushButton:hover {{ background-color: #00b8cc; }}
        """)
        btn_process.clicked.connect(self.process_huffman)
        
        input_group.addWidget(lbl_in)
        input_group.addWidget(self.txt_input)
        input_group.addWidget(btn_process)
        
        # Stats Table
        stats_group = QVBoxLayout()
        lbl_stats = QLabel("Character Frequency")
        lbl_stats.setStyleSheet(f"color: {COLOR_ACCENT}; font-weight: bold;")
        self.table_stats = QTableWidget(0, 2)
        self.table_stats.setHorizontalHeaderLabels(["Char", "Freq"])
        self.table_stats.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_stats.verticalHeader().setVisible(False)
        self.table_stats.setStyleSheet(f"""
            QTableWidget {{
                background-color: #0f172a; border: 1px solid #334155;
                color: white; border-radius: 8px;
            }}
            QHeaderView::section {{
                background-color: #1e293b; color: {COLOR_ACCENT}; border: none; padding: 5px;
            }}
        """)
        stats_group.addWidget(lbl_stats)
        stats_group.addWidget(self.table_stats)
        
        # Output
        out_group = QVBoxLayout()
        lbl_out = QLabel("Binary Output")
        lbl_out.setStyleSheet(f"color: {COLOR_ACCENT}; font-weight: bold;")
        self.txt_output = QTextEdit()
        self.txt_output.setReadOnly(True)
        self.txt_output.setStyleSheet(f"""
            QTextEdit {{
                background-color: #0f172a; border: 1px solid #334155;
                color: #00ff00; font-family: Consolas; border-radius: 8px; padding: 10px;
            }}
        """)
        out_group.addWidget(lbl_out)
        out_group.addWidget(self.txt_output)
        
        sim_layout.addLayout(input_group, 3)
        sim_layout.addLayout(stats_group, 2)
        sim_layout.addLayout(out_group, 3)
        
        panel_sim.layout.addLayout(sim_layout)
        content_layout.addWidget(panel_sim)

        # --- PANEL 5: STEP-BY-STEP SOLUTION ---
        panel_steps = CollapsibleNeonPanel("Step-by-Step Solution")
        panel_steps.toggle_content() # Buka default untuk hasil
        
        self.txt_steps = QTextEdit()
        self.txt_steps.setReadOnly(True)
        self.txt_steps.setPlaceholderText("Langkah-langkah pengerjaan akan muncul di sini...")
        self.txt_steps.setStyleSheet(f"""
            QTextEdit {{
                background-color: #0f172a; border: 1px solid #334155;
                color: white; font-family: "Segoe UI", sans-serif; 
                border-radius: 8px; padding: 10px;
                font-size: 14px; line-height: 1.5;
            }}
        """)
        panel_steps.add_content(self.txt_steps)
        content_layout.addWidget(panel_steps)
        
        # --- PANEL 6: GENERATED VISUALIZATION ---
        panel_tree = NeonPanel("Generated Huffman Tree")
        self.tree_canvas = DynamicHuffmanTree()
        panel_tree.add_content(self.tree_canvas)
        content_layout.addWidget(panel_tree)
        
        content_layout.addStretch()
        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)

    def process_huffman(self):
        """Logika Utama Huffman Coding dengan Log Steps"""
        text = self.txt_input.toPlainText().upper()
        if not text:
            return
            
        log = []
        log.append("<b>Langkah 1: Menghitung Frekuensi Karakter</b>")

        # 1. Hitung Frekuensi
        freq_map = Counter(text)
        freq_list_str = ", ".join([f"{k}:{v}" for k, v in freq_map.items()])
        log.append(f"Frekuensi: {{ {freq_list_str} }}\n")
        
        self.table_stats.setRowCount(len(freq_map))
        sorted_freq = sorted(freq_map.items(), key=lambda item: item[1], reverse=True)
        for i, (char, freq) in enumerate(sorted_freq):
            self.table_stats.setItem(i, 0, QTableWidgetItem(char))
            self.table_stats.setItem(i, 1, QTableWidgetItem(str(freq)))

        # 2. Bangun Huffman Tree
        log.append("<b>Langkah 2: Membangun Pohon Huffman (Priority Queue)</b>")
        heap = [HuffmanNode(char, freq) for char, freq in freq_map.items()]
        heapq.heapify(heap)

        log.append(f"Antrean Awal: {', '.join([str(n) for n in heap])}")
        
        step_count = 1
        while len(heap) > 1:
            left = heapq.heappop(heap)
            right = heapq.heappop(heap)
            
            merged = HuffmanNode(None, left.freq + right.freq)
            merged.left = left
            merged.right = right
            
            heapq.heappush(heap, merged)
            log.append(f"Iterasi {step_count}: Ambil terendah {left} & {right} -> Gabung jadi {merged}")
            step_count += 1

        root = heap[0]
        log.append(f"Root Akhir: {root}\n")
        
        self.tree_canvas.set_tree(root)

        # 3. Generate Codes
        log.append("<b>Langkah 3: Menghasilkan Kode Biner (Traversal)</b>")
        huffman_codes = {}
        
        def generate_codes(node, current_code):
            if not node: return
            if node.char:
                huffman_codes[node.char] = current_code
                log.append(f"Karakter '{node.char}' (Leaf) -> Path: {current_code}")
            generate_codes(node.left, current_code + "0")
            generate_codes(node.right, current_code + "1")

        generate_codes(root, "")

        # 4. Encode Text
        encoded_str = ""
        for char in text:
            encoded_str += huffman_codes.get(char, "") + " " 
        
        self.txt_output.setText(encoded_str.strip())
        self.txt_steps.setHtml("<br>".join(log))

# ==========================================
# BLOCK TESTING
# ==========================================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HuffmanPage()
    window.setWindowTitle("Huffman Page")
    window.resize(1200, 900)
    window.show()
    sys.exit(app.exec())