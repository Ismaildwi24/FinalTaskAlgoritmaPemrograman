"""
Implementasi algoritma Huffman Coding
"""
from collections import Counter
from heapq import heappush, heappop


class HuffmanNode:
    """Node untuk pohon Huffman"""
    def __init__(self, char=None, freq=0, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right
    
    def __lt__(self, other):
        return self.freq < other.freq


class HuffmanCoding:
    """Kelas untuk implementasi Huffman Coding"""
    
    def __init__(self):
        self.codes = {}
        self.steps = []
        self.frequency = {}
    
    def build_tree(self, text):
        """
        Membangun pohon Huffman dari teks input
        Mengembalikan root node dan menyimpan langkah-langkah
        """
        self.steps.clear()
        self.codes.clear()
        
        # Hitung frekuensi karakter
        self.frequency = Counter(text)
        self.steps.append("=== Langkah 1: Menghitung Frekuensi Karakter ===")
        for char, freq in sorted(self.frequency.items()):
            self.steps.append(f"  '{char}': {freq}")
        
        if len(self.frequency) == 1:
            # Kasus khusus: hanya satu karakter
            char = list(self.frequency.keys())[0]
            self.codes[char] = "0"
            self.steps.append(f"\n=== Hasil: Kode untuk '{char}' adalah '0' ===")
            return HuffmanNode(char, self.frequency[char])
        
        # Buat priority queue (min heap)
        heap = []
        self.steps.append("\n=== Langkah 2: Membuat Priority Queue ===")
        for char, freq in self.frequency.items():
            node = HuffmanNode(char, freq)
            heappush(heap, node)
            self.steps.append(f"  Menambahkan node '{char}' dengan frekuensi {freq}")
        
        # Bangun pohon Huffman
        self.steps.append("\n=== Langkah 3: Membangun Pohon Huffman ===")
        step_num = 1
        
        while len(heap) > 1:
            # Ambil dua node dengan frekuensi terkecil
            left = heappop(heap)
            right = heappop(heap)
            
            self.steps.append(f"\n  Iterasi {step_num}:")
            self.steps.append(f"    Mengambil dua node terkecil:")
            self.steps.append(f"      - Node 1: '{left.char if left.char else 'Internal'}' (freq: {left.freq})")
            self.steps.append(f"      - Node 2: '{right.char if right.char else 'Internal'}' (freq: {right.freq})")
            
            # Buat node internal baru
            merged = HuffmanNode(
                char=None,
                freq=left.freq + right.freq,
                left=left,
                right=right
            )
            
            self.steps.append(f"    Membuat node internal dengan frekuensi {merged.freq}")
            self.steps.append(f"      - Kiri: '{left.char if left.char else 'Internal'}'")
            self.steps.append(f"      - Kanan: '{right.char if right.char else 'Internal'}'")
            
            heappush(heap, merged)
            step_num += 1
        
        root = heap[0]
        self.steps.append(f"\n=== Langkah 4: Root node memiliki frekuensi total {root.freq} ===")
        
        # Generate kode Huffman
        self._generate_codes(root, "")
        
        self.steps.append("\n=== Langkah 5: Tabel Kode Huffman ===")
        for char, code in sorted(self.codes.items()):
            self.steps.append(f"  '{char}': {code}")
        
        return root
    
    def _generate_codes(self, node, code):
        """Generate kode Huffman secara rekursif"""
        if node.char is not None:
            # Leaf node
            if code == "":
                code = "0"  # Kasus khusus untuk satu karakter
            self.codes[node.char] = code
            return
        
        # Traverse ke kiri (tambahkan '0')
        if node.left:
            self._generate_codes(node.left, code + "0")
        
        # Traverse ke kanan (tambahkan '1')
        if node.right:
            self._generate_codes(node.right, code + "1")
    
    def encode(self, text):
        """Encode teks menggunakan kode Huffman"""
        encoded = ""
        for char in text:
            if char in self.codes:
                encoded += self.codes[char]
            else:
                encoded += char  # Fallback jika karakter tidak ada
        
        return encoded
    
    def get_frequency(self):
        """Mengembalikan dictionary frekuensi karakter"""
        return self.frequency
    
    def get_codes(self):
        """Mengembalikan dictionary kode Huffman"""
        return self.codes
    
    def get_steps(self):
        """Mengembalikan list langkah-langkah"""
        return self.steps
