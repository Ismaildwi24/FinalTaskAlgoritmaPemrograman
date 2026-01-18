import sys
import os
import re

# ==========================================
# SETUP PATH UNTUK IMPORT
# ==========================================
if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, "../../"))
    sys.path.insert(0, project_root)

from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, 
    QFrame, QScrollArea, QTextEdit, QLineEdit,
    QApplication, QPushButton, QButtonGroup
)
from PySide6.QtCore import Qt, QRectF
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
# LOGIC CLASS: TREE NODE
# ==========================================
class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

# ==========================================
# UI HELPER: NEON PANEL (STATIC)
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
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.is_expanded = False 
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
        
        # Header
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
        
        # Content
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(20, 0, 20, 20) 
        self.content_layout.setSpacing(10)
        
        self.content_widget.setVisible(self.is_expanded)
        self.main_layout.addWidget(self.content_widget)

    def add_content(self, widget):
        self.content_layout.addWidget(widget)
        
    def toggle_content(self):
        self.is_expanded = not self.is_expanded
        arrow = "▼" if self.is_expanded else "▶"
        status = "(Klik untuk tutup)" if self.is_expanded else "(Klik untuk detail)"
        self.toggle_btn.setText(f"{arrow} {self.title_text} {status}")
        self.content_widget.setVisible(self.is_expanded)

# ==========================================
# WIDGET 1: STATIC DIAGRAM (PREVIEW)
# ==========================================
class DiagramCanvas(QWidget):
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
        painter.setFont(QFont("Arial", 12, QFont.Bold))
        painter.drawText(QRectF(cx-25, cy-25, 50, 50), Qt.AlignCenter, "A")
        painter.drawText(QRectF(lx-25, ly-25, 50, 50), Qt.AlignCenter, "B")
        painter.drawText(QRectF(rx-25, ry-25, 50, 50), Qt.AlignCenter, "C")
        
        painter.setPen(QPen(QColor(COLOR_TEXT_SEC)))
        painter.setFont(QFont("Arial", 9))
        painter.drawText(cx + 40, cy, "Root")
        painter.drawText(lx - 40, ly, "Left")
        painter.drawText(rx + 30, ry, "Right")

# ==========================================
# WIDGET 2: DYNAMIC TREE VISUALIZATION
# ==========================================
class DynamicTreeCanvas(QWidget):
    def __init__(self):
        super().__init__()
        self.root = None
        self.setMinimumHeight(500)
        self.setStyleSheet("background-color: transparent;")

    def set_root(self, root):
        self.root = root
        self.update()

    def paintEvent(self, event):
        if not self.root:
            return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        self.draw_node(painter, self.root, self.width() // 2, 40, self.width() // 4)

    def draw_node(self, painter, node, x, y, dx):
        vertical_gap = 60
        pen_line = QPen(QColor(COLOR_ACCENT), 2)
        painter.setPen(pen_line)

        if node.left:
            child_x, child_y = x - dx, y + vertical_gap
            painter.drawLine(x, y + 20, child_x, child_y - 20)
            self.draw_node(painter, node.left, child_x, child_y, dx * 0.6)
        
        if node.right:
            child_x, child_y = x + dx, y + vertical_gap
            painter.drawLine(x, y + 20, child_x, child_y - 20)
            self.draw_node(painter, node.right, child_x, child_y, dx * 0.6)

        pen_node = QPen(QColor(COLOR_ACCENT), 3)
        brush_node = QBrush(QColor(0, 229, 255, 40))
        painter.setPen(pen_node)
        painter.setBrush(brush_node)
        
        radius = 20
        painter.drawEllipse(x - radius, y - radius, radius * 2, radius * 2)

        painter.setPen(QPen(QColor("white")))
        painter.setFont(QFont("Arial", 10, QFont.Bold))
        painter.drawText(QRectF(x - 25, y - 25, 50, 50), Qt.AlignCenter, str(node.val))

# ==========================================
# MAIN PAGE CLASS
# ==========================================
class TraversalPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.root = None
        
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
        
        # --- PANEL 1: EXPLANATION (Collapsible) ---
        panel_explain = CollapsibleNeonPanel("Algorithm Explanation")
        lbl_text = QLabel(
            "Binary Tree Traversal adalah proses mengunjungi setiap node dalam pohon tepat satu kali. "
            "Terdapat 3 metode utama:\n\n"
            "1. Preorder (Root → Left → Right): Berguna untuk menyalin pohon.\n"
            "2. Inorder (Left → Root → Right): Menghasilkan nilai terurut (pada BST).\n"
            "3. Postorder (Left → Right → Root): Berguna untuk menghapus pohon."
        )
        lbl_text.setWordWrap(True)
        lbl_text.setStyleSheet(f"font-size: 16px; color: {COLOR_TEXT_SEC}; line-height: 1.5;")
        panel_explain.add_content(lbl_text)
        content_layout.addWidget(panel_explain)
        
        # --- PANEL 2: VISUAL PREVIEW (Collapsible) ---
        panel_visual = CollapsibleNeonPanel("Visual Structure")
        canvas = DiagramCanvas()
        panel_visual.add_content(canvas)
        content_layout.addWidget(panel_visual)
        
        # --- PANEL 3: REAL-WORLD USE (Collapsible) ---
        panel_use = CollapsibleNeonPanel("Real-world Use")
        lbl_use = QLabel(
            "• Parsing ekspresi matematika (Syntax Tree)\n"
            "• Serialisasi struktur direktori file\n"
            "• Evaluasi aritmatika (Polish Notation)"
        )
        lbl_use.setStyleSheet(f"font-size: 15px; color: {COLOR_TEXT_MAIN}; font-weight: 500;")
        panel_use.add_content(lbl_use)
        content_layout.addWidget(panel_use)
        
        # --- PANEL 4: INTERACTIVE SIMULATION ---
        panel_sim = NeonPanel("Interactive Simulation")
        sim_layout = QHBoxLayout()
        sim_layout.setSpacing(20)
        
        # Inputs
        input_group = QVBoxLayout()
        lbl_in = QLabel("Build Tree (Insert Nodes)")
        lbl_in.setStyleSheet(f"color: {COLOR_ACCENT}; font-weight: bold;")
        
        self.txt_input = QLineEdit()
        self.txt_input.setPlaceholderText("Angka (cth: 50, 30, 70)")
        self.txt_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: #0f172a; border: 1px solid #334155;
                color: white; border-radius: 8px; padding: 10px; font-size: 16px;
            }}
            QLineEdit:focus {{ border: 1px solid {COLOR_ACCENT}; }}
        """)
        self.txt_input.returnPressed.connect(self.handle_insert)
        
        # Buttons
        btn_insert = QPushButton("Build Tree")
        btn_insert.setCursor(Qt.PointingHandCursor)
        btn_insert.setStyleSheet(self._btn_style(COLOR_ACCENT, "black"))
        btn_insert.clicked.connect(self.handle_insert)
        
        lbl_act = QLabel("Select Traversal:")
        lbl_act.setStyleSheet(f"color: {COLOR_ACCENT}; font-weight: bold; margin-top: 10px;")
        
        btn_inorder = QPushButton("Show Inorder")
        btn_inorder.setStyleSheet(self._btn_style("#3b82f6", "white"))
        btn_inorder.clicked.connect(lambda: self.run_traversal("inorder"))
        
        btn_preorder = QPushButton("Show Preorder")
        btn_preorder.setStyleSheet(self._btn_style("#a855f7", "white"))
        btn_preorder.clicked.connect(lambda: self.run_traversal("preorder"))
        
        btn_postorder = QPushButton("Show Postorder")
        btn_postorder.setStyleSheet(self._btn_style("#ec4899", "white"))
        btn_postorder.clicked.connect(lambda: self.run_traversal("postorder"))

        btn_reset = QPushButton("Reset")
        btn_reset.setCursor(Qt.PointingHandCursor)
        btn_reset.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent; border: 1px solid #ef4444; color: #ef4444;
                font-weight: bold; border-radius: 8px; padding: 8px;
            }}
            QPushButton:hover {{ background-color: #ef4444; color: white; }}
        """)
        btn_reset.clicked.connect(self.handle_reset)
        
        input_group.addWidget(lbl_in)
        input_group.addWidget(self.txt_input)
        input_group.addWidget(btn_insert)
        input_group.addWidget(lbl_act)
        input_group.addWidget(btn_inorder)
        input_group.addWidget(btn_preorder)
        input_group.addWidget(btn_postorder)
        input_group.addWidget(btn_reset)
        input_group.addStretch()
        
        # Output Log
        log_group = QVBoxLayout()
        lbl_log = QLabel("Traversal Output")
        lbl_log.setStyleSheet(f"color: {COLOR_ACCENT}; font-weight: bold;")
        
        self.txt_log = QTextEdit()
        self.txt_log.setReadOnly(True)
        self.txt_log.setPlaceholderText("Hasil traversal akan muncul di sini...")
        self.txt_log.setStyleSheet(f"""
            QTextEdit {{
                background-color: #0f172a; border: 1px solid #334155;
                color: #00ff00; font-family: Consolas; border-radius: 8px; padding: 10px;
                font-size: 14px;
            }}
        """)
        
        log_group.addWidget(lbl_log)
        log_group.addWidget(self.txt_log)
        
        sim_layout.addLayout(input_group, 2)
        sim_layout.addLayout(log_group, 3)
        panel_sim.layout.addLayout(sim_layout)
        content_layout.addWidget(panel_sim)
        
        # --- PANEL 5: STEP-BY-STEP SOLUTION (Collapsible & Auto-Open) ---
        panel_steps = CollapsibleNeonPanel("Step-by-Step Solution")
        panel_steps.toggle_content() # Open default
        
        self.txt_steps = QTextEdit()
        self.txt_steps.setReadOnly(True)
        self.txt_steps.setPlaceholderText("Langkah-langkah traversal akan muncul di sini...")
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

        # --- PANEL 6: VISUALIZATION CANVAS ---
        panel_tree = NeonPanel("Generated Tree Visualization")
        self.tree_canvas = DynamicTreeCanvas()
        panel_tree.add_content(self.tree_canvas)
        content_layout.addWidget(panel_tree)
        
        content_layout.addStretch()
        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)

    def _btn_style(self, bg, text_color):
        return f"""
            QPushButton {{
                background-color: {bg}; color: {text_color};
                font-weight: bold; border-radius: 8px; padding: 10px;
            }}
            QPushButton:hover {{ filter: brightness(120%); }}
        """

    def handle_insert(self):
        text = self.txt_input.text().strip()
        if not text: return
        
        parts = re.split(r'[,\s]+', text)
        inserted = []
        
        for part in parts:
            if not part: continue
            try:
                val = int(part)
                if self.root is None:
                    self.root = TreeNode(val)
                else:
                    self._insert_recursive(self.root, val)
                inserted.append(val)
            except ValueError:
                pass
        
        if inserted:
            self.txt_input.clear()
            self.tree_canvas.set_root(self.root)
            self.txt_log.append(f"🌳 Tree updated with: {inserted}")
            self.txt_steps.setText("Pohon telah diperbarui. Silakan pilih metode Traversal.")
        else:
            self.txt_log.append("⚠️ Input tidak valid.")

    def _insert_recursive(self, node, val):
        if val < node.val:
            if node.left is None:
                node.left = TreeNode(val)
            else:
                self._insert_recursive(node.left, val)
        else:
            if node.right is None:
                node.right = TreeNode(val)
            else:
                self._insert_recursive(node.right, val)

    def run_traversal(self, mode):
        if not self.root:
            self.txt_log.append("⚠️ Tree is empty!")
            return
            
        res = []
        steps = [] 
        
        if mode == "inorder":
            steps.append("<b>🔷 Memulai Inorder Traversal (Left → Root → Right)</b>")
            self._inorder(self.root, res, steps)
            tag = "Inorder"
        elif mode == "preorder":
            steps.append("<b>🔷 Memulai Preorder Traversal (Root → Left → Right)</b>")
            self._preorder(self.root, res, steps)
            tag = "Preorder"
        elif mode == "postorder":
            steps.append("<b>🔷 Memulai Postorder Traversal (Left → Right → Root)</b>")
            self._postorder(self.root, res, steps)
            tag = "Postorder"
            
        result_str = " -> ".join(map(str, res))
        self.txt_log.append(f"📌 {tag}:\n   {result_str}\n")
        self.txt_steps.setHtml("<br>".join(steps))

    def _inorder(self, node, res, steps):
        if node:
            steps.append(f"   🔻 Dari Node {node.val}: Ke Kiri...")
            self._inorder(node.left, res, steps)
            
            res.append(node.val)
            steps.append(f"   ✅ <b>Kunjungi Node {node.val}</b>")
            
            steps.append(f"   🔻 Dari Node {node.val}: Ke Kanan...")
            self._inorder(node.right, res, steps)
        else:
            steps.append("      ❌ Node kosong (Null), kembali.")

    def _preorder(self, node, res, steps):
        if node:
            res.append(node.val)
            steps.append(f"   ✅ <b>Kunjungi Node {node.val}</b>")
            
            steps.append(f"   🔻 Dari Node {node.val}: Ke Kiri...")
            self._preorder(node.left, res, steps)
            
            steps.append(f"   🔻 Dari Node {node.val}: Ke Kanan...")
            self._preorder(node.right, res, steps)
        else:
            steps.append("      ❌ Node kosong (Null), kembali.")

    def _postorder(self, node, res, steps):
        if node:
            steps.append(f"   🔻 Dari Node {node.val}: Ke Kiri...")
            self._postorder(node.left, res, steps)
            
            steps.append(f"   🔻 Dari Node {node.val}: Ke Kanan...")
            self._postorder(node.right, res, steps)
            
            res.append(node.val)
            steps.append(f"   ✅ <b>Kunjungi Node {node.val}</b>")
        else:
            steps.append("      ❌ Node kosong (Null), kembali.")

    def handle_reset(self):
        self.root = None
        self.tree_canvas.set_root(None)
        self.txt_log.clear()
        self.txt_steps.clear()
        self.txt_log.setText("🔄 Tree has been reset.")

# ==========================================
# TESTING
# ==========================================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TraversalPage()
    window.setWindowTitle("Traversal Page")
    window.resize(1200, 900)
    window.show()
    sys.exit(app.exec())