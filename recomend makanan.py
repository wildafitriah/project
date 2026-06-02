import streamlit as st
import pandas as pd

# 1. Konfigurasi
st.set_page_config(page_title="FoodMatch AI", layout="wide")

# 2. Inisialisasi Data (Menggunakan DataFrames sebagai pengganti Graph)
if "preferences" not in st.session_state:
    # Tabel relasi User -> Makanan
    st.session_state.preferences = pd.DataFrame(columns=["User", "Makanan"])
if "history" not in st.session_state:
    # Linked List sederhana menggunakan List Python untuk riwayat
    st.session_state.history = [] 

# 3. Sidebar (Akses)
with st.sidebar:
    st.title("🔑 Admin Dashboard")
    pw = st.text_input("Password Admin", type="password")
    admin_active = (pw == "12345")
    
    st.divider()
    st.subheader("User Login")
    current_user = st.text_input("Nama Pengguna")

# 4. Fungsi Utama
tab1, tab2, tab3 = st.tabs(["🏠 Beranda & Preferensi", "🎯 Rekomendasi", "⚙️ Admin"])

with tab1:
    st.header("Selamat Datang di FoodMatch AI")
    if current_user:
        pilihan = st.multiselect("Pilih makanan kesukaanmu:", ["Bakso", "Seblak", "Mie Ayam", "Soto", "Ayam Geprek"])
        if st.button("Simpan Preferensi"):
            for m in pilihan:
                new_data = pd.DataFrame({"User": [current_user], "Makanan": [m]})
                st.session_state.preferences = pd.concat([st.session_state.preferences, new_data], ignore_index=True)
            st.success("Preferensi tersimpan!")
    else:
        st.info("Silakan masukkan nama di sidebar.")

with tab2:
    st.header("🎯 Rekomendasi Personal")
    if current_user:
        # Logika rekomendasi: User lain yang suka makanan yang sama
        makanan_user = st.session_state.preferences[st.session_state.preferences["User"] == current_user]["Makanan"].tolist()
        rekomendasi = st.session_state.preferences[st.session_state.preferences["Makanan"].isin(makanan_user) & (st.session_state.preferences["User"] != current_user)]
        
        if not rekomendasi.empty:
            st.write("Karena kamu suka makanan tersebut, kamu mungkin juga suka:")
            st.dataframe(rekomendasi["Makanan"].unique(), use_container_width=True)
        else:
            st.write("Belum ada rekomendasi yang cocok saat ini.")

with tab3:
    if admin_active:
        st.header("⚙️ Statistik & Data")
        st.metric("Total Preferensi", len(st.session_state.preferences))
        st.subheader("Data Keseluruhan")
        st.table(st.session_state.preferences)
    else:
        st.warning("Akses admin diperlukan.")