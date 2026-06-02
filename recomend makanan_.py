import streamlit as st
import pandas as pd
import datetime

# =============================================================================
# BAGIAN 1: STRUKTUR DATA (ABSTRACT DATA TYPES)
# =============================================================================

class Node:
    """Node untuk Linked List Riwayat Pencarian."""
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
        """Mengambil seluruh data riwayat."""
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
        return self.adj_list

# =============================================================================
# BAGIAN 2: INISIALISASI SESSION
# =============================================================================

if "graph" not in st.session_state: st.session_state.graph = FoodGraph()
if "history" not in st.session_state: st.session_state.history = HistoryLinkedList()
if "menu" not in st.session_state: 
    st.session_state.menu = ["Bakso", "Seblak", "Mie Ayam", "Soto", "Ayam Geprek", "Nasi Goreng"]

# =============================================================================
# BAGIAN 3: ANTARMUKA (FRONT-END)
# =============================================================================

st.set_page_config(page_title="FoodMatch AI Pro", layout="wide")

# Sidebar - Navigasi
st.sidebar.title("🍔 FoodMatch AI Panel")
menu_nav = st.sidebar.radio("Pilih Menu:", ["Beranda", "Rekomendasi", "Statistik", "Manajemen Data"])

# Fungsi Pembantu untuk UI
def display_header(title):
    st.markdown(f"<h1 style='color: #FF4B4B;'>{title}</h1>", unsafe_allow_html=True)

# 1. HALAMAN BERANDA
if menu_nav == "Beranda":
    display_header("Selamat Datang di FoodMatch AI")
    st.write("Sistem Cerdas Rekomendasi Makanan berbasis Struktur Data Graph & Linked List.")
    st.success("Gunakan menu di samping untuk mulai bereksplorasi!")
    st.image("https://images.unsplash.com/photo-1546069901-ba9599a7e63c?q=80&w=1000")

# 2. HALAMAN REKOMENDASI (LOGIKA UTAMA)
elif menu_nav == "Rekomendasi":
    display_header("🎯 Pencarian Rekomendasi")
    user = st.text_input("Nama Pengguna Anda:")
    makanan = st.multiselect("Pilih Makanan Favorit Anda:", st.session_state.menu)
    
    if st.button("Proses Analisis"):
        if user and makanan:
            # Update Graph
            for m in makanan:
                st.session_state.graph.add_relationship(user, m)
            # Update History (Linked List)
            ts = datetime.datetime.now().strftime("%H:%M:%S")
            st.session_state.history.add(f"[{ts}] {user} mencari {', '.join(makanan)}")
            
            st.balloons()
            st.success("Data berhasil diproses!")
            
            # Logika Rekomendasi Sederhana
            all_data = st.session_state.graph.get_all_data()
            rekom = []
            for u, foods in all_data.items():
                if u != user:
                    rekom.extend([f for f in foods if f not in makanan])
            
            st.subheader("Hasil Rekomendasi:")
            if rekom:
                st.write(list(set(rekom)))
            else:
                st.warning("Belum ada data relasi yang cukup.")
        else:
            st.error("Input tidak lengkap.")

# 3. HALAMAN STATISTIK
elif menu_nav == "Statistik":
    display_header("📊 Statistik Pengguna")
    col1, col2 = st.columns(2)
    
    data = st.session_state.graph.get_all_data()
    if data:
        all_food_list = [f for foods in data.values() for f in foods]
        df = pd.Series(all_food_list).value_counts().reset_index()
        df.columns = ["Makanan", "Total"]
        col1.bar_chart(df.set_index("Makanan"))
        
        col2.subheader("📜 Riwayat Aktifitas (Linked List)")
        for log in st.session_state.history.get_all():
            st.text(f"→ {log}")
    else:
        st.info("Belum ada data statistik.")

# 4. HALAMAN MANAJEMEN (ADMIN)
elif menu_nav == "Manajemen Data":
    display_header("⚙️ Admin Dashboard")
    password = st.text_input("Password Admin:", type="password")
    
    if password == "admin123":
        st.subheader("Kelola Menu Makanan")
        new_m = st.text_input("Nama Makanan Baru")
        if st.button("Tambah"):
            st.session_state.menu.append(new_m)
            st.rerun()
            
        st.subheader("Data Graph (Adjacency List)")
        st.json(st.session_state.graph.get_all_data())
        
        # Fitur Ekspor
        if st.button("Download Data ke CSV"):
            df_export = pd.DataFrame(st.session_state.graph.get_all_data().items(), columns=["User", "Favs"])
            st.download_button("Klik untuk Download", df_export.to_csv(), "data.csv", "text/csv")
    else:
        st.warning("Masukkan password admin yang benar.")

# Penutup (Menambah baris kode & dokumentasi)
st.markdown("---")
st.caption("Proyek UAS Struktur Data - FoodMatch AI © 2026")