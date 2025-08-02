# pages/2_📋_Lihat_Aset.py

import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from datetime import datetime

# Fungsi save_data dipindahkan ke sini karena hanya digunakan di halaman ini dan tambah aset
def save_data(df):
    df.to_csv("data/aset.csv", index=False)

st.set_page_config(page_title="Daftar Aset", page_icon="📋", layout="wide")
st.title("📋 Daftar & Kelola Aset")

# --- SUB-NAVBAR UNTUK KELOLA & DOWNLOAD ---
sub_selected = option_menu(
    menu_title=None,
    options=["Kelola Data", "Download Data"],
    icons=["pencil-square", "cloud-download-fill"],
    orientation="horizontal"
)

df = st.session_state.get('df_aset', pd.DataFrame())

if sub_selected == "Kelola Data":
    
    # --- FILTER TAMPILAN BERDASARKAN TIPE ---
    st.markdown("##### Filter Tampilan Aset")
    filter_tipe = st.radio(
        "Tampilkan aset berdasarkan tipe:",
        ["Semua", "Laptop", "Server", "Printer"],
        horizontal=True,
        label_visibility="collapsed"
    )

    # Definisikan kolom yang relevan untuk setiap tipe
    kolom_umum = ['id_aset', 'nama', 'status', 'lokasi', 'harga_awal', 'tgl_pembelian', 'tipe']
    kolom_laptop = kolom_umum + ['ukuran_layar']
    kolom_server = kolom_umum + ['kapasitas_ram']
    kolom_printer = kolom_umum + ['jenis_tinta', 'kecepatan_cetak_ppm']

    # Siapkan DataFrame untuk ditampilkan berdasarkan filter
    df_display = pd.DataFrame()

    if filter_tipe == "Laptop":
        df_display = df[df['tipe'] == 'Laptop'][kolom_laptop]
    elif filter_tipe == "Server":
        df_display = df[df['tipe'] == 'Server'][kolom_server]
    elif filter_tipe == "Printer":
        df_display = df[df['tipe'] == 'Printer'][kolom_printer]
    else: # "Semua"
        df_display = df

    st.dataframe(df_display.fillna(''))
    st.markdown("---")
    st.subheader("Pilih Aset untuk Dikelola (Update/Delete)")

    # Ambil daftar ID dari DataFrame yang sedang ditampilkan
    id_list = df_display['id_aset'].tolist() if 'id_aset' in df_display.columns else []

    if not id_list:
        st.info("Tidak ada data untuk dikelola pada tampilan ini. Silakan tambahkan aset baru atau ubah filter.")
    else:
        selected_id = st.selectbox("Pilih ID Aset", id_list, key="manage_select")
        if selected_id:
            # Operasi update/delete tetap dilakukan pada DataFrame utama (df)
            aset_terpilih_df = df[df['id_aset'] == selected_id]
            if not aset_terpilih_df.empty:
                index_to_manage = aset_terpilih_df.index[0]
                aset_terpilih = aset_terpilih_df.iloc[0].to_dict()

                col1, col2 = st.columns(2)
                with col1:
                    with st.expander("📝 Ubah Data Aset Ini", expanded=True):
                        with st.form("form_update"):
                            st.write(f"Mengubah data untuk: **{aset_terpilih['nama']}**")
                            
                            # --- FORM UPDATE LENGKAP ---
                            new_nama = st.text_input("Nama Aset", value=aset_terpilih['nama'])
                            current_status_index = ["Aktif", "Perbaikan", "Non-Aktif"].index(aset_terpilih['status']) if aset_terpilih['status'] in ["Aktif", "Perbaikan", "Non-Aktif"] else 0
                            new_status = st.selectbox("Status", ["Aktif", "Perbaikan", "Non-Aktif"], index=current_status_index)
                            new_lokasi = st.text_input("Lokasi", value=aset_terpilih['lokasi'])
                            new_harga = st.number_input("Harga Awal", min_value=0.0, value=float(aset_terpilih['harga_awal']), format="%.2f")
                            new_tgl_pembelian = st.date_input("Tanggal Pembelian", value=pd.to_datetime(aset_terpilih['tgl_pembelian']))

                            # Input spesifik berdasarkan tipe
                            if aset_terpilih['tipe'] == 'Laptop':
                                new_ukuran_layar = st.text_input("Ukuran Layar (inch)", value=aset_terpilih.get('ukuran_layar', ''))
                            elif aset_terpilih['tipe'] == 'Server':
                                new_kapasitas_ram = st.text_input("Kapasitas RAM (GB)", value=aset_terpilih.get('kapasitas_ram', ''))
                            elif aset_terpilih['tipe'] == 'Printer':
                                current_tinta_index = ["Laser", "Inkjet", "Dot Matrix"].index(aset_terpilih['jenis_tinta']) if aset_terpilih.get('jenis_tinta') in ["Laser", "Inkjet", "Dot Matrix"] else 0
                                new_jenis_tinta = st.selectbox("Jenis Tinta", ["Laser", "Inkjet", "Dot Matrix"], index=current_tinta_index)
                                new_kecepatan_cetak_ppm = st.number_input("Kecepatan Cetak (PPM)", min_value=0, value=int(aset_terpilih.get('kecepatan_cetak_ppm', 0) or 0))

                            if st.form_submit_button("Simpan Perubahan"):
                                # Simpan semua perubahan ke DataFrame utama
                                df.loc[index_to_manage, 'nama'] = new_nama
                                df.loc[index_to_manage, 'status'] = new_status
                                df.loc[index_to_manage, 'lokasi'] = new_lokasi
                                df.loc[index_to_manage, 'harga_awal'] = new_harga
                                df.loc[index_to_manage, 'tgl_pembelian'] = new_tgl_pembelian.strftime('%Y-%m-%d')

                                if aset_terpilih['tipe'] == 'Laptop':
                                    df.loc[index_to_manage, 'ukuran_layar'] = new_ukuran_layar
                                elif aset_terpilih['tipe'] == 'Server':
                                    df.loc[index_to_manage, 'kapasitas_ram'] = new_kapasitas_ram
                                elif aset_terpilih['tipe'] == 'Printer':
                                    df.loc[index_to_manage, 'jenis_tinta'] = new_jenis_tinta
                                    df.loc[index_to_manage, 'kecepatan_cetak_ppm'] = new_kecepatan_cetak_ppm

                                save_data(df)
                                st.session_state.df_aset = df.copy()
                                st.success("Data aset berhasil diperbarui!")
                                st.rerun()
                with col2:
                    with st.expander("🗑️ Hapus Data Aset Ini"):
                        st.warning(f"Anda yakin ingin menghapus **{aset_terpilih['nama']}**?")
                        if st.button("Ya, Hapus Data Ini"):
                            df.drop(index_to_manage, inplace=True)
                            save_data(df)
                            st.session_state.df_aset = df.copy()
                            st.success("Data aset berhasil dihapus.")
                            st.rerun()

elif sub_selected == "Download Data":
    st.subheader("Unduh Laporan Aset")
    st.write("Pilih tipe aset yang ingin diunduh, lalu klik tombol di bawah ini.")
    
    # --- FILTER DOWNLOAD BERDASARKAN TIPE ---
    download_filter_tipe = st.radio(
        "Filter data yang akan diunduh:",
        ["Semua", "Laptop", "Server", "Printer"],
        horizontal=True,
        key="download_filter" # Gunakan key yang berbeda untuk widget ini
    )

    # Definisikan kolom yang relevan untuk setiap tipe
    kolom_umum = ['id_aset', 'nama', 'status', 'lokasi', 'harga_awal', 'tgl_pembelian', 'tipe']
    kolom_laptop = kolom_umum + ['ukuran_layar']
    kolom_server = kolom_umum + ['kapasitas_ram']
    kolom_printer = kolom_umum + ['jenis_tinta', 'kecepatan_cetak_ppm']

    # Siapkan DataFrame untuk di-download berdasarkan filter
    df_to_download = pd.DataFrame()
    filename = "laporan_aset.csv"

    if download_filter_tipe == "Laptop":
        df_to_download = df[df['tipe'] == 'Laptop'][kolom_laptop]
        filename = "laporan_aset_laptop.csv"
    elif download_filter_tipe == "Server":
        df_to_download = df[df['tipe'] == 'Server'][kolom_server]
        filename = "laporan_aset_server.csv"
    elif download_filter_tipe == "Printer":
        df_to_download = df[df['tipe'] == 'Printer'][kolom_printer]
        filename = "laporan_aset_printer.csv"
    else: # "Semua"
        df_to_download = df
        filename = "laporan_semua_aset.csv"

    st.info(f"Anda akan mengunduh **{len(df_to_download)}** baris data.")

    @st.cache_data
    def convert_df_to_csv(df_to_convert):
        # Hanya konversi jika DataFrame tidak kosong
        if not df_to_convert.empty:
            return df_to_convert.to_csv(index=False).encode('utf-8')
        return "".encode('utf-8')

    csv = convert_df_to_csv(df_to_download)
    
    st.download_button(
        label="Download Data as CSV",
        data=csv,
        file_name=filename,
        mime='text/csv',
        # Tombol dinonaktifkan jika tidak ada data untuk diunduh
        disabled=df_to_download.empty 
    )
