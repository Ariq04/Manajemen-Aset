# app.py

import streamlit as st
import pandas as pd
import os

# --- Konfigurasi dan Fungsi Bantuan ---
DATA_FILE = os.path.join("data", "aset.csv")

def load_data():
    """Memuat data dari file CSV atau membuat DataFrame kosong dengan kolom yang benar."""
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    # Definisikan semua kemungkinan kolom untuk DataFrame kosong agar konsisten
    columns = [
        'id_aset', 'nama', 'status', 'lokasi', 'harga_awal', 'tgl_pembelian',
        'tipe', 'ukuran_layar', 'kapasitas_ram', 'jenis_tinta', 'kecepatan_cetak_ppm'
    ]
    return pd.DataFrame(columns=columns)

# --- Konfigurasi Halaman Utama ---
st.set_page_config(
    page_title="Manajemen Aset IT",
    page_icon="🏢",
    layout="wide"
)

# Muat data ke dalam session_state HANYA jika belum ada.
# Ini adalah langkah kunci agar data bisa diakses oleh semua halaman lain.
if 'df_aset' not in st.session_state:
    st.session_state.df_aset = load_data()

# --- Konten Halaman Utama ---
st.title("Selamat Datang di Aplikasi Manajemen Aset IT")
st.markdown("---")
st.write(
    """
    Aplikasi ini dirancang untuk membantu Anda mengelola aset Teknologi Informasi di perusahaan Anda secara efisien.
    """
)
st.info("👈 Silakan gunakan menu navigasi di sebelah kiri untuk mengakses fitur yang tersedia, seperti Dashboard, melihat daftar aset, atau menambah aset baru.")

# Menambahkan gambar ilustrasi untuk mempercantik tampilan
# st.image("https://images.unsplash.com/photo-1522204523234-8729aa6e3d5f?q=80&w=2940&auto=format&fit=crop", caption="Manajemen Aset yang Terorganisir")

