# Persiapan Sidang — ClassTwin

## Kekuatan (sampaikan di presentasi)

- Implementasi nyata dan jalan — bukan prototipe konseptual
- Reproducibility dengan fixed seed — jarang ada di skripsi SI
- Validasi 4 lapis: face validity, determinisme, clamp test, konvergensi
- Landasan teori kuat: Hattie, Shute, Yerkes-Dodson, Vygotsky
- Jujur tentang keterbatasan (digital model, bukan digital twin penuh)
- Dashboard Streamlit = kontribusi praktis untuk non-teknis

---

## Kelemahan & Jawaban Sidang

### 1. "Temuan tautologis — hasilnya sudah diprediksi dari desain model"

**Pertanyaan penguji:** *"Kelas besar menghasilkan IPK lebih rendah karena Anda memang mendesain rules-nya begitu. Apa yang baru di sini?"*

**Jawaban:**
> Anda benar bahwa arah temuan konsisten dengan literatur — itu justru disengaja sebagai bagian validasi face validity. Kontribusi penelitian ini bukan pada penemuan hubungan baru, melainkan pada **artefak**: sebuah prototipe simulasi open-source yang reproducible, dapat dikonfigurasi, dan dilengkapi dashboard — yang belum tersedia sebelumnya untuk konteks perguruan tinggi Indonesia. Nilai utamanya adalah memungkinkan kaprodi membandingkan skenario kebijakan secara virtual sebelum diterapkan, bukan menghasilkan temuan empiris baru tentang psikologi pendidikan.

---

### 2. "Parameter illustratif — `base_learning_rate = 0.28` dari mana?"

**Pertanyaan penguji:** *"Bagaimana Anda memilih nilai parameter seperti 0.28? Apa justifikasinya?"*

**Jawaban:**
> Parameter dipilih melalui dua langkah. Pertama, **batas range** ditentukan dari literatur — misalnya efek ukuran kelas dari meta-analisis Hattie (2008) dan Glass & Smith (1979) memberikan batas atas/bawah yang masuk akal. Kedua, nilai spesifik di dalam range tersebut dipilih secara iteratif agar menghasilkan baseline IPK ~3.0, yang merepresentasikan kelas "normal" di PT Indonesia. Ini adalah pendekatan standar untuk model ABS eksplorasi kebijakan sebelum kalibrasi empiris — sebagaimana diakui secara eksplisit di Bab 3.10 dan Bab 5.3. Kalibrasi dengan data LMS nyata adalah saran penelitian lanjutan yang jelas.

---

### 3. "Judul menyebut Digital Twin tapi isinya Digital Model"

**Pertanyaan penguji:** *"Judul Anda pakai Digital Twin, tapi Anda sendiri mengakui ini cuma digital model tingkat 1. Mengapa tidak ganti judulnya?"*

**Jawaban:**
> Istilah "Digital Twin" dalam judul mengacu pada **paradigma** dan **aspirasi arsitektur**, bukan klaim kematangan penuh. Rasheed et al. (2020) dan Mousavi et al. (2024) mendefinisikan digital model sebagai tingkat pertama dari spektrum digital twin. Penelitian ini secara eksplisit memposisikan ClassTwin di tingkat tersebut — bukan menyembunyikannya. Penggunaan istilah "Digital Twin" di judul konsisten dengan literatur pendidikan yang menggunakan istilah ini secara inklusif, termasuk Batty (2018) untuk sistem sosial. Framing ini juga yang digunakan Bab 1.1 paragraf pertama dan Bab 3.10 poin 6.

---

### 4. "RQ4 kontradiksi Sirin (2005)"

**Pertanyaan penguji:** *"Hasil RQ4 Anda menunjukkan kesenjangan IPK tidak melebar saat SES diversity tinggi. Ini kontradiksi Sirin. Mengapa?"*

**Jawaban:**
> Kontradiksi ini bersifat parsial dan sudah diakui di Bab 5. Sirin (2005) menemukan SES rendah berdampak negatif pada IPK absolut — dan hasil simulasi mengkonfirmasi ini: IPK Q1 di skenario ses_diverse (2.50) lebih rendah dari baseline (2.60). Yang tidak terkonfirmasi adalah hipotesis bahwa *kesenjangan antar-kuartil* akan melebar. Mekanisme penyebabnya ada di desain model: peer learning dalam kelompok campuran SES justru membantu mahasiswa Q1 karena mereka berinteraksi dengan teman sebaya yang lebih kuat. Ini konsisten dengan teori ZPD Vygotsky — efek positif peer learning mengimbangi disadvantage SES rendah dalam model ini. Limitasi ini diakui karena model belum memperhitungkan faktor non-akademik SES seperti akses perangkat atau waktu belajar di rumah.

---

### 5. "Bab 3 terlalu tipis untuk metodologi"

**Pertanyaan penguji:** *"Metodologi Anda kurang detail. Bagaimana saya bisa mereplikasi model ini?"*

**Jawaban:**
> Reprodusibilitas penuh dijamin melalui dua mekanisme: (1) seluruh source code tersedia open-source dengan konfigurasi yang tersimpan bersama setiap eksperimen dalam format JSON, dan (2) fixed random seed memastikan output identik bit-per-bit. Detail formula update agen ada di Bab 3.4–3.6, dan tabel parameter lengkap tersedia di Bab 3.5. Siapapun dapat mereplikasi eksperimen dengan menjalankan `python -m src.experiments.runner` dengan seed yang sama.

---

## Pertanyaan Lain yang Mungkin Muncul

**"Bagaimana Anda memvalidasi bahwa model ini merepresentasikan kelas nyata?"**
> Validasi yang dilakukan adalah validasi wajah (face validity) — bukan validasi prediktif. Arah semua efek konsisten dengan 6+ sumber literatur (Hattie, Shute, Vygotsky, Sirin, ASHRAE 55, Means et al.). Validasi prediktif membutuhkan data LMS nyata dan merupakan pekerjaan masa depan yang sudah disebutkan di Bab 5.3.

**"Apa bedanya dengan simulasi Excel biasa?"**
> ABS memungkinkan heterogenitas individu secara eksplisit — setiap mahasiswa punya atribut berbeda dan berinteraksi satu sama lain. Excel bekerja di level populasi agregat dan tidak bisa menangkap perbedaan antar-individu, efek jaringan sosial, atau emergent behavior seperti dropout cascade.

**"Mengapa Mesa, bukan NetLogo?"**
> Mesa berbasis Python — lebih mudah diintegrasikan dengan ekosistem data science (pandas, matplotlib, Streamlit) dan lebih accessible untuk pengembangan lanjutan oleh peneliti yang tidak familiar dengan NetLogo. Juga memudahkan reproducibility karena semua dependensi bisa di-pin via requirements.txt.

---

## Yang Perlu Diperkuat di Skripsi (sebelum sidang)

- [ ] Bab 3: tambah tabel parameter lengkap + kolom "Dasar Literatur" untuk tiap parameter
- [ ] Bab 4: tambah paragraf eksplisit "mengapa temuan konsisten literatur tetap bernilai"
- [ ] Bab 4 RQ4: tambah penjelasan mekanisme peer learning vs SES disadvantage
- [ ] Bab 1: perkuat framing "digital model dalam spektrum digital twin"
- [ ] Bab 5: perkuat framing kontribusi = artefak open-source, bukan temuan baru
