# Handwashing Analysis

![Status](https://img.shields.io/badge/status-selesai-brightgreen)

## Deskripsi Proyek
Handwashing Analysis adalah skrip Python yang menganalisis dan memvisualisasikan dampak kebijakan cuci tangan terhadap angka kematian ibu melahirkan, terinspirasi dari kasus historis penemuan Dr. Ignaz Semmelweis di Rumah Sakit Umum Wina pada abad ke-19. Dataset yang digunakan berupa data bulanan contoh (dummy) yang meniru pola data asli: angka kematian tinggi sebelum kebijakan cuci tangan diterapkan, lalu menurun drastis sesudahnya. Proyek ini menyelesaikan masalah memvalidasi dan mengomunikasikan dampak sebuah intervensi (kebijakan cuci tangan) secara visual menggunakan data time-series, salah satu bentuk analisis data historis yang umum dalam epidemiologi.

## Fitur Utama
- Data bulanan contoh dibuat dari tahun 1841 hingga 1849, meniru periode sebelum dan sesudah kebijakan cuci tangan diterapkan pada Juni 1847
- Angka kematian dihitung sebagai persentase dari jumlah kelahiran dan kematian setiap bulan
- Grafik tren garis (line plot) menampilkan perubahan angka kematian dari waktu ke waktu, dengan garis vertikal penanda tanggal kebijakan mulai diterapkan
- Grafik boxplot membandingkan distribusi angka kematian antara periode sebelum dan sesudah kebijakan secara berdampingan
- Ringkasan rata-rata angka kematian sebelum dan sesudah kebijakan ditampilkan langsung di terminal sebagai konteks numerik

## Teknologi yang Digunakan
- Python 3.x
- NumPy
- Pandas
- Matplotlib
- Seaborn

## Arsitektur
Skrip ini berjalan secara prosedural dengan tiga fungsi utama:
1. `generate_sample_data()` membuat data bulanan dari 1841 hingga 1849 menggunakan `pandas.date_range()`, dengan angka kematian yang sengaja dibuat jauh lebih tinggi pada periode sebelum `HANDWASHING_START` dan jauh lebih rendah sesudahnya, mensimulasikan efek nyata dari kebijakan tersebut.
2. `plot_death_rate_trend()` menggambar grafik garis menggunakan `sns.lineplot()` untuk menunjukkan tren angka kematian dari waktu ke waktu, ditambah `plt.axvline()` sebagai penanda visual kapan kebijakan cuci tangan mulai diterapkan.
3. `plot_before_after_comparison()` mengelompokkan data menjadi dua kategori (sebelum/sesudah) menggunakan `numpy.where()`, lalu menggambar boxplot perbandingan menggunakan `sns.boxplot()` untuk menyoroti perbedaan distribusi secara lebih ringkas dibanding grafik garis.

Alur utamanya di `main()`: data dummy dibuat → rata-rata angka kematian sebelum dan sesudah kebijakan dihitung dan ditampilkan ke terminal → kedua grafik (tren garis dan boxplot perbandingan) ditampilkan berurutan lewat jendela pop-up Matplotlib.

## Pembelajaran Spesifik
- Menggunakan `pandas.date_range()` dengan frekuensi `"MS"` (month start) untuk menghasilkan deret tanggal bulanan secara presisi, teknik dasar saat bekerja dengan data time-series.
- Menerapkan `plt.axvline()` sebagai cara efektif menandai sebuah peristiwa penting (intervensi/kebijakan) langsung pada grafik tren, membantu audiens memahami konteks perubahan data tanpa penjelasan tambahan.
- Memahami kapan grafik garis (tren dari waktu ke waktu) lebih sesuai digunakan dibandingkan boxplot (perbandingan distribusi antar kelompok), dan bagaimana keduanya saling melengkapi dalam satu analisis.
- Menggunakan `numpy.where()` untuk membuat kolom kategori baru berdasarkan kondisi tanggal, teknik umum dalam feature engineering saat menyiapkan data untuk visualisasi maupun pemodelan.
- Menyadari pentingnya menampilkan ringkasan numerik (rata-rata) sebagai pelengkap visualisasi, karena angka yang konkret membantu memperkuat kesimpulan yang disampaikan oleh grafik.