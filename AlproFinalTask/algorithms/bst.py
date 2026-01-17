class BSTNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class BinarySearchTree:
    def __init__(self):
        self.root = None
        self.steps = []  # menyimpan log langkah-langkah

    def insert(self, value):
        """
        Insert satu nilai ke BST dan simpan langkahnya.
        """
        if self.root is None:
            self.root = BSTNode(value)
            self.steps.append(f"Tree kosong → {value} dijadikan root.")
        else:
            self._insert_recursive(self.root, value)

    def _insert_recursive(self, current, value):
        if value < current.value:
            self.steps.append(
                f"{value} < {current.value} → bergerak ke KIRI"
            )
            if current.left is None:
                current.left = BSTNode(value)
                self.steps.append(
                    f"Node kiri kosong → {value} ditambahkan sebagai anak kiri {current.value}"
                )
            else:
                self._insert_recursive(current.left, value)

        elif value > current.value:
            self.steps.append(
                f"{value} > {current.value} → bergerak ke KANAN"
            )
            if current.right is None:
                current.right = BSTNode(value)
                self.steps.append(
                    f"Node kanan kosong → {value} ditambahkan sebagai anak kanan {current.value}"
                )
            else:
                self._insert_recursive(current.right, value)

        else:
            self.steps.append(
                f"{value} sudah ada di BST → dilewati (tidak ditambahkan)"
            )

    def build_from_list(self, values):
        """
        Bangun BST dari list angka.
        """
        self.steps.clear()
        for v in values:
            self.steps.append(f"\nMemasukkan {v}:")
            self.insert(v)

    def get_steps(self):
        return self.steps
