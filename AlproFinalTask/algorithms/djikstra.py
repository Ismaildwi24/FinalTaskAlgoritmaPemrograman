"""
Implementasi Algoritma Dijkstra untuk mencari jalur terpendek
"""
import math


class Dijkstra:
    """Kelas untuk implementasi algoritma Dijkstra"""
    
    def __init__(self):
        self.graph = {}
        self.distances = {}
        self.previous = {}
        self.visited = set()
        self.steps = []
    
    def build_graph(self, edges_text):
        """
        Membangun graf dari string input
        Format: "A-B:5,B-C:3,C-D:2"
        """
        self.graph.clear()
        self.steps.clear()
        
        edges = edges_text.split(',')
        self.steps.append("=== Langkah 1: Membangun Graf ===")
        
        for edge in edges:
            edge = edge.strip()
            if not edge:
                continue
            
            parts = edge.split(':')
            if len(parts) != 2:
                continue
            
            nodes_part = parts[0].strip()
            weight = float(parts[1].strip())
            
            if '-' in nodes_part:
                node1, node2 = nodes_part.split('-')
                node1 = node1.strip()
                node2 = node2.strip()
                
                if node1 not in self.graph:
                    self.graph[node1] = {}
                if node2 not in self.graph:
                    self.graph[node2] = {}
                
                # Graf tidak berarah (bidirectional)
                self.graph[node1][node2] = weight
                self.graph[node2][node1] = weight
                
                self.steps.append(f"  Edge: {node1} ↔ {node2} (bobot: {weight})")
        
        self.steps.append(f"\nTotal node: {len(self.graph)}")
        return self.graph
    
    def find_shortest_path(self, source):
        """
        Mencari jalur terpendek dari source ke semua node lainnya
        """
        if source not in self.graph:
            return None
        
        # Inisialisasi
        self.distances = {node: float('inf') for node in self.graph}
        self.distances[source] = 0
        self.previous = {node: None for node in self.graph}
        self.visited = set()
        
        self.steps.append(f"\n=== Langkah 2: Inisialisasi ===")
        self.steps.append(f"  Node awal: {source}")
        self.steps.append(f"  Jarak awal: {self.distances}")
        
        iteration = 1
        
        while len(self.visited) < len(self.graph):
            # Pilih node dengan jarak terkecil yang belum dikunjungi
            unvisited = {k: v for k, v in self.distances.items() if k not in self.visited}
            if not unvisited:
                break
            
            current = min(unvisited, key=unvisited.get)
            current_distance = self.distances[current]
            
            self.steps.append(f"\n=== Iterasi {iteration} ===")
            self.steps.append(f"  Node terpilih: {current} (jarak: {current_distance})")
            
            self.visited.add(current)
            
            # Update jarak ke tetangga
            neighbors_updated = []
            for neighbor, weight in self.graph[current].items():
                if neighbor not in self.visited:
                    new_distance = current_distance + weight
                    if new_distance < self.distances[neighbor]:
                        old_distance = self.distances[neighbor]
                        self.distances[neighbor] = new_distance
                        self.previous[neighbor] = current
                        neighbors_updated.append(
                            f"    {neighbor}: {old_distance} → {new_distance} (via {current})"
                        )
            
            if neighbors_updated:
                self.steps.append("  Update jarak tetangga:")
                self.steps.extend(neighbors_updated)
            else:
                self.steps.append("  Tidak ada update jarak")
            
            iteration += 1
        
        self.steps.append(f"\n=== Selesai: Semua node telah dikunjungi ===")
        return self.distances
    
    def get_path(self, target):
        """
        Mengembalikan jalur dari source ke target
        """
        if target not in self.previous:
            return []
        
        path = []
        current = target
        
        while current is not None:
            path.insert(0, current)
            current = self.previous.get(current)
        
        return path
    
    def get_all_paths(self, source):
        """
        Mengembalikan semua jalur dari source ke setiap node
        """
        paths = {}
        for node in self.graph:
            if node != source:
                path = self.get_path(node)
                if path:
                    paths[node] = {
                        'path': path,
                        'distance': self.distances[node]
                    }
        return paths
    
    def get_steps(self):
        """Mengembalikan list langkah-langkah"""
        return self.steps
