import streamlit as st
import pandas as pd
import heapq

# ==================================================
# KONFIGURASI HALAMAN
# ==================================================

st.set_page_config(
    page_title="Rute Pengiriman Barang",
    page_icon="📦",
    layout="wide"
)

# ==================================================
# LINKED LIST
# ==================================================

class PengirimanNode:

    def __init__(
        self,
        kode,
        pengirim,
        penerima,
        asal,
        tujuan,
        berat,
        rute,
        jarak,
        biaya
    ):
        self.kode = kode
        self.pengirim = pengirim
        self.penerima = penerima
        self.asal = asal
        self.tujuan = tujuan
        self.berat = berat
        self.rute = rute
        self.jarak = jarak
        self.biaya = biaya
        self.next = None


class PengirimanLinkedList:

    def __init__(self):
        self.head = None

    def tambah_pengiriman(
        self,
        kode,
        pengirim,
        penerima,
        asal,
        tujuan,
        berat,
        rute,
        jarak,
        biaya
    ):

        node = PengirimanNode(
            kode,
            pengirim,
            penerima,
            asal,
            tujuan,
            berat,
            rute,
            jarak,
            biaya
        )

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

            data.append({
                "Kode": cur.kode,
                "Pengirim": cur.pengirim,
                "Penerima": cur.penerima,
                "Asal": cur.asal,
                "Tujuan": cur.tujuan,
                "Berat (Kg)": cur.berat,
                "Rute": cur.rute,
                "Jarak (Km)": cur.jarak,
                "Biaya": f"Rp {cur.biaya:,}"
            })

            cur = cur.next

        return data

    def total_pendapatan(self):

        total = 0

        cur = self.head

        while cur:
            total += cur.biaya
            cur = cur.next

        return total

    def update_pengiriman(
        self,
        kode,
        pengirim,
        penerima,
        berat
    ):

        cur = self.head

        while cur:

            if cur.kode == kode:

                cur.pengirim = pengirim
                cur.penerima = penerima
                cur.berat = berat

                return True

            cur = cur.next

        return False

    def hapus_pengiriman(self, kode):

        if not self.head:
            return False

        if self.head.kode == kode:
            self.head = self.head.next
            return True

        prev = self.head
        cur = self.head.next

        while cur:

            if cur.kode == kode:

                prev.next = cur.next
                return True

            prev = cur
            cur = cur.next

        return False


# ==================================================
# GRAPH
# ==================================================

graph = {

    "Jakarta": {
        "Bekasi": 20,
        "Tangerang": 15
    },

    "Bekasi": {
        "Jakarta": 20,
        "Bogor": 10,
        "Karawang": 25
    },

    "Tangerang": {
        "Jakarta": 15,
        "Bogor": 25,
        "Bandung": 30
    },

    "Bogor": {
        "Bekasi": 10,
        "Tangerang": 25,
        "Bandung": 20
    },

    "Bandung": {
        "Bogor": 20,
        "Tangerang": 30,
        "Cirebon": 35
    },

    "Karawang": {
        "Bekasi": 25,
        "Cirebon": 40
    },

    "Cirebon": {
        "Karawang": 40,
        "Bandung": 35
    }

}

# ==================================================
# DIJKSTRA
# ==================================================

def dijkstra(graph, start, end):

    pq = [(0, start)]

    distances = {
        node: float("inf")
        for node in graph
    }

    distances[start] = 0

    previous = {}

    while pq:

        current_distance, current_node = heapq.heappop(pq)

        for neighbor, weight in graph[current_node].items():

            distance = current_distance + weight

            if distance < distances[neighbor]:

                distances[neighbor] = distance

                previous[neighbor] = current_node

                heapq.heappush(
                    pq,
                    (distance, neighbor)
                )

    path = []

    current = end

    while current in previous:

        path.insert(0, current)

        current = previous[current]

    path.insert(0, start)

    return path, distances[end]


# ==================================================
# SESSION STATE
# ==================================================

if "pengiriman" not in st.session_state:
    st.session_state.pengiriman = PengirimanLinkedList()

if "admin_login" not in st.session_state:
    st.session_state.admin_login = False

# ==================================================
# HEADER
# ==================================================

st.title("📦 Sistem Rute Pengiriman Barang")

st.write(
    "Menggunakan Struktur Data Graph, Dijkstra dan Linked List"
)

# ==================================================
# LOGIN ADMIN
# ==================================================

st.sidebar.header("🔐 Login Admin")

username = st.sidebar.text_input(
    "Username"
)

password = st.sidebar.text_input(
    "Password",
    type="password"
)

if st.sidebar.button("Login"):

    if username == "admin" and password == "12345":

        st.session_state.admin_login = True

        st.sidebar.success(
            "Login Berhasil"
        )

    else:

        st.sidebar.error(
            "Login Gagal"
        )

if st.session_state.admin_login:

    st.sidebar.success(
        "✅ Admin Aktif"
    )

    if st.sidebar.button("Logout"):

        st.session_state.admin_login = False

        st.rerun()

# ==================================================
# FORM PENGIRIMAN
# ==================================================

st.sidebar.header("📝 Form Pengiriman")

pengirim = st.sidebar.text_input(
    "Nama Pengirim"
)

penerima = st.sidebar.text_input(
    "Nama Penerima"
)

asal = st.sidebar.selectbox(
    "Kota Asal",
    list(graph.keys())
)

tujuan = st.sidebar.selectbox(
    "Kota Tujuan",
    list(graph.keys())
)

berat = st.sidebar.number_input(
    "Berat Barang (Kg)",
    min_value=1,
    value=1
)

submit = st.sidebar.button(
    "📦 Proses Pengiriman"
)

# ==================================================
# INFORMASI KOTA
# ==================================================

st.header("🗺️ Jaringan Distribusi")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("Jakarta")
    st.info("Bekasi")
    st.info("Bogor")

with col2:
    st.info("Bandung")
    st.info("Karawang")

with col3:
    st.info("Tangerang")
    st.info("Cirebon")

# ==================================================
# PROSES PENGIRIMAN
# ==================================================

if submit:

    if pengirim == "" or penerima == "":

        st.warning(
            "Lengkapi data terlebih dahulu"
        )

    elif asal == tujuan:

        st.warning(
            "Asal dan tujuan tidak boleh sama"
        )

    else:

        path, jarak = dijkstra(
            graph,
            asal,
            tujuan
        )

        biaya = jarak * berat * 2500

        kode = (
            f"RESI-"
            f"{len(st.session_state.pengiriman.tampilkan_data())+1}"
        )

        st.session_state.pengiriman.tambah_pengiriman(
            kode,
            pengirim,
            penerima,
            asal,
            tujuan,
            berat,
            " ➜ ".join(path),
            jarak,
            biaya
        )

        st.success(
            "Pengiriman Berhasil Dibuat"
        )

        st.subheader(
            "📄 Detail Pengiriman"
        )

        st.info(
            f"""
Kode Resi : {kode}

Pengirim : {pengirim}

Penerima : {penerima}

Rute :
{' ➜ '.join(path)}

Jarak :
{jarak} KM

Berat :
{berat} Kg

Biaya :
Rp {biaya:,}
"""
        )

# ==================================================
# ADMIN PANEL
# ==================================================

st.divider()

if st.session_state.admin_login:

    st.header("📊 Dashboard Admin")

    data = st.session_state.pengiriman.tampilkan_data()

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Total Pengiriman",
            len(data)
        )

    with col2:
        st.metric(
            "Total Pendapatan",
            f"Rp {st.session_state.pengiriman.total_pendapatan():,}"
        )

    if data:

        df = pd.DataFrame(data)

        st.dataframe(
            df,
            use_container_width=True
        )

        st.subheader("✏️ Update Data")

        kode_update = st.selectbox(
            "Pilih Resi",
            [x["Kode"] for x in data]
        )

        pengirim_baru = st.text_input(
            "Pengirim Baru"
        )

        penerima_baru = st.text_input(
            "Penerima Baru"
        )

        berat_baru = st.number_input(
            "Berat Baru",
            min_value=1,
            value=1
        )

        if st.button(
            "Update Data"
        ):

            if st.session_state.pengiriman.update_pengiriman(
                kode_update,
                pengirim_baru,
                penerima_baru,
                berat_baru
            ):

                st.success(
                    "Data berhasil diupdate"
                )

        st.subheader("🗑️ Hapus Data")

        kode_hapus = st.selectbox(
            "Pilih Resi Yang Akan Dihapus",
            [x["Kode"] for x in data],
            key="hapus"
        )

        if st.button(
            "Hapus Pengiriman"
        ):

            if st.session_state.pengiriman.hapus_pengiriman(
                kode_hapus
            ):

                st.success(
                    "Data berhasil dihapus"
                )

                st.rerun()

    else:

        st.warning(
            "Belum ada data pengiriman"
        )

else:

    st.info(
        "🔒 Dashboard hanya dapat diakses Admin"
    )

# ==================================================
# FOOTER
# ==================================================

st.caption(
    "© 2026 | UAS Struktur Data | Graph + Dijkstra + Linked List + Streamlit"
)