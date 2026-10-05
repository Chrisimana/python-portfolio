# Seaborn Regression Plot

![Status](https://img.shields.io/badge/status-selesai-brightgreen)

## Deskripsi Proyek
Seaborn Regression Plot adalah skrip Python yang memvisualisasikan hubungan antara dua variabel numerik menggunakan scatter plot beserta garis regresi linear, dibangun dengan library Seaborn dan Matplotlib. Dataset yang digunakan berupa data contoh (dummy) yang merepresentasikan hubungan antara jam belajar per hari dengan nilai ujian. Proyek ini menyelesaikan masalah memvisualisasikan serta mengidentifikasi pola hubungan linear antar variabel secara cepat dan intuitif, salah satu teknik dasar dalam exploratory data analysis (EDA).

## Fitur Utama
- Data contoh dibuat secara terprogram menggunakan distribusi acak yang realistis, termasuk noise agar polanya tidak terlalu sempurna
- Scatter plot menampilkan sebaran data asli, membantu melihat variasi data di sekitar garis tren
- Garis regresi linear dihitung dan digambar otomatis oleh `sns.regplot()`, lengkap dengan area interval kepercayaan (confidence interval)
- Ringkasan statistik deskriptif (`describe()`) ditampilkan di terminal sebelum grafik muncul
- Tampilan grafik menggunakan tema Seaborn yang bersih (`whitegrid`) dengan label sumbu dan judul yang informatif

## Teknologi yang Digunakan
- Python 3.x
- NumPy
- Pandas
- Matplotlib
- Seaborn

## Arsitektur
Skrip ini berjalan secara prosedural dengan dua fungsi utama:
1. `generate_sample_data()` membuat dataset dummy menggunakan `numpy.random.default_rng()` untuk menghasilkan nilai jam belajar secara acak, lalu menghitung nilai ujian berdasarkan hubungan linear sederhana ditambah noise acak, sehingga pola hubungan antar variabel terlihat realistis namun tidak sempurna.
2. `plot_regression()` menerima DataFrame hasil `generate_sample_data()`, lalu menggambar scatter plot beserta garis regresi menggunakan `sns.regplot()`, dengan parameter `scatter_kws` dan `line_kws` untuk menyesuaikan gaya visual titik data dan garis regresi secara terpisah.

Alur utamanya di `main()`: data dummy dibuat → ringkasan statistik ditampilkan ke terminal → grafik regresi ditampilkan lewat jendela pop-up Matplotlib menggunakan `plt.show()`.

## Pembelajaran Spesifik
- Memahami perbedaan antara `sns.regplot()` (untuk satu plot sederhana pada satu axes) dan `sns.lmplot()` (untuk plot yang mendukung facet/pemisahan kategori), serta kapan masing-masing lebih tepat digunakan.
- Menerapkan `numpy.random.default_rng()` dengan seed tetap untuk menghasilkan data acak yang dapat direproduksi, penting agar hasil visualisasi konsisten setiap kali skrip dijalankan ulang.
- Menggunakan parameter `scatter_kws` dan `line_kws` untuk mengustomisasi elemen visual tertentu dalam satu fungsi plotting Seaborn, tanpa perlu menggambar scatter plot dan garis regresi secara terpisah.
- Memahami bahwa garis regresi pada `regplot()` otomatis disertai area bayangan yang merepresentasikan interval kepercayaan, memberi gambaran seberapa yakin model terhadap prediksinya di berbagai titik.