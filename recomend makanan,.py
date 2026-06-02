import streamlit as st
import pandas as pd
import datetime

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
        if user not in self.adj_list:
            self.adj_list[user] = []
        if food not in self.adj_list[user]:
            self.adj_list[user].append(food)
            
    def get_all_data(self):
        return self.adj_list

# =============================================================================
# 2. INISIALISASI SESSION STATE
# =============================================================================
if "graph" not in st.session_state: st.session_state.graph = FoodGraph()
if "history" not in st.session_state: st.session_state.history = HistoryLinkedList()
if "menu" not in st.session_state: 
    st.session_state.menu = ["Bakso", "Seblak", "Mie Ayam", "Soto", "Ayam Geprek", "Nasi Goreng"]
if "is_admin" not in st.session_state: st.session_state.is_admin = False

# =============================================================================
# 3. ANTARMUKA (FRONT-END)
# =============================================================================
st.set_page_config(page_title="FoodMatch AI", layout="wide")

# Judul Utama
st.title("🍔 FoodMatch AI: Intelligent Recommender")

# Menu Horizontal tepat di bawah judul
menu_options = ["🏠 Beranda", "🎯 Cari Rekomendasi", "📊 Statistik & Riwayat", "⚙️ Admin Panel"]
selected_menu = st.tabs(menu_options)

# --- LOGIN PANEL (Sidebar) ---
with st.sidebar:
    st.header("🔑 Akses Login")
    login_type = st.radio("Tipe Akses:", ["User", "Admin"])
    
    if login_type == "Admin":
        pw = st.text_input("Password Admin", type="password")
        if st.button("Login Admin"):
            if pw == "12345":
                st.session_state.is_admin = True
                st.success("Admin Login Berhasil!")
            else:
                st.error("Password Salah!")
    else:
        current_user = st.text_input("Nama Pengguna (User):")

# --- LOGIKA TAB ---

# 1. Beranda
with selected_menu[0]:
    st.write("Selamat Datang! Sistem ini menggunakan **Graph** untuk memetakan preferensi makanan dan **Linked List** untuk riwayat pencarian.")
    st.image("https://images.unsplash.com/photo-1546069901-ba9599a7e63c?q=80&w=1000", width=600)

# 2. Rekomendasi
with selected_menu[1]:
    if not current_user:
        st.warning("Silakan masukkan nama user di sidebar untuk mulai.")
    else:
        pilihan = st.multiselect("Pilih Makanan Favorit:", st.session_state.menu)
        if st.button("Proses Analisis"):
            if pilihan:
                # Simpan ke Graph & History
                for m in pilihan:
                    st.session_state.graph.add_relationship(current_user, m)
                ts = datetime.datetime.now().strftime("%H:%M:%S")
                st.session_state.history.add(f"[{ts}] {current_user} memilih: {', '.join(pilihan)}")
                st.success("Preferensi tersimpan!")
                
                # Logika Rekomendasi
                rekom = []
                for u, foods in st.session_state.graph.get_all_data().items():
                    if u != current_user:
                        rekom.extend([f for f in foods if f not in pilihan])
                st.info(f"Rekomendasi untuk {current_user}: {list(set(rekom))}")

# 3. Statistik
with selected_menu[2]:
    st.header("📊 Statistik Sistem")
    col1, col2 = st.columns(2)
    
    data = st.session_state.graph.get_all_data()
    if data:
        all_food = [f for foods in data.values() for f in foods]
        df = pd.Series(all_food).value_counts().reset_index()
        df.columns = ["Makanan", "Jumlah"]
        col1.bar_chart(df.set_index("Makanan"))
        
        col2.subheader("📜 Riwayat Linked List")
        for log in st.session_state.history.get_all():
            st.text(f"• {log}")

# 4. Admin Dashboard
with selected_menu[3]:
    if st.session_state.is_admin:
        st.header("⚙️ Konfigurasi Admin")
        new_m = st.text_input("Tambah Menu Makanan:")
        if st.button("Tambah ke Daftar"):
            st.session_state.menu.append(new_m)
            st.rerun()
        st.subheader("Data Graph")
        st.json(st.session_state.graph.get_all_data())
    else:
        st.warning("Akses Admin diperlukan (Silakan login via sidebar).")