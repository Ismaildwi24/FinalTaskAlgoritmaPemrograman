"""
Implementasi Binary Tree Traversal (PreOrder, InOrder, PostOrder)
"""
from algorithms.bst import BSTNode, BinarySearchTree


class BinaryTreeTraversal:
    """Kelas untuk implementasi traversal pada binary tree"""
    
    def __init__(self):
        self.tree = None
        self.preorder_result = []
        self.inorder_result = []
        self.postorder_result = []
        self.steps = []
    
    def build_tree(self, values):
        """
        Membangun BST dari list nilai
        """
        self.tree = BinarySearchTree()
        self.tree.build_from_list(values)
        self.steps = self.tree.get_steps()
        return self.tree.root
    
    def preorder(self, node):
        """
        PreOrder Traversal: Root -> Left -> Right
        """
        if node is None:
            return []
        
        result = []
        result.append(node.value)  # Root
        result.extend(self.preorder(node.left))  # Left
        result.extend(self.preorder(node.right))  # Right
        
        return result
    
    def inorder(self, node):
        """
        InOrder Traversal: Left -> Root -> Right
        """
        if node is None:
            return []
        
        result = []
        result.extend(self.inorder(node.left))  # Left
        result.append(node.value)  # Root
        result.extend(self.inorder(node.right))  # Right
        
        return result
    
    def postorder(self, node):
        """
        PostOrder Traversal: Left -> Right -> Root
        """
        if node is None:
            return []
        
        result = []
        result.extend(self.postorder(node.left))  # Left
        result.extend(self.postorder(node.right))  # Right
        result.append(node.value)  # Root
        
        return result
    
    def traverse_all(self, root):
        """
        Melakukan semua jenis traversal dan menyimpan hasil
        """
        self.preorder_result = self.preorder(root)
        self.inorder_result = self.inorder(root)
        self.postorder_result = self.postorder(root)
        
        return {
            'preorder': self.preorder_result,
            'inorder': self.inorder_result,
            'postorder': self.postorder_result
        }
    
    def get_explanation(self):
        """Mengembalikan penjelasan untuk setiap jenis traversal"""
        explanations = {
            'preorder': {
                'name': 'PreOrder Traversal',
                'order': 'Root → Left → Right',
                'description': 'Kunjungi root terlebih dahulu, lalu subtree kiri, kemudian subtree kanan.'
            },
            'inorder': {
                'name': 'InOrder Traversal',
                'order': 'Left → Root → Right',
                'description': 'Kunjungi subtree kiri terlebih dahulu, lalu root, kemudian subtree kanan. Pada BST, hasilnya akan terurut.'
            },
            'postorder': {
                'name': 'PostOrder Traversal',
                'order': 'Left → Right → Root',
                'description': 'Kunjungi subtree kiri terlebih dahulu, lalu subtree kanan, kemudian root.'
            }
        }
        return explanations
