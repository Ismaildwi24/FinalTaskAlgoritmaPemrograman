"""
Modul untuk validasi input user
"""
from PySide6.QtWidgets import QMessageBox


class Validator:
    """Kelas untuk validasi berbagai jenis input"""
    
    @staticmethod
    def validate_huffman_input(text):
        """
        Validasi input untuk Huffman Coding
        - Tidak boleh kosong
        - Hanya alfabet dan spasi
        """
        if not text or not text.strip():
            return False, "Input tidak boleh kosong!"
        
        # Hanya alfabet dan spasi yang diperbolehkan
        if not all(c.isalpha() or c.isspace() for c in text):
            return False, "Input hanya boleh mengandung huruf dan spasi!"
        
        return True, ""
    
    @staticmethod
    def validate_bst_input(text):
        """
        Validasi input untuk Binary Search Tree
        - Deretan angka dipisahkan koma
        """
        if not text or not text.strip():
            return False, "Input tidak boleh kosong!"
        
        try:
            # Split dan parse angka
            parts = text.split(',')
            numbers = []
            for part in parts:
                part = part.strip()
                if part:
                    num = int(part)
                    numbers.append(num)
            
            if not numbers:
                return False, "Minimal harus ada satu angka!"
            
            return True, ""
        except ValueError:
            return False, "Input harus berupa angka yang dipisahkan koma (contoh: 5,3,7,1,9)!"
    
    @staticmethod
    def validate_traversal_input(text):
        """
        Validasi input untuk Binary Tree Traversal
        - Sama seperti BST (deretan angka)
        """
        return Validator.validate_bst_input(text)
    
    @staticmethod
    def validate_dijkstra_graph(edges_text, source_text):
        """
        Validasi input untuk Dijkstra
        - Format: node1-node2:weight,node2-node3:weight
        - Source harus ada di graph
        """
        if not edges_text or not edges_text.strip():
            return False, "Input graf tidak boleh kosong!"
        
        if not source_text or not source_text.strip():
            return False, "Node awal tidak boleh kosong!"
        
        try:
            edges = edges_text.split(',')
            nodes = set()
            
            for edge in edges:
                edge = edge.strip()
                if not edge:
                    continue
                
                if ':' not in edge or '-' not in edge:
                    return False, "Format salah! Gunakan: node1-node2:weight (contoh: A-B:5,B-C:3)"
                
                parts = edge.split(':')
                if len(parts) != 2:
                    return False, "Format bobot salah! Gunakan: node1-node2:weight"
                
                weight = float(parts[1].strip())
                if weight <= 0:
                    return False, "Bobot harus bilangan positif!"
                
                nodes_part = parts[0].split('-')
                if len(nodes_part) != 2:
                    return False, "Format edge salah! Gunakan: node1-node2:weight"
                
                nodes.add(nodes_part[0].strip())
                nodes.add(nodes_part[1].strip())
            
            if source_text.strip() not in nodes:
                return False, f"Node awal '{source_text.strip()}' tidak ditemukan dalam graf!"
            
            return True, ""
        except ValueError:
            return False, "Bobot harus berupa angka!"
    
    @staticmethod
    def show_error(parent, message):
        """Menampilkan pesan error menggunakan QMessageBox"""
        msg = QMessageBox(parent)
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Input Tidak Valid")
        msg.setText(message)
        msg.exec()