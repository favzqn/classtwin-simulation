# Ringkasan Eksekutif Skripsi
## Pengembangan Digital Twin Ekosistem Kelas Berbasis Agent-Based Simulation untuk Analisis Faktor yang Mempengaruhi Kinerja Mahasiswa

**Nama:** Fauzan
**Program:** Skripsi S1
**Tanggal:** April 2026

---

## 1. Latar Belakang & Motivasi

Kepala program studi di perguruan tinggi Indonesia membuat keputusan kebijakan kelas setiap semester — ukuran kelas, batas pengembalian tugas, mode perkuliahan — sering kali tanpa data tentang dampaknya terhadap kinerja mahasiswa. Penelitian ini menjawab kebutuhan itu dengan membangun alat simulasi yang memungkinkan eksperimen kebijakan "bagaimana jika" sebelum diterapkan di kelas nyata.

---

## 2. Pendekatan: Agent-Based Simulation

Model yang dibangun adalah prototipe **Classroom Ecosystem Digital Twin** berbasis simulasi berbasis agen (ABS):

- **Agen:** 30 mahasiswa (*StudentAgent*) + 1 dosen (*LecturerAgent*)
- **Durasi:** 14 minggu (satu semester penuh)
- **Output:** IPK proksi, tingkat kehadiran, stres, putus studi
- **Dashboard:** Antarmuka Streamlit untuk pengguna non-teknis
- **Reprodusibilitas:** Random seed tetap → hasil identik setiap run

---

## 3. Pertanyaan Penelitian & Hasil

| No. | Pertanyaan | Jawaban Singkat |
|-----|-----------|----------------|
| RQ1 | Apakah ukuran kelas besar menurunkan kinerja? | **Ya** — kelas 60 orang: IPK turun 0,70 poin, gagal 10% |
| RQ2 | Apakah umpan balik cepat & beban ringan meningkatkan hasil? | **Ya** — umpan balik lambat (4 mgg): IPK turun 0,95 poin, gagal 30% |
| RQ3 | Apakah tutoring 4 minggu mempersempit kesenjangan? | **Ya** — IPK Q1 terbawah naik +0,10 poin |
| RQ4 | Apakah keberagaman SES memperlebar kesenjangan antar-kuartil? | **Tidak** — kesenjangan relatif justru mengecil, tapi IPK absolut Q1 tetap lebih rendah |
| RQ5 | Apakah suhu & mode perkuliahan berdampak terukur? | **Ya** — daring penuh: −0,48 IPK; kelas panas 32°C: −0,30 IPK |

---

## 4. Temuan Utama

### Rentang Dampak Kebijakan (IPK 0–4)

| Skenario | IPK Rata-rata | Selisih vs Baseline |
|----------|--------------|---------------------|
| Paket Kebijakan Terbaik | **3,47** | +0,46 |
| Umpan Balik Segera | 3,17 | +0,16 |
| Kelas Kecil (15 mhs) | 3,17 | +0,16 |
| **Baseline (30 mhs)** | **3,01** | — |
| Daring Penuh | 2,53 | −0,48 |
| Kelas Besar (60 mhs) | 2,32 | −0,70 |
| Umpan Balik Lambat (4 mgg) | 2,22 | −0,79 |
| Skenario Terburuk (gabungan) | 1,72 | −1,30 |

**Rentang total: 1,75 poin IPK** antara kondisi terbaik dan terburuk.

### Urutan Prioritas Faktor Kebijakan (Analisis Sensitivitas OAT)

1. **Keterlambatan umpan balik** → dampak terbesar (+0,95 IPK)
2. Ukuran kelas (+0,85)
3. Efektivitas pengajaran (+0,70)
4. Mode perkuliahan (+0,48)
5. Beban tugas (+0,37)
6. Suhu ruangan (+0,30)

---

## 5. Validasi Model

- **Validitas wajah:** Semua arah efek konsisten dengan literatur (Hattie 2008, Shute 2008, Means et al. 2010)
- **Determinisme:** Seed yang sama → hasil identik
- **Uji klem:** Semua variabel tetap dalam rentang valid [0,1]
- **Multi-seed robustness:** 20 replikasi per skenario → semua temuan terkonfirmasi
- **Konvergensi:** N=30 cukup stabil (CI ±0,04)

> **Catatan:** Ini adalah validitas wajah dan internal — bukan validitas prediktif. Parameter bersifat ilustratif, bukan hasil kalibrasi data LMS nyata.

---

## 6. Rekomendasi Kebijakan

| Prioritas | Kebijakan | Dampak | Biaya Implementasi |
|-----------|----------|--------|-------------------|
| 1 | Percepat pengembalian nilai (< 1 minggu) | +0,95 IPK (potensi) | Rendah |
| 2 | Batasi ukuran kelas (≤ 30 mahasiswa) | +0,85 IPK | Tinggi |
| 3 | Identifikasi dini + tutoring wk 7–10 | +0,10 IPK (Q1) | Sedang |
| 4 | Pastikan AC memadai (20–24°C) | +0,30 IPK | Sedang |
| 5 | Batasi beban tugas jika umpan balik terbatas | +0,37 IPK | Rendah |

---

## 7. Kontribusi & Keterbatasan

**Kontribusi:**
- Prototipe ABS classroom digital twin yang sepenuhnya open-source dan dapat direproduksi
- Dashboard Streamlit untuk pengguna non-teknis
- 15 skenario eksperimen yang menjawab 5 RQ

**Keterbatasan:**
- Parameter ilustratif, belum dikalibrasi data LMS nyata
- Satu mata kuliah, satu dosen
- Validitas eksternal belum diuji

**Arah pengembangan:** Kalibrasi dengan data SPADA/Moodle untuk mewujudkan digital twin prediktif penuh.

---

*Simulasi dapat didemonstrasikan secara langsung via dashboard Streamlit.*
