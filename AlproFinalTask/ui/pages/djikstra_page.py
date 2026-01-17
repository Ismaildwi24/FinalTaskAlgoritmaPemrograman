import sys
import os
import math
import heapq
import re

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, "../../"))
    sys.path.insert(0, project_root)

from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, 
    QFrame, QScrollArea, QTextEdit, QLineEdit,
    QApplication, QPushButton, QSizePolicy
)
from PySide6.QtCore import Qt, QRectF, QPointF
from PySide6.QtGui import QColor, QPainter, QPen, QBrush, QFont

try:
    from ui.components.sidebar import Sidebar
except ImportError:
    class Sidebar(QWidget):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.setFixedWidth(80) 
            self.setStyleSheet("background-color: #0f172a; border-right: 1px solid #1e293b;")

# KONFIGURASI STYLE
COLOR_BG = "#0b1220"
COLOR_ACCENT = "#00e5ff"   
COLOR_HIGHLIGHT = "#ffd700" 
COLOR_PANEL = "rgba(15, 23, 42, 0.8)"
COLOR_TEXT_MAIN = "#ffffff"
COLOR_TEXT_SEC = "#94a3b8"

# LOGIC CLASS: DIJKSTRA SOLVER
class GraphLogic:
    def __init__(self):
        self.nodes = set()
        self.edges = {} 
        self.steps_log = [] 

    def clear(self):
        self.nodes.clear()
        self.edges.clear()
        self.steps_log = []

    def add_edge(self, u, v, w):
        self.nodes.add(u)
        self.nodes.add(v)
        if u not in self.edges: self.edges[u] = {}
        if v not in self.edges: self.edges[v] = {}
        self.edges[u][v] = w
        self.edges[v][u] = w

    def get_shortest_path(self, start, end):
        self.steps_log = [] 
        
        if start not in self.nodes or end not in self.nodes:
            self.steps_log.append("⚠️ Error: Node Start atau End tidak ditemukan dalam graf.")
            return None, float('inf'), {}

        pq = [(0, start)]
        distances = {node: float('inf') for node in self.nodes}
        distances[start] = 0
        previous = {node: None for node in self.nodes}
        
        visited = set()
        iteration = 0

        self.steps_log.append(f"🏁 <b>Inisialisasi:</b> Jarak ke {start} = 0, ke node lain = ∞\n")

        while pq:
            current_dist, u = heapq.heappop(pq)

            if u in visited:
                continue
            visited.add(u)
            iteration += 1

            self.steps_log.append(f"🔄 <b>Iterasi {iteration}:</b> Mengunjungi Node <b>{u}</b> (Jarak akumulasi: {current_dist})")

            if u == end:
                self.steps_log.append(f"   ✅ Node tujuan {end} tercapai dengan jarak {current_dist}!")
                break

            if current_dist > distances[u]:
                continue
            
            has_update = False
            if u in self.edges:
                for v, weight in self.edges[u].items():
                    if v in visited: continue 
                    
                    distance = current_dist + weight
                    log_check = f"   👉 Cek tetangga <b>{v}</b> (Jarak via {u}: {current_dist} + {weight} = {distance})"
                    
                    if distance < distances[v]:
                        distances[v] = distance
                        previous[v] = u
                        heapq.heappush(pq, (distance, v))
                        log_check += f" -> <span style='color:{COLOR_ACCENT}'>Update jarak {v} (∞ ➔ {distance})</span>"
                        has_update = True
                    else:
                        log_check += f" -> Tidak update (≥ {distances[v]})"
                    
                    self.steps_log.append(log_check)
            
            if not has_update:
                self.steps_log.append("   💤 Tidak ada pembaruan jarak pada tetangga.")
            
            self.steps_log.append("") 

        path = []
        current = end
        if distances[end] != float('inf'):
            while current:
                path.append(current)
                current = previous[current]
            path.reverse()
        else:
            self.steps_log.append(f"❌ Tidak ada jalur yang ditemukan menuju {end}.")

        return path, distances[end], distances

# UI HELPER: NEON PANEL (STATIC)
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

# UI HELPER: (DROPDOWN)
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

# WIDGET 1: STATIC DIAGRAM (PREVIEW)
class StaticGraphCanvas(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumHeight(200)
        self.setStyleSheet("background: transparent;")
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        cx, cy = self.width() // 2, 50
        lx, ly = cx - 80, 150
        rx, ry = cx + 80, 150
        
        nodes = {'A': (cx, cy), 'B': (lx, ly), 'C': (rx, ry)}
        
        pen_line = QPen(QColor(COLOR_ACCENT), 2)
        painter.setPen(pen_line)
        painter.drawLine(*nodes['A'], *nodes['B'])
        painter.drawLine(*nodes['B'], *nodes['C'])
        
        pen_high = QPen(QColor(COLOR_HIGHLIGHT), 4)
        painter.setPen(pen_high)
        painter.drawLine(*nodes['A'], *nodes['C']) 
        
        pen_node = QPen(QColor(COLOR_ACCENT), 3)
        brush_node = QBrush(QColor(0, 229, 255, 40))
        
        for label, (x, y) in nodes.items():
            painter.setPen(pen_node)
            painter.setBrush(brush_node)
            painter.drawEllipse(QPointF(x, y), 25, 25)
            
            painter.setPen(QColor("white"))
            painter.setFont(QFont("Arial", 10, QFont.Bold))
            painter.drawText(QRectF(x-25, y-25, 50, 50), Qt.AlignCenter, label)

        painter.setPen(QColor(COLOR_TEXT_SEC))
        painter.drawText((cx+lx)//2 - 20, (cy+ly)//2, "4")
        painter.drawText((lx+rx)//2, ly + 20, "3")
        painter.drawText((cx+rx)//2 + 10, (cy+ry)//2, "2")

# WIDGET 2: DYNAMIC GRAPH CANVAS
class DynamicGraphCanvas(QWidget):
    def __init__(self):
        super().__init__()
        self.graph_data = None 
        self.path_result = [] 
        self.setMinimumHeight(500)
        self.setStyleSheet("background-color: transparent;")

    def set_data(self, graph, path=[]):
        self.graph_data = graph
        self.path_result = path
        self.update()

    def paintEvent(self, event):
        if not self.graph_data or not self.graph_data.nodes:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        nodes = sorted(list(self.graph_data.nodes))
        n = len(nodes)
        center_x, center_y = self.width() // 2, self.height() // 2
        radius = min(center_x, center_y) - 60
        
        node_coords = {}
        for i, node in enumerate(nodes):
            angle = 2 * math.pi * i / n
            x = center_x + radius * math.cos(angle - math.pi / 2) 
            y = center_y + radius * math.sin(angle - math.pi / 2)
            node_coords[node] = (x, y)

        processed_edges = set()
        path_edges = set()
        if self.path_result and len(self.path_result) > 1:
            for i in range(len(self.path_result) - 1):
                u, v = self.path_result[i], self.path_result[i+1]
                path_edges.add(tuple(sorted((u, v))))

        for u in self.graph_data.edges:
            for v, w in self.graph_data.edges[u].items():
                edge_key = tuple(sorted((u, v)))
                if edge_key in processed_edges: continue
                processed_edges.add(edge_key)

                if edge_key in path_edges:
                    pen = QPen(QColor(COLOR_HIGHLIGHT), 4) 
                else:
                    pen = QPen(QColor(COLOR_ACCENT), 2) 
                    
                painter.setPen(pen)
                p1 = QPointF(*node_coords[u])
                p2 = QPointF(*node_coords[v])
                painter.drawLine(p1, p2)

                mid_x = (p1.x() + p2.x()) / 2
                mid_y = (p1.y() + p2.y()) / 2
                
                painter.setBrush(QColor(15, 23, 42)) 
                painter.setPen(Qt.NoPen)
                painter.drawEllipse(QPointF(mid_x, mid_y), 12, 12)
                
                painter.setPen(QColor("white"))
                painter.setFont(QFont("Arial", 9))
                painter.drawText(QRectF(mid_x-15, mid_y-15, 30, 30), Qt.AlignCenter, str(w))

        for node, (x, y) in node_coords.items():
            if node in self.path_result:
                pen_node = QPen(QColor(COLOR_HIGHLIGHT), 3)
                brush_node = QBrush(QColor(255, 215, 0, 50)) 
            else:
                pen_node = QPen(QColor(COLOR_ACCENT), 3)
                brush_node = QBrush(QColor(0, 229, 255, 40)) 

            painter.setPen(pen_node)
            painter.setBrush(brush_node)
            painter.drawEllipse(QPointF(x, y), 25, 25)

            painter.setPen(QColor("white"))
            painter.setFont(QFont("Arial", 11, QFont.Bold))
            painter.drawText(QRectF(x-25, y-25, 50, 50), Qt.AlignCenter, str(node))


# MAIN PAGE CLASS
class DijkstraPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.logic = GraphLogic()
        
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
        
        #PANEL 1: EXPLANATION 
        panel_explain = CollapsibleNeonPanel("Algorithm Explanation")
        lbl_text = QLabel(
            "Algoritma Dijkstra digunakan untuk menemukan jalur terpendek antara node "
            "dalam graf berbobot. Algoritma ini bekerja dengan memilih node dengan "
            "jarak terkecil yang belum dikunjungi dan memperbarui jarak tetangganya.\n\n"
            "Sangat efisien untuk graf dengan bobot non-negatif."
        )
        lbl_text.setWordWrap(True)
        lbl_text.setStyleSheet(f"font-size: 16px; color: {COLOR_TEXT_SEC}; line-height: 1.5;")
        panel_explain.add_content(lbl_text)
        content_layout.addWidget(panel_explain)
        
        #PANEL 2: VISUAL PREVIEW
        panel_visual = CollapsibleNeonPanel("Visual Diagram (Concept)")
        canvas = StaticGraphCanvas()
        panel_visual.add_content(canvas)
        content_layout.addWidget(panel_visual)
        
        #PANEL 3: REAL-WORLD USE
        panel_use = CollapsibleNeonPanel("Real-world Use")
        lbl_use = QLabel(
            "• Navigasi GPS (Google Maps, Waze)\n"
            "• Protokol Routing Jaringan (OSPF)\n"
            "• Perencanaan logistik dan distribusi"
        )
        lbl_use.setStyleSheet(f"font-size: 15px; color: {COLOR_TEXT_MAIN}; font-weight: 500;")
        panel_use.add_content(lbl_use)
        content_layout.addWidget(panel_use)
        
        #PANEL 4: INTERACTIVE SIMULATION
        panel_sim = NeonPanel("Interactive Simulation")
        sim_layout = QHBoxLayout()
        sim_layout.setSpacing(20)
        
        #Inputs
        input_group = QVBoxLayout()
        
        lbl_edges = QLabel("Define Edges (Format: A-B:5, B-C:10)")
        lbl_edges.setStyleSheet(f"color: {COLOR_ACCENT}; font-weight: bold;")
        self.txt_edges = QLineEdit()
        self.txt_edges.setPlaceholderText("Contoh: A-B:4, A-C:2, B-C:5, C-D:3")
        self.txt_edges.setStyleSheet(self._input_style())
        
        path_layout = QHBoxLayout()
        self.txt_start = QLineEdit()
        self.txt_start.setPlaceholderText("Start (e.g. A)")
        self.txt_start.setStyleSheet(self._input_style())
        
        self.txt_end = QLineEdit()
        self.txt_end.setPlaceholderText("End (e.g. D)")
        self.txt_end.setStyleSheet(self._input_style())
        
        path_layout.addWidget(self.txt_start)
        path_layout.addWidget(self.txt_end)
        
        btn_calc = QPushButton("Find Shortest Path")
        btn_calc.setCursor(Qt.PointingHandCursor)
        btn_calc.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLOR_ACCENT}; color: black;
                font-weight: bold; border-radius: 8px; padding: 10px;
            }}
            QPushButton:hover {{ background-color: #00b8cc; }}
        """)
        btn_calc.clicked.connect(self.handle_calculate)
        
        input_group.addWidget(lbl_edges)
        input_group.addWidget(self.txt_edges)
        input_group.addLayout(path_layout)
        input_group.addWidget(btn_calc)
        input_group.addStretch()
        
        # Log Output
        log_group = QVBoxLayout()
        lbl_log = QLabel("Result Summary")
        lbl_log.setStyleSheet(f"color: {COLOR_ACCENT}; font-weight: bold;")
        
        self.txt_log = QTextEdit()
        self.txt_log.setReadOnly(True)
        self.txt_log.setStyleSheet(f"""
            QTextEdit {{
                background-color: #0f172a; border: 1px solid #334155;
                color: #00ff00; font-family: Consolas; border-radius: 8px; padding: 10px;
                font-size: 14px;
            }}
        """)
        
        log_group.addWidget(lbl_log)
        log_group.addWidget(self.txt_log)
        
        sim_layout.addLayout(input_group, 3)
        sim_layout.addLayout(log_group, 2)
        panel_sim.layout.addLayout(sim_layout)
        content_layout.addWidget(panel_sim)
        
        #PANEL 5: STEP-BY-STEP SOLUTION
        panel_steps = CollapsibleNeonPanel("Step-by-Step Solution")
        panel_steps.toggle_content() 
        
        self.txt_steps = QTextEdit()
        self.txt_steps.setReadOnly(True)
        self.txt_steps.setPlaceholderText("Langkah-langkah penyelesaian akan muncul di sini...")
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
        
        #PANEL 6: GENERATED VISUALIZATION
        panel_tree = NeonPanel("Generated Graph Visualization")
        self.graph_canvas = DynamicGraphCanvas()
        panel_tree.add_content(self.graph_canvas)
        content_layout.addWidget(panel_tree)
        
        content_layout.addStretch()
        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)

    def _input_style(self):
        return f"""
            QLineEdit {{
                background-color: #0f172a; border: 1px solid #334155;
                color: white; border-radius: 8px; padding: 10px; font-size: 14px;
            }}
            QLineEdit:focus {{ border: 1px solid {COLOR_ACCENT}; }}
        """

    def handle_calculate(self):
        self.logic.clear()
        self.txt_log.clear()
        self.txt_steps.clear()
        
        raw_edges = self.txt_edges.text().strip().upper()
        start_node = self.txt_start.text().strip().upper()
        end_node = self.txt_end.text().strip().upper()
        
        if not raw_edges or not start_node or not end_node:
            self.txt_log.setText("⚠️ Error: Mohon isi Edges, Start, dan End node.")
            return

        matches = re.findall(r'([A-Z0-9]+)\s*[-]\s*([A-Z0-9]+)\s*[:]\s*(\d+)', raw_edges)
        
        if not matches:
             self.txt_log.setText("⚠️ Error: Format edges salah.\nGunakan format: A-B:5, B-C:3")
             return

        for u, v, w in matches:
            self.logic.add_edge(u, v, int(w))
            
        path, dist, all_dist = self.logic.get_shortest_path(start_node, end_node)
        
        self.graph_canvas.set_data(self.logic, path)
        self.txt_steps.setHtml("<br>".join(self.logic.steps_log))
        
        if dist == float('inf'):
            self.txt_log.append(f"❌ Tidak ada jalur dari {start_node} ke {end_node}.")
        else:
            path_str = " -> ".join(path)
            self.txt_log.append(f"✅ Jalur Terpendek ({start_node} → {end_node}):")
            self.txt_log.append(f"   Path: {path_str}")
            self.txt_log.append(f"   Total Jarak: {dist}")
            self.txt_log.append("\n📊 Jarak ke node lain:")
            for node, d in all_dist.items():
                if d != float('inf'):
                    self.txt_log.append(f"   - {node}: {d}")

# TESTING
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DijkstraPage()
    window.setWindowTitle("Dijkstra Page")
    window.resize(1200, 900)
    window.show()
    sys.exit(app.exec())

