import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import date

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Angket PDBK - Rekap Banyak Siswa",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def kategori_hambatan(pct: float) -> str:
    if pct <= 25:
        return "Hambatan Sangat Berat"
    if pct <= 50:
        return "Hambatan Berat"
    if pct <= 75:
        return "Hambatan Sedang"
    return "Hambatan Ringan"

# =========================
# ITEMS (43) - dapat diedit sesuai instrumen Anda
# =========================
ITEMS = []

def add_items(konstruk: str, sub: str, statements: list[str]):
    for s in statements:
        ITEMS.append({
            "Konstruk": konstruk,
            "Subdimensi": sub,
            "Item": s,
            "Skor": 1
        })

# HATI (15)
add_items("HATI", "Regulasi emosi", [
    "Peserta didik menunjukkan kesulitan menenangkan diri setelah emosi meningkat.",
    "Peserta didik bereaksi berlebihan terhadap situasi yang tidak sesuai harapan.",
    "Peserta didik mudah berubah mood dalam waktu singkat.",
    "Peserta didik sulit menerima koreksi atau arahan tanpa emosi.",
    "Peserta didik membutuhkan bantuan untuk menstabilkan emosi."
])
add_items("HATI", "Kontrol perilaku", [
    "Peserta didik menunjukkan perilaku impulsif (bertindak tanpa berpikir).",
    "Peserta didik sulit mengikuti aturan kelas secara konsisten.",
    "Peserta didik menunjukkan perilaku agresif (verbal/nonverbal).",
    "Peserta didik melakukan tindakan yang berpotensi membahayakan diri/lingkungan.",
    "Peserta didik sulit dihentikan saat melakukan perilaku tertentu."
])
add_items("HATI", "Interaksi sosial", [
    "Peserta didik menunjukkan kesulitan bekerja sama dengan teman.",
    "Peserta didik cenderung menarik diri dari interaksi sosial.",
    "Peserta didik sulit menunggu giliran saat aktivitas bersama.",
    "Peserta didik menunjukkan respons sosial yang kurang sesuai konteks.",
    "Peserta didik memerlukan pendampingan untuk berinteraksi secara positif."
])

# AKAL (16)
add_items("AKAL", "Atensi & fokus", [
    "Peserta didik mudah terdistraksi saat pembelajaran berlangsung.",
    "Peserta didik kesulitan mempertahankan perhatian sampai tugas selesai.",
    "Peserta didik memerlukan pengulangan instruksi agar dapat fokus.",
    "Peserta didik sering berhenti di tengah kegiatan tanpa alasan jelas."
])
add_items("AKAL", "Bahasa reseptif", [
    "Peserta didik kesulitan memahami instruksi sederhana.",
    "Peserta didik kesulitan memahami instruksi dua langkah atau lebih.",
    "Peserta didik kesulitan memahami pertanyaan lisan.",
    "Peserta didik tidak merespons panggilan secara konsisten."
])
add_items("AKAL", "Bahasa ekspresif", [
    "Peserta didik kesulitan mengungkapkan kebutuhan dengan kata-kata.",
    "Peserta didik menggunakan kosakata yang terbatas dibanding teman sebaya.",
    "Peserta didik kesulitan menyusun kalimat sederhana.",
    "Peserta didik lebih sering menggunakan gestur daripada verbal untuk berkomunikasi."
])
add_items("AKAL", "Kognitif dasar", [
    "Peserta didik mengalami kesulitan membaca (pengenalan huruf/kata).",
    "Peserta didik mengalami kesulitan berhitung dasar.",
    "Peserta didik kesulitan memahami konsep sederhana (besar-kecil, banyak-sedikit).",
    "Peserta didik memerlukan waktu lebih lama untuk menyelesaikan tugas akademik."
])

# JASAD (12)
add_items("JASAD", "Motorik kasar", [
    "Peserta didik mengalami kesulitan koordinasi gerak saat berjalan/berlari.",
    "Peserta didik kesulitan menjaga keseimbangan tubuh.",
    "Peserta didik kesulitan melakukan aktivitas motorik kasar (melompat/naik-turun tangga).",
    "Peserta didik mudah lelah saat aktivitas fisik ringan."
])
add_items("JASAD", "Motorik halus", [
    "Peserta didik kesulitan memegang alat tulis dengan stabil.",
    "Peserta didik kesulitan menebalkan/meniru bentuk sederhana.",
    "Peserta didik kesulitan aktivitas meronce/menggunting/melipat.",
    "Peserta didik kesulitan koordinasi tangan-mata saat tugas halus."
])
add_items("JASAD", "Fungsi sensorik", [
    "Peserta didik menunjukkan indikasi gangguan penglihatan saat aktivitas belajar.",
    "Peserta didik menunjukkan indikasi gangguan pendengaran saat menerima instruksi.",
    "Peserta didik sensitif terhadap suara keras dan menutup telinga.",
    "Peserta didik menunjukkan respons sensorik yang tidak sesuai (menjilat/menyentuh berlebihan)."
])

DF_TEMPLATE = pd.DataFrame(ITEMS)

# =========================
# STATE
# =========================
def init_state():
    if "df" not in st.session_state:
        st.session_state.df = DF_TEMPLATE.copy()
    if "rekap" not in st.session_state:
        st.session_state.rekap = pd.DataFrame(columns=[
            "Tanggal", "Sekolah", "Nama", "Kelas", "Pengisi",
            "Skor_HATI", "Skor_AKAL", "Skor_JASAD",
            "Total_Skor", "Skor_Maks", "Persentase", "Kategori"
        ])

init_state()

# =========================
# COMPUTE
# =========================
def compute_summary(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    summary = (
        df.groupby("Konstruk", as_index=False)
          .agg(Jumlah_Item=("Item", "count"), Skor_Total=("Skor", "sum"))
    )
    summary["Skor_Maks"] = summary["Jumlah_Item"] * 4
    summary["Persentase"] = (summary["Skor_Total"] / summary["Skor_Maks"] * 100).round(2)
    summary["Kategori"] = summary["Persentase"].apply(kategori_hambatan)

    total = int(df["Skor"].sum())
    maks = int(len(df) * 4)
    pct = round(total / maks * 100, 2)
    cat = kategori_hambatan(pct)

    skor_hati = int(df.loc[df["Konstruk"] == "HATI", "Skor"].sum())
    skor_akal = int(df.loc[df["Konstruk"] == "AKAL", "Skor"].sum())
    skor_jasad = int(df.loc[df["Konstruk"] == "JASAD", "Skor"].sum())

    meta = {
        "total": total,
        "maks": maks,
        "pct": pct,
        "cat": cat,
        "skor_hati": skor_hati,
        "skor_akal": skor_akal,
        "skor_jasad": skor_jasad,
    }
    return summary, meta

def export_excel(rekap: pd.DataFrame, df_items_last: pd.DataFrame | None = None) -> bytes:
    bio = BytesIO()
    with pd.ExcelWriter(bio, engine="openpyxl") as writer:
        rekap.to_excel(writer, sheet_name="Rekap", index=False)
        # Sheet opsional: item terakhir (agar jika perlu audit)
        if df_items_last is not None and not df_items_last.empty:
            df_items_last.to_excel(writer, sheet_name="Item_Terakhir", index=False)
    return bio.getvalue()

# =========================
# UI
# =========================
st.title("Angket PDBK — Rekap Banyak Siswa (1 Sheet)")
st.caption("Alur: isi skor → Simpan ke Rekap → lanjut siswa berikutnya → Unduh Excel rekap.")

with st.expander("Identitas (diisi setiap siswa)", expanded=True):
    c1, c2 = st.columns(2)
    sekolah = c1.text_input("Instansi/Sekolah", "")
    tanggal = c2.date_input("Tanggal", value=date.today())

    c3, c4 = st.columns(2)
    nama = c3.text_input("Nama Peserta Didik", "")
    kelas = c4.text_input("Kelas", "")

    pengisi = st.text_input("Nama Pengisi (Guru/Pendamping)", "")

tabs = st.tabs(["Isi Skor", "Rekap & Unduh"])

with tabs[0]:
    st.subheader("Isi Skor (43 Item)")
    st.info("Klik kolom **Skor** untuk memilih 1–4. Setelah selesai, buka tab **Rekap & Unduh** → Simpan ke Rekap.")

    konstruk_filter = st.selectbox("Filter konstruk", ["SEMUA", "HATI", "AKAL", "JASAD"], index=0)

    df_all = st.session_state.df

    if konstruk_filter == "SEMUA":
        df_view = df_all.copy().reset_index(drop=True)
    else:
        df_view = df_all[df_all["Konstruk"] == konstruk_filter].copy().reset_index(drop=True)

    edited = st.data_editor(
        df_view,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Skor": st.column_config.SelectboxColumn("Skor", options=[1,2,3,4], required=True)
        }
    )

    # Update df_all berdasarkan Item (unik)
    score_map = dict(zip(edited["Item"], edited["Skor"]))
    st.session_state.df["Skor"] = st.session_state.df["Item"].map(lambda x: int(score_map.get(x, st.session_state.df.loc[st.session_state.df["Item"] == x, "Skor"].iloc[0])))

with tabs[1]:
    st.subheader("Rekap Hasil")
    df_all = st.session_state.df
    summary, meta = compute_summary(df_all)

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Skor", f"{meta['total']}")
    m2.metric("Skor Maks", f"{meta['maks']}")
    m3.metric("Persentase", f"{meta['pct']}%")
    m4.metric("Kategori", meta["cat"])

    st.dataframe(summary, use_container_width=True, hide_index=True)
    st.divider()

    left, right = st.columns([1, 1])
    with left:
        if st.button("✅ Simpan hasil siswa ini ke Rekap"):
            if not nama.strip():
                st.error("Nama Peserta Didik wajib diisi sebelum menyimpan.")
            else:
                new_row = {
                    "Tanggal": str(tanggal),
                    "Sekolah": sekolah,
                    "Nama": nama,
                    "Kelas": kelas,
                    "Pengisi": pengisi,
                    "Skor_HATI": meta["skor_hati"],
                    "Skor_AKAL": meta["skor_akal"],
                    "Skor_JASAD": meta["skor_jasad"],
                    "Total_Skor": meta["total"],
                    "Skor_Maks": meta["maks"],
                    "Persentase": meta["pct"],
                    "Kategori": meta["cat"],
                }
                st.session_state.rekap = pd.concat([st.session_state.rekap, pd.DataFrame([new_row])], ignore_index=True)
                st.success("Tersimpan ke rekap. Silakan lanjut isi siswa berikutnya.")
    with right:
        if st.button("🔄 Reset skor untuk siswa berikutnya (semua = 1)"):
            st.session_state.df = DF_TEMPLATE.copy()
            st.success("Skor di-reset. Silakan isi siswa berikutnya.")

    st.subheader("Tabel Rekap (Banyak Siswa)")
    st.dataframe(st.session_state.rekap, use_container_width=True, hide_index=True)

    c1, c2 = st.columns([1, 1])
    with c1:
        st.download_button(
            "⬇️ Download Excel Rekap (1 Sheet)",
            data=export_excel(st.session_state.rekap, df_items_last=st.session_state.df),
            file_name=f"Rekap_Angket_PDBK_{str(tanggal)}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    with c2:
        if st.button("🗑️ Hapus semua rekap"):
            st.session_state.rekap = st.session_state.rekap.iloc[0:0].copy()
            st.success("Rekap dikosongkan.")
