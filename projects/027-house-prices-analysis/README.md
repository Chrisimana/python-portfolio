# House Prices Analysis

![Status](https://img.shields.io/badge/status-selesai-brightgreen)

## Deskripsi Proyek
House Prices Analysis adalah skrip Python yang menganalisis dan memvisualisasikan faktor-faktor yang memengaruhi harga rumah, menggunakan dataset contoh (dummy) yang mencakup luas bangunan, jumlah kamar tidur, kamar mandi, usia bangunan, dan jarak ke pusat kota. Proyek ini menyelesaikan masalah memahami hubungan antar variabel dalam dataset properti secara visual, sebuah langkah awal yang umum dilakukan sebelum membangun model prediksi harga rumah (misalnya regresi linear berganda).

## Fitur Utama
- Dataset contoh berisi 300 data rumah dengan enam fitur numerik, dibuat dengan hubungan yang realistis antar variabel beserta noise acak
- Heatmap korelasi menampilkan kekuatan hubungan antar seluruh pasangan fitur numerik sekaligus dalam satu visualisasi
- Scatter plot beserta garis regresi untuk melihat hubungan spesifik antara luas bangunan dan harga rumah
- Boxplot yang menampilkan sebaran harga rumah berdasarkan jumlah kamar tidur, membantu melihat pengaruh fitur kategorikal terhadap harga
- Ringkasan statistik deskriptif seluruh fitur ditampilkan di terminal sebelum grafik muncul

## Teknologi yang Digunakan
- Python 3.x
- NumPy
- Pandas
- Matplotlib
- Seaborn

## Arsitektur
Skrip ini berjalan secara prosedural dengan empat fungsi utama:
1. `generate_sample_data()` membuat dataset dummy menggunakan distribusi acak untuk setiap fitur (luas bangunan, kamar tidur, kamar mandi, usia, jarak ke kota), lalu menghitung harga rumah berdasarkan kombinasi linear dari seluruh fitur tersebut ditambah noise acak, sehingga pola korelasi antar variabel terlihat realistis.
2. `plot_correlation_heatmap()` menghitung matriks korelasi menggunakan `DataFrame.corr()`, lalu memvisualisasikannya sebagai heatmap menggunakan `sns.heatmap()` dengan anotasi nilai korelasi pada setiap sel.
3. `plot_price_vs_sqft()` menggambar scatter plot beserta garis regresi menggunakan `sns.regplot()` untuk menyoroti hubungan antara luas bangunan dan harga, fitur yang biasanya memiliki korelasi terkuat terhadap harga rumah.
4. `plot_price_by_bedrooms()` menggambar boxplot menggunakan `sns.boxplot()` untuk membandingkan distribusi harga rumah pada setiap kategori jumlah kamar tidur.

Alur utamanya di `main()`: data dummy dibuat → ringkasan statistik ditampilkan ke terminal → ketiga grafik (heatmap korelasi, regresi harga vs luas, boxplot harga vs kamar tidur) ditampilkan berurutan lewat jendela pop-up Matplotlib.

## Pembelajaran Spesifik
- Menggunakan `DataFrame.corr()` bersama `sns.heatmap()` sebagai kombinasi standar untuk mengeksplorasi hubungan antar banyak variabel numerik sekaligus, jauh lebih efisien dibandingkan membuat scatter plot untuk setiap pasangan fitur secara manual.
- Memahami bahwa korelasi yang ditampilkan heatmap hanya mengukur hubungan linear, sehingga tetap perlu divalidasi dengan visualisasi tambahan seperti scatter plot untuk melihat bentuk hubungan yang sesungguhnya.
- Menerapkan kombinasi beberapa variabel dengan bobot koefisien berbeda saat membuat data dummy, teknik yang berguna untuk mensimulasikan dataset realistis ketika data asli belum tersedia.
- Menggunakan `clip()` pada array NumPy untuk membatasi nilai dalam rentang yang masuk akal (misalnya mencegah harga rumah bernilai negatif akibat noise acak yang terlalu besar).
- Memilih jenis visualisasi yang sesuai dengan tipe data: heatmap untuk hubungan antar banyak variabel numerik, scatter plot dengan regresi untuk hubungan dua variabel numerik, dan boxplot untuk membandingkan distribusi numerik terhadap variabel kategorikal/diskret.