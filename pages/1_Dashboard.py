# pages/1_Dashboard.py

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

st.title("📊 Dashboard Aset Perusahaan")
st.markdown("---")

# Akses data dari session state
df = st.session_state.get('df_aset', pd.DataFrame())

if df.empty:
    st.warning("Data aset masih kosong. Silakan tambahkan aset dari halaman 'Tambah Aset Baru'.")
else:
    # --- KPI Cards ---
    total_aset = len(df)
    nilai_total_aset = pd.to_numeric(df['harga_awal']).sum()
    aset_aktif = len(df[df['status'] == 'Aktif'])
    aset_perbaikan = len(df[df['status'] == 'Perbaikan'])

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Aset", f"{total_aset} Unit")
    with col2:
        st.metric("Nilai Total Aset", f"Rp {nilai_total_aset:,.0f}")
    with col3:
        st.metric("Aset Aktif", f"{aset_aktif} Unit")
    with col4:
        st.metric("Dalam Perbaikan", f"{aset_perbaikan} Unit")

    st.markdown("---")

    # --- Grafik ---
    col_chart1, col_chart2 = st.columns(2)
    with col_chart1:
        st.subheader("Komposisi Tipe Aset")
        tipe_counts = df['tipe'].value_counts()
        fig_tipe = px.pie(values=tipe_counts.values, names=tipe_counts.index, hole=.3,
                          color_discrete_sequence=px.colors.sequential.Agsunset)
        st.plotly_chart(fig_tipe, use_container_width=True)

    with col_chart2:
        st.subheader("Distribusi Status Aset")
        status_counts = df['status'].value_counts()
        fig_status = px.bar(x=status_counts.index, y=status_counts.values, labels={'x': 'Status', 'y': 'Jumlah'},
                            color=status_counts.index, color_discrete_map={
            'Aktif': 'green', 'Perbaikan': 'orange', 'Non-Aktif': 'red'
        })
        st.plotly_chart(fig_status, use_container_width=True)
