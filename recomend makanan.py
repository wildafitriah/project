import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Food Recommendation",
    page_icon="🍔",
    layout="wide"
)

# =====================================
# GRAPH
# =====================================

class FoodGraph:

    def __init__(self):
        self.graph = {}

    def tambah_node(self, node):
        if node not in self.graph:
            self.graph[node] = set()

    def tambah_suka(self, user, makanan):

        self.tambah_node(user)
        self.tambah_node(makanan)

        self.graph[user].add(makanan)
        self.graph[makanan].add(user)

    def rekomendasi(self, target_user):

        if target_user not in self.graph:
            return []

        makanan_disukai = self.graph[target_user]

        skor = {}

        for makanan in makanan_disukai:

            for user_lain in self.graph[makanan]:

                if user_lain != target_user:

                    for makanan_baru in self.graph[user_lain]:

                        if makanan_baru not in makanan_disukai:

                            skor[makanan_baru] = (
                                skor.get(makanan_baru, 0) + 1
                            )

        hasil = sorted(
            skor.items(),
            key=lambda x: x[1],
            reverse=True
        )

        return hasil


# =====================================
# SESSION
# =====================================

if "food" not in st.session_state:

    st.session_state.food = FoodGraph()

    # dummy data

    st.session_state.food.tambah_suka(
        "Andi",
        "Bakso"
    )

    st.session_state.food.tambah_suka(
        "Andi",
        "Mie Ayam"
    )

    st.session_state.food.tambah_suka(
        "Budi",
        "Bakso"
    )

    st.session_state.food.tambah_suka(
        "Budi",
        "Seblak"
    )

    st.session_state.food.tambah_suka(
        "Citra",
        "Mie Ayam"
    )

    st.session_state.food.tambah_suka(
        "Citra",
        "Nasi Goreng"
    )

if "admin" not in st.session_state:
    st.session_state.admin = False

# =====================================
# LOGIN ADMIN
# =====================================

st.sidebar.header("🔐 Login Admin")

user_admin = st.sidebar.text_input(
    "Username"
)

pass_admin = st.sidebar.text_input(
    "Password",
    type="password"
)

if st.sidebar.button("Login"):

    if user_admin == "admin" and pass_admin == "12345":

        st.session_state.admin = True

        st.sidebar.success(
            "Login berhasil"
        )

    else:

        st.sidebar.error(
            "Login gagal"
        )

# =====================================
# USER INPUT
# =====================================

st.title(
    "🍔 Sistem Rekomendasi Makanan"
)

st.write(
    "Menggunakan Struktur Data Graph"
)

nama_user = st.text_input(
    "Nama User"
)

makanan = st.selectbox(
    "Pilih Makanan Favorit",
    [
        "Bakso",
        "Mie Ayam",
        "Seblak",
        "Nasi Goreng",
        "Sate",
        "Ayam Geprek"
    ]
)

if st.button("❤️ Tambah Favorit"):

    st.session_state.food.tambah_suka(
        nama_user,
        makanan
    )

    st.success(
        f"{makanan} ditambahkan"
    )

# =====================================
# REKOMENDASI
# =====================================

if st.button("🍽️ Cari Rekomendasi"):

    hasil = st.session_state.food.rekomendasi(
        nama_user
    )

    if hasil:

        st.subheader(
            "Rekomendasi Untuk Anda"
        )

        for makanan, skor in hasil:

            st.success(
                f"{makanan} ({skor} poin)"
            )

    else:

        st.warning(
            "Belum ada rekomendasi"
        )

# =====================================
# ADMIN PANEL
# =====================================

if st.session_state.admin:

    st.header("📊 Dashboard Admin")

    data = []

    for node, koneksi in st.session_state.food.graph.items():

        data.append({
            "Node": node,
            "Jumlah Koneksi": len(koneksi)
        })

    df = pd.DataFrame(data)

    st.dataframe(
        df,
        use_container_width=True
    )

    st.metric(
        "Total Node",
        len(df)
    )