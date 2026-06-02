import streamlit as st
import pandas as pd

# Konfigurasi Halaman
st.set_page_config(page_title="Rekomendasi Makanan", page_icon="🍔", layout="wide")

# CSS untuk mempercantik tampilan
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# Inisialisasi Data Menggunakan Session State agar data menetap saat halaman refresh
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame({
        "Makanan": ["Nasi Goreng", "Sate Ayam", "Burger", "Pizza", "Mie Ayam"],
        "Rekomendasi": ["Es Teh", "Es Jeruk", "Kentang Goreng", "Coca Cola", "Pangsit"]
    })

if "admin_login" not in st.session_state:
    st.session_state.admin_login = False

# Sidebar
with st.sidebar:
    st.header("🔑 Admin Panel")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if username == "admin" and password == "12345":
            st.session_state.admin_login = True
            st.rerun()
        else:
            st.error("Login Gagal")
    
    if st.session_state.admin_login:
        if st.button("Logout"):
            st.session_state.admin_login = False
            st.rerun()

# Judul
st.title("🍔 Sistem Rekomendasi Makanan")
st.write("Temukan pasangan makanan favoritmu dengan mudah!")

# Tab Antarmuka
tab1, tab2 = st.tabs(["🏠 Beranda", "⚙️ Manajemen Data"])

with tab1:
    st.subheader("Cari Rekomendasi")
    pilihan = st.selectbox("Pilih makanan kesukaanmu:", st.session_state.df["Makanan"].tolist())
    
    if st.button("Lihat Rekomendasi"):
        hasil = st.session_state.df[st.session_state.df["Makanan"] == pilihan]["Rekomendasi"].values[0]
        st.success(f"Karena kamu suka **{pilihan}**, kami merekomendasikan: **{hasil}**")

with tab2:
    if st.session_state.admin_login:
        st.subheader("Kelola Data Rekomendasi")
        st.dataframe(st.session_state.df, use_container_width=True)
        
        with st.form("tambah_data"):
            makanan_baru = st.text_input("Nama Makanan")
            rekom_baru = st.text_input("Rekomendasi")
            submit = st.form_submit_button("Tambah Data")
            if submit and makanan_baru and rekom_baru:
                new_row = pd.DataFrame({"Makanan": [makanan_baru], "Rekomendasi": [rekom_baru]})
                st.session_state.df = pd.concat([st.session_state.df, new_row], ignore_index=True)
                st.success("Data berhasil ditambahkan!")
                st.rerun()
    else:
        st.warning("🔒 Akses terbatas. Silakan login di sidebar untuk mengelola data.")

st.caption("© 2026 | Sistem Rekomendasi Makanan - Struktur Data")