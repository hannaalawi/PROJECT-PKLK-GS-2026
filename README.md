# Angket PDBK - Rekap Banyak Siswa (Streamlit)

Web app sederhana untuk mengisi angket PDBK dan menyimpan hasil banyak siswa ke 1 sheet Excel (Rekap).

## Jalankan lokal (PC/Laptop)
pip install -r requirements.txt
streamlit run app_angket_pdbk.py

## Deploy (Publik Link) - Streamlit Community Cloud
1) Buat repo GitHub (Public)
2) Upload: app_angket_pdbk.py, requirements.txt, README.md
3) Streamlit Community Cloud → New app → pilih repo → pilih app_angket_pdbk.py → Deploy
4) Dapat URL publik, bisa dibuka via Chrome Android.

Catatan:
- Setelah mengisi skor untuk 1 siswa: tab "Rekap & Unduh" → "Simpan hasil siswa ini ke Rekap"
- Klik "Reset skor" untuk lanjut siswa berikutnya
- Download Excel akan menghasilkan 1 sheet utama bernama "Rekap"
