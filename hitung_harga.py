import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
import time
import threading

# Database produk dan admin
produk = {
    '001': {'nama': 'Barang A', 'harga': 10000},
    '002': {'nama': 'Barang B', 'harga': 20000},
    '003': {'nama': 'Barang C', 'harga': 30000}
}
admin_password = 'securepassword123'
history = []  # Daftar untuk menyimpan history perhitungan

# Animasi tulisan
def animasi_tulisan(label):
    teks = "Selamat datang di Aplikasi Hitung Harga"
    for i in range(len(teks)+1):
        label.config(text=teks[:i])
        time.sleep(0.1)

def animasi_threading(label):
    t = threading.Thread(target=animasi_tulisan, args=(label,))
    t.start()

# Login admin
def login_admin():
    def check_password():
        if password_entry.get() == admin_password:
            login_window.destroy()
            tambah_produk()
        else:
            messagebox.showerror("Login Gagal", "Password salah!")
    
    login_window = ttk.Toplevel()
    login_window.title("Login Admin")
    ttk.Label(login_window, text="Masukkan Password Admin").pack(pady=10)
    password_entry = ttk.Entry(login_window, show="*")
    password_entry.pack(pady=5)
    ttk.Button(login_window, text="Login", command=check_password, bootstyle="primary-outline").pack(pady=10)

# Tambah produk
def tambah_produk():
    def simpan_produk():
        produk_id = entry_id.get()
        nama_produk = entry_nama.get()
        harga_produk = int(entry_harga.get())
        produk[produk_id] = {'nama': nama_produk, 'harga': harga_produk}
        messagebox.showinfo("Sukses", "Produk berhasil ditambahkan")
        tambah_window.destroy()
        
    tambah_window = ttk.Toplevel()
    tambah_window.title("Tambah Produk Baru")
    
    ttk.Label(tambah_window, text="ID Produk").pack(pady=5)
    entry_id = ttk.Entry(tambah_window)
    entry_id.pack(pady=5)
    
    ttk.Label(tambah_window, text="Nama Produk").pack(pady=5)
    entry_nama = ttk.Entry(tambah_window)
    entry_nama.pack(pady=5)
    
    ttk.Label(tambah_window, text="Harga Produk").pack(pady=5)
    entry_harga = ttk.Entry(tambah_window)
    entry_harga.pack(pady=5)
    
    ttk.Button(tambah_window, text="Simpan", command=simpan_produk, bootstyle="success-outline").pack(pady=10)

# Lihat produk
def lihat_produk():
    produk_list = "\n".join([f"{k}: {v['nama']} - Rp{v['harga']}" for k, v in produk.items()])
    messagebox.showinfo("Daftar Produk", produk_list)

# Hitung harga setelah diskon
def hitung_harga():
    produk_id = entry_id_barang.get()
    if produk_id not in produk:
        messagebox.showerror("Error", "ID Barang tidak valid!")
        return
    
    harga_satuan = produk[produk_id]['harga']
    jumlah_barang = int(entry_jumlah.get())
    
    konfirmasi = messagebox.askyesno("Konfirmasi", f"Anda memilih {produk[produk_id]['nama']} dengan harga Rp{harga_satuan}. Lanjutkan?")
    if not konfirmasi:
        return
    
    total_sebelum_diskon = harga_satuan * jumlah_barang
    if jumlah_barang >= 10:
        diskon = 0.10
    elif jumlah_barang >= 5:
        diskon = 0.05
    else:
        diskon = 0.0
    
    total_setelah_diskon = total_sebelum_diskon * (1 - diskon)
    hasil = {
        "produk": produk[produk_id]['nama'],
        "harga_satuan": harga_satuan,
        "jumlah_barang": jumlah_barang,
        "total_sebelum_diskon": total_sebelum_diskon,
        "diskon": diskon * 100,
        "total_setelah_diskon": total_setelah_diskon
    }
    history.append(hasil)  # Tambahkan hasil ke history
    messagebox.showinfo("Total Harga", f"Total sebelum diskon: Rp{total_sebelum_diskon}\nDiskon: {diskon * 100}%\nTotal setelah diskon: Rp{total_setelah_diskon}")

# Batal perhitungan
def batal():
    entry_id_barang.delete(0, tk.END)
    entry_jumlah.delete(0, tk.END)

# Tampilkan history perhitungan
def tampilkan_history():
    history_window = ttk.Toplevel()
    history_window.title("History Hasil Perhitungan")
    
    if not history:
        ttk.Label(history_window, text="Belum ada history perhitungan.", font=("Arial", 12)).pack(pady=20)
    else:
        for h in history:
            hasil_text = (f"Produk: {h['produk']}\n"
                          f"Harga Satuan: Rp{h['harga_satuan']}\n"
                          f"Jumlah Barang: {h['jumlah_barang']}\n"
                          f"Total Sebelum Diskon: Rp{h['total_sebelum_diskon']}\n"
                          f"Diskon: {h['diskon']}%\n"
                          f"Total Setelah Diskon: Rp{h['total_setelah_diskon']}\n")
            ttk.Label(history_window, text=hasil_text, font=("Arial", 10), bootstyle="info").pack(pady=5)

# GUI utama dengan ttkbootstrap
app = ttk.Window(themename="darkly", title="Aplikasi Hitung Harga", size=(500, 500))
app.wm_attributes("-alpha", 0.93)  # Set transparansi 


# Animasi selamat datang
label_animasi = ttk.Label(app, font=("Arial", 16, "bold"), bootstyle="info")
label_animasi.pack(pady=15)
animasi_threading(label_animasi)

# Label dan input ID Barang
ttk.Label(app, text="Masukkan ID Barang", font=("Arial", 12)).pack(pady=5)
entry_id_barang = ttk.Entry(app, font=("Arial", 11), width=20)
entry_id_barang.pack(pady=5)

# Label dan input jumlah barang
ttk.Label(app, text="Masukkan Jumlah Barang", font=("Arial", 12)).pack(pady=5)
entry_jumlah = ttk.Entry(app, font=("Arial", 11), width=20)
entry_jumlah.pack(pady=5)

# Frame untuk menata tombol-tombol secara rapi
button_frame = ttk.Frame(app)
button_frame.pack(pady=15)

# Tombol utama dengan gaya lebih modern dan rapi
ttk.Button(button_frame, text="Hitung Harga", command=hitung_harga, bootstyle="success-outline", width=15).grid(row=0, column=0, padx=10, pady=5)
ttk.Button(button_frame, text="Batal", command=batal, bootstyle="danger-outline", width=15).grid(row=0, column=1, padx=10, pady=5)
ttk.Button(button_frame, text="Lihat Produk", command=lihat_produk, bootstyle="info-outline", width=15).grid(row=1, column=0, padx=10, pady=5)
ttk.Button(button_frame, text="Tambah Produk", command=login_admin, bootstyle="warning-outline", width=15).grid(row=1, column=1, padx=10, pady=5)
ttk.Button(button_frame, text="Lihat History", command=tampilkan_history, bootstyle="secondary-outline", width=15).grid(row=2, column=0, columnspan=2, pady=5)

# Hak cipta
ttk.Label(app, text="Hak Cipta © 2024 by Kaizenn-Me", font=("Arial", 10, "italic")).pack(side="bottom", pady=20)

app.mainloop()
