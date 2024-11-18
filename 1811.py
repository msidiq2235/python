import tkinter as tk
from tkinter import messagebox
import sqlite3

# Koneksi SQLite
conn = sqlite3.connect('nilai_siswa.db')
cursor = conn.cursor()

# Membuat tabel jika belum ada
cursor.execute('''
CREATE TABLE IF NOT EXISTS nilai_siswa (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama_siswa TEXT,
    biologi INTEGER,
    fisika INTEGER,
    inggris INTEGER,
    prediksi_fakultas TEXT
)
''')
conn.commit()

def hasil_prediksi():
    try:
        nama = nama_entry.get()
        biologi = int(biologi_entry.get())
        fisika = int(fisika_entry.get())
        inggris = int(inggris_entry.get())

        # Validasi nilai
        if not (0 <= biologi <= 100 and 0 <= fisika <= 100 and 0 <= inggris <= 100):
            raise ValueError("Nilai harus antara 0 dan 100.")
        if not nama:
            raise ValueError("Nama siswa tidak boleh kosong.")
        
        # Prediksi Fakultas
        if biologi > fisika and biologi > inggris:
            fakultas = "Kedokteran"
        elif fisika > biologi and fisika > inggris:
            fakultas = "Teknik"
        elif inggris > biologi and inggris > fisika:
            fakultas = "Bahasa"
        else:
            fakultas = "Tidak Dapat Ditentukan (Nilai Sama)"

        # Simpan ke database
        cursor.execute('''
        INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)
        ''', (nama, biologi, fisika, inggris, fakultas))
        conn.commit()

        # Tampilkan hasil
        hasil_label.config(text=f"Prodi Pilihan: {fakultas}")
        messagebox.showinfo("Sukses", "Data berhasil disimpan dan diproses!")
    except ValueError as e:
        messagebox.showerror("Input Error", str(e))

# GUI
root = tk.Tk()
root.title("Aplikasi Prediksi Prodi Pilihan")
root.geometry("400x400")
root.configure(bg="#800000")

# Entry Nama dan Nilai
judul_label = tk.Label(root, text="Aplikasi Prediksi Prodi Pilihan", font=("Arial", 16, "bold"), bg="#800000", fg="white")
judul_label.pack(pady=10)

frame = tk.Frame(root, bg="#800000")
frame.pack(pady=10)

tk.Label(frame, text="Nama Siswa:", bg="#800000", fg="white").grid(row=0, column=0, sticky="w", padx=5, pady=5)
nama_entry = tk.Entry(frame)
nama_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame, text="Nilai Biologi:", bg="#800000", fg="white").grid(row=1, column=0, sticky="w", padx=5, pady=5)
biologi_entry = tk.Entry(frame)
biologi_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame, text="Nilai Fisika:", bg="#800000", fg="white").grid(row=2, column=0, sticky="w", padx=5, pady=5)
fisika_entry = tk.Entry(frame)
fisika_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Label(frame, text="Nilai Inggris:", bg="#800000", fg="white").grid(row=3, column=0, sticky="w", padx=5, pady=5)
inggris_entry = tk.Entry(frame)
inggris_entry.grid(row=3, column=1, padx=5, pady=5)

# Tombol Submit
submit_button = tk.Button(root, text="Submit", command=hasil_prediksi, bg="#FFFFFF", fg="#800000")
submit_button.pack(pady=20)

# Label Hasil
hasil_label = tk.Label(root, text="Prodi Pilihan: ", font=("Arial", 12), bg="#800000", fg="white")
hasil_label.pack(pady=10)

root.mainloop()
