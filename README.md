# 📘 Program Pembelajaran Algoritma Pemrograman

## 👥 Identitas Kelompok

**Tugas Kelompok – Ujian Akhir Semester (UAS)**
**Mata Kuliah**: Algoritma Pemrograman

| No | Nama                     | NIM             |
| -- | ------------------------ | --------------- |
| 1  | Tegar Tutu Empar Pranata | 202410370110008 |
| 2  | Ismail Dwi Muh. Anugerah | 202410370110013 |
| 3  | Akhmad Arjuan Syuhada    | 202410370110043 |

---

Aplikasi Pembelajaran Algoritma & Struktur Data adalah sebuah **aplikasi desktop edukatif berbasis Python** yang dirancang untuk membantu mahasiswa memahami konsep dasar algoritma dan struktur data secara **interaktif, visual, dan bertahap (step-by-step)**.

Aplikasi ini dikembangkan sebagai **tugas kelompok untuk memenuhi Ujian Akhir Semester (UAS)** pada mata kuliah **Algoritma Pemrograman**.

---

## 🎯 Tujuan Program

Tujuan utama dari aplikasi ini adalah:

* Membantu mahasiswa **memahami konsep algoritma dan struktur data** secara visual
* Menyediakan **simulasi interaktif** agar user dapat mencoba langsung algoritma yang dipelajari
* Menampilkan **proses langkah demi langkah** dari setiap algoritma
* Memberikan **validasi input** agar user memahami batasan data yang digunakan dalam algoritma

Aplikasi ini ditujukan khusus untuk **mahasiswa pemula** yang baru mempelajari Algoritma Pemrograman.

---

## 📚 Algoritma & Struktur Data yang Diimplementasikan

Aplikasi ini mengimplementasikan empat materi utama:

1. **Huffman Coding**

   * Analisis frekuensi karakter
   * Proses pembentukan pohon Huffman
   * Pembuatan kode biner Huffman
   * Hasil encoding teks

2. **Binary Search Tree (BST)**

   * Proses insert node
   * Visualisasi struktur pohon
   * Hubungan parent–child

3. **Binary Tree Traversal**

   * PreOrder Traversal
   * InOrder Traversal
   * PostOrder Traversal
   * Visualisasi urutan traversal

4. **Algoritma Dijkstra**

   * Graf berbobot
   * Penentuan jarak terpendek
   * Proses iteratif pemilihan node
   * Visualisasi jalur terpendek

---

## 🖥️ Fitur Utama Aplikasi

* ✅ Antarmuka **dark mode minimalis modern**
* ✅ Dibangun menggunakan **Python + customtkinter**
* ✅ Navigasi menggunakan **sidebar (Home, Back, Exit)**
* ✅ Setiap algoritma memiliki:

  * Penjelasan konsep
  * Ilustrasi visual
  * Contoh penerapan dunia nyata
  * Simulasi interaktif
* ✅ **Validasi input user** dengan alert jika input tidak sesuai
* ✅ Menampilkan **proses algoritma secara step-by-step**, bukan hanya hasil akhir

---

## 🧩 Struktur Halaman Aplikasi

1. **Halaman Awal (Welcome Page)**

   * Judul aplikasi
   * Deskripsi singkat
   * Tombol masuk

2. **Halaman Utama (Menu Pembelajaran)**

   * Pilihan algoritma:

     * Huffman Coding
     * Binary Search Tree
     * Binary Traversal
     * Algoritma Dijkstra
   * Tombol keluar

3. **Halaman Pembelajaran**

   * Penjelasan materi
   * Visualisasi algoritma
   * Penerapan dunia nyata
   * Area simulasi interaktif
   * Sidebar navigasi

---

## 🛠️ Teknologi yang Digunakan

* **Bahasa Pemrograman**: Python
* **UI Framework**: PySide6 (Qt for Python)
* **Styling UI**: Qt Style Sheet (QSS) – Dark Mode
* **Paradigma**: Modular, terpisah antara UI dan logika algoritma
* **Platform**: Desktop Application

---

## 📁 Struktur Proyek

Struktur folder proyek disusun secara modular untuk memisahkan **UI**, **logika algoritma**, dan **utilitas pendukung**, sehingga mudah dipahami dan dikembangkan.

```
AlproFinalTask/
│
├── main.py                  # Entry point (run app)
│
├── ui/
│   ├── __init__.py
│   │
│   ├── pages/               # Semua halaman aplikasi
│   │   ├── __init__.py
│   │   ├── welcome_page.py
│   │   ├── menu_page.py
│   │   ├── bst_page.py
│   │   ├── traversal_page.py
│   │   ├── huffman_page.py
│   │   └── dijkstra_page.py
│   │
│   ├── components/          # Komponen UI reusable
│   │   ├── __init__.py
│   │   ├── sidebar.py
│   │   ├── card.py
│     │   └── header.py
│   │
│   └── styles/
│       ├── __init__.py
│       └── dark.qss         # Styling dark mode (Qt CSS)
│
├── algorithms/              # Logika algoritma (tanpa UI)
│   ├── __init__.py
│   ├── bst.py
│   ├── traversal.py
│   ├── huffman.py
│   └── dijkstra.py
│
├── assets/                  # Asset visual
│   ├── icons/
│   └── images/
│
└── utils/
    ├── __init__.py
    ├── validator.py         # Validasi input user
    └── helpers.py
```

---

## 📌 Catatan

Aplikasi ini dikembangkan **murni untuk keperluan akademik** sebagai media pembelajaran Algoritma Pemrograman. Fokus utama aplikasi adalah **pemahaman konsep dan proses algoritma**, bukan optimasi performa tingkat lanjut.

---

## 🚀 Cara Menjalankan Program

Ikuti langkah-langkah berikut untuk menjalankan aplikasi ini di komputer Anda:

1. **Pastikan Python Terinstal**
   * Unduh dan instal Python versi terbaru dari [python.org](https://www.python.org/).
   * Pastikan Python sudah ditambahkan ke PATH.

2. **Instal Dependensi**
   * Buka terminal di direktori proyek.
   * Jalankan perintah berikut untuk menginstal dependensi:
     ```bash
     pip install -r requirements.txt
     ```

3. **Jalankan Aplikasi**
   * Jalankan perintah berikut di terminal:
     ```bash
     python main.py
     ```

4. **Navigasi di Aplikasi**
   * Gunakan sidebar untuk berpindah antar halaman.
   * Pilih algoritma yang ingin dipelajari.

---

## 🖼️ Tampilan Halaman Aplikasi

Berikut adalah beberapa tampilan halaman dari aplikasi ini:

1. **Halaman Awal (Welcome Page)**
   ![Welcome Page](https://github.com/Ismaildwi24/FinalTaskAlgoritmaPemrograman/blob/main/AlproFinalTask/assets/images/welcome_page.png)

2. **Halaman Menu Pembelajaran**
   ![Menu Page](https://github.com/Ismaildwi24/FinalTaskAlgoritmaPemrograman/blob/main/AlproFinalTask/assets/images/menu_page.png)

3. **Halaman Huffman Coding**
   ![Huffman Page](https://github.com/Ismaildwi24/FinalTaskAlgoritmaPemrograman/blob/main/AlproFinalTask/assets/images/huffman_page.png)

4. **Halaman Binary Search Tree**
   ![BST Page](https://github.com/Ismaildwi24/FinalTaskAlgoritmaPemrograman/blob/main/AlproFinalTask/assets/images/bst_page.png)

5. **Halaman Binary Traversal**
   ![Traversal Page](https://github.com/Ismaildwi24/FinalTaskAlgoritmaPemrograman/blob/main/AlproFinalTask/assets/images/traversal_page.png)

6. **Halaman Algoritma Dijkstra**
   ![Dijkstra Page](https://github.com/Ismaildwi24/FinalTaskAlgoritmaPemrograman/blob/main/AlproFinalTask/assets/images/dijkstra_page.png)

---

**Mata Kuliah**: Algoritma Pemrograman  
**Jenis Tugas**: Tugas Kelompok – Ujian Akhir Semester (UAS)
