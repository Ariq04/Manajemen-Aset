# pages/3_Tambah_Aset.py

import streamlit as st
import pandas as pd
from datetime import datetime
from core.models import Laptop, Server, Printer

def save_data(df):
    df.to_csv("data/aset.csv", index=False)

st.set_page_config(page_title="Tambah Aset", page_icon="➕", layout="wide")
st.title("➕ Form Tambah Aset Baru")

df = st.session_state.get('df_aset', pd.DataFrame())

tipe_aset = st.selectbox("Pilih Tipe Aset", ["Laptop", "Server", "Printer"], key="tipe_aset_choice")

with st.form("form_tambah_aset", clear_on_submit=True):
    id_aset = st.text_input("ID Aset (unik)", f"ASET-{len(df) + 1}")
    nama = st.text_input("Nama Aset")
    status = st.selectbox("Status", ["Aktif", "Perbaikan", "Non-Aktif"])
    lokasi = st.text_input("Lokasi")
    harga_awal = st.number_input("Harga Awal", min_value=0.0, format="%.2f")
    tgl_pembelian = st.date_input("Tanggal Pembelian")

    st.write(f"**Atribut Khusus untuk: {tipe_aset}**")
    if tipe_aset == "Laptop":
        ukuran_layar = st.text_input("Ukuran Layar (inch)")
    elif tipe_aset == "Server":
        kapasitas_ram = st.text_input("Kapasitas RAM (GB)")
    elif tipe_aset == "Printer":
        jenis_tinta = st.selectbox("Jenis Tinta", ["Laser", "Inkjet", "Dot Matrix"])
        kecepatan_cetak_ppm = st.number_input("Kecepatan Cetak (PPM)", min_value=0)

    submitted = st.form_submit_button("Simpan Aset")

    if submitted:
        aset_baru = None
        if tipe_aset == "Laptop":
            aset_baru = Laptop(id_aset, nama, status, lokasi, harga_awal, tgl_pembelian, ukuran_layar)
        elif tipe_aset == "Server":
            aset_baru = Server(id_aset, nama, status, lokasi, harga_awal, tgl_pembelian, kapasitas_ram)
        elif tipe_aset == "Printer":
            aset_baru = Printer(id_aset, nama, status, lokasi, harga_awal, tgl_pembelian, jenis_tinta, kecepatan_cetak_ppm)

        if aset_baru:
            new_data_df = pd.DataFrame([aset_baru.to_dict()])
            updated_df = pd.concat([df, new_data_df], ignore_index=True)
            save_data(updated_df)
            st.session_state.df_aset = updated_df.copy() # Update session state
            st.success(f"Aset '{nama}' berhasil ditambahkan!")
            # Tidak perlu rerun karena form sudah clear_on_submit
