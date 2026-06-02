import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

st.set_page_config(page_title="Rekomendasi Makanan", page_icon="🍔", layout="wide")

# Inisialisasi Graph di session state
if "graph" not in st.session_state:
    st.session_state.graph = nx.Graph()
    # Menambahkan data awal
    st.session_state.graph.add_edges_from([
        ("Nasi Goreng", "Sate Ayam"), ("Nasi Goreng", "Es Teh"),
        ("Burger", "Kentang Goreng"), ("Burger", "Coca Cola"),
        ("Sate Ayam", "Es Jeruk"), ("Pizza", "Coca Cola")
    ])

# Fungsi Admin
if "admin_mode" not in st.session_state:
    st.session_state.admin_mode = False

st.title("🍔 Sistem Rekomendasi Makanan")

# Sidebar
st.sidebar.header("🔧 Pengaturan")
admin_key = st.sidebar.text_input("Password Admin", type="password")
if st.sidebar.button("Login Admin"):
    if admin_key == "admin123":
        st.session_state.admin_mode = True
    else:
        st.error("Password Salah!")

# Bagian Utama
tab1, tab2 = st.tabs(["🏠 Beranda & Rekomendasi", "⚙️ Panel Admin"])

with tab1:
    st.header("Cari Rekomendasi")
    makanan_list = list(st.session_state.graph.nodes())
    pilihan = st.selectbox("Pilih makanan yang kamu suka:", makanan_list)
    
    if st.button("Cari Rekomendasi"):
        if pilihan in st.session_state.graph:
            rekomendasi = list(st.session_state.graph.neighbors(pilihan))
            st.success(f"Karena kamu suka {pilihan}, kamu mungkin juga suka:")
            st.write(rekomendasi if rekomendasi else "Belum ada rekomendasi terkait.")
        
        # Visualisasi Graf
        st.subheader("Visualisasi Hubungan Makanan")
        fig, ax = plt.subplots()
        nx.draw(st.session_state.graph, with_labels=True, node_color='skyblue', node_size=2000, ax=ax)
        st.pyplot(fig)

with tab2:
    if st.session_state.admin_mode:
        st.header("Admin Panel: Kelola Graph")
        
        menu_baru = st.text_input("Tambah Makanan Baru")
        target_rekomendasi = st.selectbox("Hubungkan dengan:", [""] + makanan_list)
        
        if st.button("Tambah ke Graph"):
            if menu_baru and target_rekomendasi:
                st.session_state.graph.add_edge(menu_baru, target_rekomendasi)
                st.success(f"Berhasil menambahkan {menu_baru}!")
                st.rerun()
                
        st.divider()
        if st.button("Logout Admin"):
            st.session_state.admin_mode = False
            st.rerun()
    else:
        st.warning("Silakan login sebagai admin di sidebar untuk mengakses fitur ini.")

st.caption("© 2026 | Project Struktur Data - Graph Food Recommender")