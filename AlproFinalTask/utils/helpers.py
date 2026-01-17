"""
Helper functions untuk berbagai operasi umum
"""
import re
from typing import List, Tuple, Optional


def parse_numbers(text: str) -> List[int]:
    """
    Parse string angka yang dipisahkan koma menjadi list integer
    Contoh: "10, 5, 20" -> [10, 5, 20]
    """
    if not text or not text.strip():
        return []
    
    numbers = []
    for part in text.split(','):
        part = part.strip()
        if part:
            try:
                numbers.append(int(part))
            except ValueError:
                continue
    
    return numbers


def format_tree_visualization(root, prefix: str = "", is_last: bool = True) -> str:
    """
    Format visualisasi binary tree dalam format text
    """
    if root is None:
        return ""
    
    result = prefix + ("└── " if is_last else "├── ") + str(root.value) + "\n"
    prefix += "    " if is_last else "│   "
    
    if root.left or root.right:
        if root.right:
            result += format_tree_visualization(root.right, prefix, root.left is None)
        if root.left:
            result += format_tree_visualization(root.left, prefix, True)
    
    return result


def format_graph_edges(edges_text: str) -> List[Tuple[str, str, float]]:
    """
    Parse string edges graf menjadi list tuple (node1, node2, weight)
    Contoh: "A-B:5,B-C:3" -> [("A", "B", 5.0), ("B", "C", 3.0)]
    """
    edges = []
    if not edges_text or not edges_text.strip():
        return edges
    
    for edge in edges_text.split(','):
        edge = edge.strip()
        if not edge:
            continue
        
        if ':' not in edge or '-' not in edge:
            continue
        
        try:
            parts = edge.split(':')
            if len(parts) != 2:
                continue
            
            weight = float(parts[1].strip())
            nodes_part = parts[0].split('-')
            if len(nodes_part) != 2:
                continue
            
            node1 = nodes_part[0].strip()
            node2 = nodes_part[1].strip()
            edges.append((node1, node2, weight))
        except ValueError:
            continue
    
    return edges


def format_output_lines(lines: List[str], separator: str = "\n") -> str:
    """
    Format list string menjadi satu string dengan separator
    """
    return separator.join(str(line) for line in lines if line)


def sanitize_text(text: str) -> str:
    """
    Sanitize text input untuk menghindari karakter berbahaya
    """
    if not text:
        return ""
    
    # Hapus karakter kontrol kecuali newline dan tab
    text = re.sub(r'[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F]', '', text)
    
    return text.strip()


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Truncate text jika terlalu panjang
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix


def format_frequency_table(frequency: dict) -> List[Tuple[str, int]]:
    """
    Format frequency dictionary menjadi list tuple yang terurut
    """
    return sorted(frequency.items(), key=lambda x: (-x[1], x[0]))


def format_huffman_output(codes: dict) -> List[str]:
    """
    Format kode Huffman menjadi list string output
    Contoh: {'A': '01', 'B': '10'} -> ['A=01', 'B=10']
    """
    return [f"{char}={code}" for char, code in sorted(codes.items())]