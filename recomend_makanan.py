import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="FoodMatch AI",
    page_icon="🍔",
    layout="wide"
)

# ==========================================
# LINKED LIST
# ==========================================

class HistoryNode:
    def __init__(self, data):
        self.data = data
        self.next = None


class RecommendationHistory:

    def __init__(self):
        self.head = None

    def add(self, data):

        node = HistoryNode(data)

        if not self.head:
            self.head = node

        else:

            cur = self.head

            while cur.next:
                cur = cur.next

            cur.next = node

    def get_all(self):

        result = []

        cur = self.head

        while cur:

            result.append(cur.data)

            cur = cur.next

        return result


# ==========================================
# GRAPH
# ==========================================

class FoodGraph:

    def __init__(self):

        self.graph = {}

    def add_node(self, node):

        if node not in self.graph:
            self.graph[node] = set()

    def add_like(self, user, food):

        self.add_node(user)
        self.add_node(food)

        self.graph[user].add(food)
        self.graph[food].add(user)

    def recommend(self, target_user):

        if target_user not in self.graph:
            return []

        liked = self.graph[target_user]

        score = {}

        for food in liked:

            for other_user in self.graph[food]:

                if other_user != target_user:

                    for rec_food in self.graph[other_user]:

                        if rec_food not in liked:

                            score[rec_food] = (
                                score.get(rec_food, 0) + 1
                            )

        return sorted(
            score.items(),
            key=lambda x: x[1],
            reverse=True
        )


# ==========================================
# SESSION
# ==========================================

if "food_graph" not in st.session_state:

    st.session_state.food_graph = FoodGraph()

    # dummy

    st.session_state.food_graph.add_like(
        "Rina",
        "Bakso"
    )

    st.session_state.food_graph.add_like(
        "Rina",
        "Mie Ayam"
    )

    st.session_state.food_graph.add_like(
        "Dika",
        "Bakso"
    )

    st.session_state.food_graph.add_like(
        "Dika",
        "Seblak"
    )

    st.session_state.food_graph.add_like(
        "Salsa",
        "Nasi Goreng"
    )

    st.session_state.food_graph.add_like(
        "Salsa",
        "Seblak"
    )

if "history" not in st.session_state:
    st.session_state.history = RecommendationHistory()

if "admin" not in st.session_state:
    st.session_state.admin = False

if "foods" not in st.session_state:

    st.session_state.foods = [
        {
            "Nama": "Bakso",
            "Harga": 15000,
            "Kategori": "Berkuah"
        },
        {
            "Nama": "Seblak",
            "Harga": 18000,
            "Kategori": "Pedas"
        },
        {
            "Nama": "Mie Ayam",
            "Harga": 17000,
            "Kategori": "Mie"
        },
        {
            "Nama": "Nasi Goreng",
            "Harga": 20000,
            "Kategori": "Nasi"
        }
    ]

# ==========================================
# LOGIN ADMIN
# ==========================================

st.sidebar.header("🔐 Login Admin")

user_admin = st.sidebar.text_input(
    "Username"
)

pass_admin = st.sidebar.text_input(
    "Password",
    type="password"
)

if st.sidebar.button("Login Admin"):

    if user_admin == "admin" and pass_admin == "12345":

        st.session_state.admin = True

        st.sidebar.success(
            "Login berhasil"
        )

    else:

        st.sidebar.error(
            "Login gagal"
        )

# ==========================================
# HEADER
# ==========================================

st.title("🍔 FoodMatch AI")

st.write(
    "Sistem Rekomendasi Makanan Berbasis Graph"
)

# ==========================================
# USER
# ==========================================

st.header("👤 Pengguna")

nama_user = st.text_input(
    "Masukkan Nama Anda"
)

food_names = [
    item["Nama"]
    for item in st.session_state.foods
]

makanan = st.selectbox(
    "Pilih Makanan Favorit",
    food_names
)

if st.button("❤️ Tambah Favorit"):

    if nama_user:

        st.session_state.food_graph.add_like(
            nama_user,
            makanan
        )

        st.success(
            f"{makanan} ditambahkan"
        )

# ==========================================
# REKOMENDASI
# ==========================================

if st.button("🍽️ Cari Rekomendasi"):

    hasil = st.session_state.food_graph.recommend(
        nama_user
    )

    if hasil:

        st.subheader(
            "🎯 Rekomendasi Untuk Anda"
        )

        for makanan, skor in hasil:

            st.success(
                f"{makanan} | {skor} poin"
            )

            st.session_state.history.add(
                f"{nama_user} -> {makanan}"
            )

    else:

        st.warning(
            "Belum ada rekomendasi"
        )

# ==========================================
# VISUAL GRAPH
# ==========================================

st.header("🕸️ Visualisasi Graph")

G = nx.Graph()

for node, neighbors in st.session_state.food_graph.graph.items():

    for neighbor in neighbors:

        G.add_edge(node, neighbor)

fig, ax = plt.subplots(figsize=(8,5))

nx.draw(
    G,
    with_labels=True,
    node_size=1500,
    ax=ax
)

st.pyplot(fig)

# ==========================================
# HISTORY
# ==========================================

st.header("📜 Riwayat Rekomendasi")

history_data = st.session_state.history.get_all()

if history_data:

    for item in history_data:
        st.write(item)

# ==========================================
# ADMIN PANEL
# ==========================================

if st.session_state.admin:

    st.divider()

    st.header("📊 Dashboard Admin")

    df = pd.DataFrame(
        st.session_state.foods
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Total Menu",
            len(df)
        )

    with col2:

        st.metric(
            "Total Node",
            len(
                st.session_state.food_graph.graph
            )
        )

    st.dataframe(
        df,
        use_container_width=True
    )

    st.subheader(
        "➕ Tambah Menu"
    )

    nama = st.text_input(
        "Nama Makanan"
    )

    harga = st.number_input(
        "Harga",
        min_value=1000
    )

    kategori = st.text_input(
        "Kategori"
    )

    if st.button(
        "Tambah Menu"
    ):

        st.session_state.foods.append(
            {
                "Nama": nama,
                "Harga": harga,
                "Kategori": kategori
            }
        )

        st.success(
            "Menu berhasil ditambahkan"
        )

        st.rerun()

else:

    st.info(
        "🔒 Login Admin untuk mengakses dashboard"
    )

st.caption(
    "© 2026 | FoodMatch AI - Graph + Linked List"
)