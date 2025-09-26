# KeepActive Utility

## Deskripsi
KeepActive adalah sebuah aplikasi desktop sederhana untuk Windows yang membantu menjaga aplikasi lain tetap "aktif". Aplikasi ini menyimulasikan gerakan mouse kecil pada interval waktu yang ditentukan jika jendela aplikasi yang dipilih sedang aktif. Ini berguna untuk mencegah aplikasi atau sistem menandai Anda sebagai "tidak aktif" atau "away".

## Fitur
- Menampilkan daftar semua jendela aplikasi yang sedang berjalan.
- Memungkinkan pemilihan beberapa aplikasi menggunakan kotak centang.
- Interval waktu yang dapat disesuaikan untuk simulasi aktivitas.
- Antarmuka yang sederhana dan mudah digunakan.

## Cara Kerja
Aplikasi ini secara berkala memeriksa apakah jendela yang sedang aktif adalah salah satu dari jendela yang telah Anda pilih. Jika ya, aplikasi akan menggerakkan mouse sejauh satu piksel ke kanan dan kemudian kembali ke kiri. Gerakan kecil ini cukup untuk memberi sinyal kepada sebagian besar sistem operasi dan aplikasi bahwa pengguna masih aktif, tanpa mengganggu pekerjaan Anda.

## Aplikasi Siap Pakai
**Aplikasi yang sudah jadi dan bisa langsung dijalankan (`KeepActive.exe`) tersedia di dalam folder `dist`. Anda bisa langsung menggunakan aplikasi dari sana tanpa perlu melakukan instalasi.**

## Instalasi (Untuk Pengembangan)
Jika Anda ingin menjalankan atau mengembangkan aplikasi ini dari kode sumbernya, Anda perlu menginstal beberapa pustaka Python.

1.  **Pastikan Python terinstal:** Anda memerlukan Python 3.x.
2.  **Clone repositori ini (jika ada) atau unduh file-filenya.**
3.  **Instal dependensi:** Buka terminal atau command prompt di direktori proyek dan jalankan perintah berikut:
    ```bash
    pip install -r requirements.txt
    ```

## Menjalankan dari Kode Sumber
Setelah dependensi terinstal, Anda dapat menjalankan aplikasi dengan perintah:
```bash
python app_builder.py
```

## Membangun Aplikasi (Build)
Proyek ini menggunakan `PyInstaller` untuk membuat file `.exe`. Jika Anda ingin membangun ulang aplikasi:
1.  Instal PyInstaller:
    ```bash
    pip install pyinstaller
    ```
2.  Jalankan perintah build dari direktori proyek:
    ```bash
    pyinstaller KeepActive.spec
    ```
    File `.exe` yang baru akan dibuat di dalam folder `dist`.
