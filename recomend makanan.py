import streamlit as st
import pandas as pd
import datetime

# --- CLASS STRUKTUR DATA (UAS) ---
class FoodNode:
    """Node untuk Linked List Riwayat Transaksi"""
    def __init__(self, kode, nama, menu, total, waktu):
        self.kode = kode
        self.nama = nama
        self.menu = menu
        self.total = total
        self.waktu = waktu
        self.next = None

class TicketLinkedList:
    def __init__(self):
        self.head = None

    def tambah_data(self, kode, nama, menu, total):
        waktu = datetime.datetime.now().strftime("%H:%M:%S")
        node = FoodNode(kode, nama, menu, total, waktu)
        if not self.head:
            self.head = node
        else:
            cur = self.head
            while cur.next:
                cur = cur.next
            cur.next = node

    def tampilkan_data(self):
        data = []
        cur = self.head
        while cur:
            data.append({"Kode": cur.kode, "Nama": cur.nama, "Menu": ", ".join(cur.menu), "Total": cur.total, "Waktu": cur.waktu})
            cur = cur.next
        return data

class FoodGraph:
    """Graph untuk Sistem Rekomendasi (Co-occurrence)"""
    def __init__(self):
        self.adj_list = {}
    
    def add_relationship(self, menu_list):
        for i in range(len(menu_list)):
            for j in range(len(menu_list)):
                if i != j:
                    u, v = menu_list[i], menu_list[j]
                    if u not in self.adj_list: self.adj_list[u] = set()
                    self.adj_list[u].add(v)
    
    def get_recommendation(self, selected_items):
        rekom = set()
        for item in selected_items:
            if item in self.adj_list:
                rekom.update(self.adj_list[item])
        return list(rekom - set(selected_items))

# --- INISIALISASI ---
if "orders" not in st.session_state: st.session_state.orders = TicketLinkedList()
if "graph" not in st.session_state: st.session_state.graph = FoodGraph()
menu_data = {"Bakso": 15000, "Seblak": 18000, "Mie Ayam": 17000, "Soto": 15000, "Es Teh": 5000, "Dimsum": 12000}

# --- UI APP ---
st.set_page_config(page_title="FoodMatch AI", layout="wide")
st.title("🍔 FoodMatch AI: Order & Recommender")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📝 Pesan Makanan")
    nama = st.text_input("Nama Pelanggan")
    pilihan = st.multiselect("Pilih Menu:", list(menu_data.keys()))
    
    if st.button("Pesan Sekarang"):
        if nama and pilihan:
            total = sum([menu_data[m] for m in pilihan])
            kode = f"TRX-{len(st.session_state.orders.tampilkan_data())+1}"
            
            st.session_state.orders.tambah_data(kode, nama, pilihan, total)
            st.session_state.graph.add_relationship(pilihan)
            
            st.session_state.last_order = {"nama": nama, "pilihan": pilihan, "total": total}
            st.rerun()

with col2:
    st.subheader("💡 Rekomendasi & Struk")
    if "last_order" in st.session_state:
        o = st.session_state.last_order
        st.success(f"Pesanan {o['nama']} berhasil!")
        st.metric("Total Bayar", f"Rp {o['total']:,}")
        
        saran = st.session_state.graph.get_recommendation(o['pilihan'])
        if saran:
            st.info(f"Karena kamu pesan {', '.join(o['pilihan'])}, coba juga: **{', '.join(saran)}**")
        else:
            st.write("Sistem sedang mempelajari pola seleramu...")

# --- ADMIN DASHBOARD ---
with st.expander("⚙️ Admin Dashboard"):
    st.header("📊 Data Pesanan (Linked List)")
    data = st.session_state.orders.tampilkan_data()
    if data:
        st.dataframe(pd.DataFrame(data))
        st.subheader("Visualisasi Graph (Adjacency List)")
        st.json(st.session_state.graph.adj_list)