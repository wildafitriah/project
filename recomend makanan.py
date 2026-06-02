import streamlit as st
import pandas as pd
import datetime
import time

# =============================================================================
# 1. BAGIAN STRUKTUR DATA (ABSTRACT DATA TYPES)
# =============================================================================

class Node:
    """Node untuk Linked List Riwayat."""
    def __init__(self, data):
        self.data = data
        self.next = None

class HistoryLinkedList:
    """Implementasi Linked List untuk menyimpan jejak aktivitas user."""
    def __init__(self):
        self.head = None
    
    def add(self, data):
        """Menambahkan data ke depan (O(1))."""
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node
    
    def get_all(self):
        nodes = []
        curr = self.head
        while curr:
            nodes.append(curr.data)
            curr = curr.next
        return nodes

class FoodGraph:
    """Representasi Graf (Adjacency List) untuk relasi User-Makanan."""
    def __init__(self):
        self.adj_list = {}
    
    def add_relationship(self, user, food):
        """Menambahkan edge antara user dan makanan."""
        if user not in self.adj_list:
            self.adj_list[user] = []
        if food not in self.adj_list[user]:
            self.adj_list[user].append(food)
            
    def get_all_data(self):
        """Mengambil seluruh data graf."""
        return self.adj_list

# =============================================================================
# 2. INISIALISASI SESSION STATE
# =============================================================================

def init_session():
    """Fungsi untuk inisialisasi state aplikasi."""
    if "graph" not in st.session_state: st.session_state.graph = FoodGraph()
    if "history" not in st.session_state: st.session_state.history = HistoryLinkedList()
    if "menu_df" not in st.session_state: 
        st.session_state.menu_df = pd.DataFrame({
            "Nama": ["Bakso", "Seblak", "Mie Ayam", "Soto", "Es Teh", "Es Jeruk", "Dimsum"],
            "Kategori": ["Makanan", "Makanan", "Makanan", "Makanan", "Minuman", "Minuman", "Makanan"],
            "Harga": [15000, 18000, 17000, 15000, 5000, 7000, 12000]
        })
    if "is_admin" not in st.session_state: st.session_state.is_admin = False

init_session()

# =============================================================================
# 3. ANTARMUKA PENGGUNA (FRONT-END)
# =============================================================================

st.set_page_config(page_title="FoodMatch AI Pro", layout="wide")

# Styling agar UI lebih elegan
st.markdown("""
    <style>
    .main { background-color: #f5f5f5; }
    .stButton>button { width: 100%; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🍔 FoodMatch AI: Order & Recommender System")

# Tab menu di bawah judul
menu_options = ["🏠 Beranda Menu", "🎯 Pesan & Rekomendasi", "📊 Statistik & Riwayat", "⚙️ Admin Dashboard"]
tabs = st.tabs(menu_options)

# --- LOGIN SIDEBAR ---
with st.sidebar:
    st.header("🔑 Akses Login")
    login_mode = st.radio("Mode:", ["User", "Admin"])
    if login_mode == "Admin":
        pw = st.text_input("Password Admin", type="password")
        if st.button("Login"):
            st.session_state.is_admin = (pw == "12345")
            if not st.session_state.is_admin: st.error("Password Salah!")
    else:
        current_user = st.text_input("Nama Pengguna:")

# 1. TAB BERANDA MENU
with tabs[0]:
    st.header("📋 Daftar Menu & Harga")
    st.dataframe(st.session_state.menu_df, use_container_width=True)

# 2. TAB PESAN & REKOMENDASI
with tabs[1]:
    st.header("🎯 Pesan Makanan & Dapatkan Rekomendasi")
    if not current_user:
        st.warning("Masukkan nama Anda di sidebar untuk melanjutkan.")
    else:
        pilihan = st.multiselect("Pilih Makanan/Minuman:", st.session_state.menu_df["Nama"].tolist())
        jumlah = st.number_input("Jumlah Order:", min_value=1, value=1)
        
        if st.button("Proses Pesanan & Analisis"):
            if pilihan:
                # Perhitungan Harga
                total = st.session_state.menu_df[st.session_state.menu_df["Nama"].isin(pilihan)]["Harga"].sum() * jumlah
                
                # Simpan ke Graph
                for item in pilihan:
                    st.session_state.graph.add_relationship(current_user, item)
                
                # Simpan ke Linked List
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                st.session_state.history.add(f"{timestamp} | {current_user} | Total: Rp{total:,}")
                
                st.success(f"Pesanan berhasil! Total bayar: **Rp{total:,}**")
                
                # Logika Rekomendasi (Graph traversal sederhana)
                all_data = st.session_state.graph.get_all_data()
                rekom = [f for u, fs in all_data.items() if u != current_user for f in fs if f not in pilihan]
                if rekom:
                    st.info(f"Karena kamu suka {', '.join(pilihan)}, coba juga: {list(set(rekom))}")
            else:
                st.error("Pilih menu terlebih dahulu!")

# 3. TAB STATISTIK
with tabs[2]:
    st.header("📊 Insight & Riwayat")
    col1, col2 = st.columns(2)
    
    data = st.session_state.graph.get_all_data()
    if data:
        # Analisis populer
        all_items = [f for fs in data.values() for f in fs]
        df_pop = pd.Series(all_items).value_counts().reset_index()
        df_pop.columns = ["Menu", "Jumlah Disukai"]
        col1.bar_chart(df_pop.set_index("Menu"))
        
        # Riwayat Linked List
        col2.subheader("📜 Riwayat Linked List")
        for log in st.session_state.history.get_all():
            st.text(f"▷ {log}")
    else:
        st.info("Belum ada data transaksi.")

# 4. TAB ADMIN
with tabs[3]:
    if st.session_state.is_admin:
        st.header("⚙️ Konfigurasi Data")
        with st.form("add_menu"):
            n = st.text_input("Nama Baru")
            h = st.number_input("Harga", min_value=0)
            if st.form_submit_button("Tambah"):
                new_row = pd.DataFrame({"Nama": [n], "Kategori": ["Menu"], "Harga": [h]})
                st.session_state.menu_df = pd.concat([st.session_state.menu_df, new_row], ignore_index=True)
                st.rerun()
        st.json(st.session_state.graph.get_all_data())
    else:
        st.warning("Hanya Admin yang diizinkan masuk.")

# footer
st.markdown("---")
st.write("Sistem dikembangkan untuk tugas akhir Struktur Data.")