## BAB IV: HASIL DAN PEMBAHASAN

### 4.1 Hasil Skenario Baseline

Skenario baseline merepresentasikan kondisi kelas "standar": 30 mahasiswa, keterlambatan umpan balik 1 minggu, 2 tugas per minggu, suhu ruangan 22°C, perkuliahan tatap muka, dan tidak ada program intervensi.

Tabel 4.1 menyajikan metrik ringkasan skenario baseline.

**Tabel 4.1: Metrik Ringkasan Skenario Baseline**

| Metrik | Nilai |
|---|---|
| IPK Rata-rata (0–4) | 3,01 |
| Standar Deviasi IPK | 0,40 |
| Tingkat Kegagalan (IPK < 2,0) | 0% |
| Tingkat Kehadiran Rata-rata | 92,6% |
| Stres Akhir Rata-rata | 0,21 |
| Tingkat Putus Studi | 0% |

IPK rata-rata baseline 3,01 masuk dalam kategori "Sangat Memuaskan" pada skala penilaian perguruan tinggi Indonesia, mencerminkan kondisi kelas yang berjalan dengan baik tanpa tekanan berlebih. Gambar 4.1 menunjukkan evolusi pengetahuan rata-rata kelas selama 14 minggu simulasi, dengan pita ±1 SD. Pengetahuan meningkat secara monoton sepanjang semester meskipun dengan kecepatan yang sedikit menurun menjelang akhir akibat akumulasi kelelahan mahasiswa.

![Gambar 4.1](../../data/thesis_report/figures/knowledge_over_time.png)
*Gambar 4.1: Evolusi pengetahuan rata-rata kelas (±1 SD) selama 14 minggu simulasi (skenario baseline)*

Gambar 4.2 menunjukkan profil stres yang tetap berada pada rentang moderat (0,21 pada akhir semester).

![Gambar 4.2](../../data/thesis_report/figures/stress_over_time.png)
*Gambar 4.2: Profil stres rata-rata kelas selama 14 minggu simulasi (skenario baseline)*

### 4.2 Eksperimen Ukuran Kelas (RQ1)

Tiga skenario dibandingkan untuk menjawab RQ1: kelas kecil (15 mahasiswa), baseline (30), dan kelas besar (60).

**Tabel 4.2: Perbandingan Ukuran Kelas**

| Skenario | IPK Rata-rata | Tingkat Kegagalan | Tingkat Kehadiran | Stres Akhir |
|---|---|---|---|---|
| Kelas Kecil (15) | 3,17 | 0% | 95,2% | 0,22 |
| Baseline (30) | 3,01 | 0% | 92,6% | 0,21 |
| Kelas Besar (60) | 2,32 | 10% | 93,9% | 0,22 |

Hasil simulasi menunjukkan bahwa kelas besar (60 mahasiswa) menghasilkan IPK rata-rata 2,32, turun 0,70 poin dibandingkan baseline (3,01), sementara tingkat kegagalan naik dari 0% menjadi 10%. Kelas kecil (15 mahasiswa) menunjukkan IPK rata-rata 3,17, naik 0,16 poin dari baseline. Pola ini **menjawab RQ1 secara afirmatif**: ukuran kelas yang lebih besar berkorelasi negatif dengan kinerja akademik rata-rata dalam simulasi.

Untuk menginterpretasikan besaran dampak, selisih −0,70 poin pada kelas besar setara dengan **1,75 simpangan baku** distribusi baseline (SD = 0,40), yang tergolong *large effect size* berdasarkan konvensi Cohen (d ≥ 0,8). Sebaliknya, peningkatan +0,16 poin pada kelas kecil setara dengan 0,40 SD, tergolong *small-to-medium effect size*. Asimetri ini mengindikasikan bahwa kerugian akibat kelas besar jauh lebih besar daripada manfaat yang diperoleh dari memperkecil kelas.

Mekanisme di balik pola ini dapat dijelaskan sebagai berikut: pada kelas besar, efektivitas pengajaran per-mahasiswa menurun karena dosen memiliki kapasitas terbatas untuk memberikan perhatian individual. Seiring bertambahnya jumlah mahasiswa, penundaan umpan balik meningkat secara proporsional, yang berkontribusi pada akumulasi stres kelas.

Temuan ini konsisten dengan meta-analisis Hattie (2008) dan Glass & Smith (1979), meskipun *effect size* dalam simulasi ini bersifat ilustratif dan tidak dapat langsung dibandingkan secara numerik dengan studi empiris tersebut. Gambar 4.4 menunjukkan distribusi IPK proxy mahasiswa pada akhir semester untuk ketiga kondisi ukuran kelas.

![Gambar 4.4](../../data/thesis_report/figures/gpa_distribution.png)
*Gambar 4.4: Distribusi IPK proxy mahasiswa pada akhir semester*

### 4.3 Eksperimen Keterlambatan Umpan Balik (RQ2a)

Tiga kondisi dibandingkan: umpan balik segera (0 minggu), baseline (1 minggu), dan umpan balik sangat lambat (4 minggu).

**Tabel 4.3: Perbandingan Keterlambatan Umpan Balik**

| Skenario | IPK Rata-rata | Tingkat Kegagalan | Stres Akhir |
|---|---|---|---|
| Umpan Balik Segera (0 mgg) | 3,17 | 0% | 0,21 |
| Baseline (1 mgg) | 3,01 | 0% | 0,21 |
| Umpan Balik Lambat (4 mgg) | 2,22 | 30% | 0,49 |

Tren yang konsisten terlihat: semakin lambat umpan balik dikembalikan, semakin tinggi stres dan semakin rendah IPK. Perpindahan dari umpan balik segera ke umpan balik 4 minggu menurunkan IPK sebesar 0,95 poin dan meningkatkan tingkat kegagalan dari 0% menjadi 30%. Selisih ini setara dengan **2,37 simpangan baku** distribusi baseline — efek terbesar yang diamati dari seluruh intervensi variabel tunggal yang diuji dalam penelitian ini. Pada skenario umpan balik 4 minggu, efek akumulasi (*pending feedback*) dari beberapa tugas yang belum dikembalikan secara bersamaan menghasilkan lonjakan stres dari 0,21 menjadi 0,49.

Temuan ini **mendukung RQ2a** dan konsisten dengan tinjauan Shute (2008) yang menemukan bahwa keterlambatan umpan balik di atas dua minggu secara signifikan mengurangi dampak positif umpan balik terhadap pembelajaran.

Gambar 4.3 menunjukkan perbandingan profil stres dari ketiga kondisi sepanjang 14 minggu, mengilustrasikan divergensi yang semakin besar antara kondisi umpan balik segera dan umpan balik lambat setelah minggu ke-5.

![Gambar 4.3](../../data/thesis_report/figures/scenario_comparison.png)
*Gambar 4.3: Perbandingan IPK rata-rata seluruh skenario yang diuji*

### 4.4 Eksperimen Beban Tugas (RQ2b)

Tiga tingkat beban tugas dibandingkan: ringan (1/minggu), standar (2/minggu), dan berat (3/minggu).

**Tabel 4.4: Perbandingan Beban Tugas**

| Skenario | IPK Rata-rata | Tingkat Kegagalan | Stres Akhir |
|---|---|---|---|
| Beban Ringan (1/mgg) | 3,09 | 0% | 0,20 |
| Baseline (2/mgg) | 3,01 | 0% | 0,21 |
| Beban Berat (3/mgg) | 2,72 | 6,7% | 0,41 |

Skenario beban berat menghasilkan stres rata-rata yang lebih tinggi (0,41 vs 0,21) dan IPK yang lebih rendah (2,72 vs 3,01), sementara beban ringan menunjukkan hasil yang sedikit lebih baik. Pola ini **menjawab RQ2b secara afirmatif**. Selisih IPK −0,30 poin pada beban berat setara dengan **0,75 simpangan baku** distribusi baseline, tergolong *medium effect size* — lebih kecil dibandingkan dampak keterlambatan umpan balik (2,37 SD) maupun ukuran kelas (1,75 SD), yang konsisten dengan urutan prioritas dalam analisis OAT (lihat Bagian 4.9).

Meskipun pemberian tugas yang lebih banyak secara intuitif tampak mendorong mahasiswa untuk belajar lebih keras, dalam model ini peningkatan stres yang ditimbulkan justru mengurangi efektivitas pembelajaran, konsisten dengan mekanisme Yerkes-Dodson yang menjadi landasan model. Gambar 4.5 menampilkan evolusi motivasi rata-rata kelas, yang turut terpengaruh oleh akumulasi beban tugas.

![Gambar 4.5](../../data/thesis_report/figures/motivation_over_time.png)
*Gambar 4.5: Evolusi motivasi rata-rata kelas selama 14 minggu simulasi*

### 4.5 Skenario Kasus Terburuk

Skenario kasus terburuk menggabungkan kondisi paling merugikan secara bersamaan: 60 mahasiswa, 3 tugas per minggu, dan keterlambatan umpan balik 4 minggu. Dibandingkan dengan baseline:

- IPK rata-rata turun sebesar **1,30 poin** (dari 3,01 menjadi 1,72), setara dengan **3,25 simpangan baku** — jauh melampaui ambang *very large effect size*
- Tingkat kegagalan meningkat menjadi **90%**
- Tingkat putus studi mencapai **10%**

Temuan penting dari skenario ini adalah bahwa efek gabungan jauh lebih besar dibandingkan skenario tunggal terburuk sekalipun (keterlambatan umpan balik menghasilkan 30% kegagalan, bukan 90%), menunjukkan **efek interaksi non-linear** antara ukuran kelas, beban tugas, dan keterlambatan umpan balik. Ketika tekanan dari berbagai sumber menumpuk secara bersamaan, ambang putus studi mahasiswa jauh lebih mudah tercapai.

### 4.6 Eksperimen Program Tutoring (RQ3)

Skenario intervensi membandingkan kondisi baseline dengan kondisi di mana program tutoring diberikan kepada 25% mahasiswa berkinerja terendah pada minggu 7–10.

Sub-analisis dilakukan khusus untuk kelompok mahasiswa kuartil terbawah berdasarkan SES (Q1). Tabel 4.5 menunjukkan perbandingan.

**Tabel 4.5: Dampak Program Tutoring pada Kuartil Terbawah**

| Kondisi | IPK Rata-rata (Seluruh Kelas) | IPK Rata-rata (Q1 Terbawah) | Tingkat Kegagalan (Q1) |
|---|---|---|---|
| Baseline | 3,01 | 2,96 | 0% |
| Dengan Program Tutoring | 3,08 | 3,06 | 0% |
| Selisih (Delta) | +0,07 | +0,10 | 0% |

Hasil simulasi menunjukkan bahwa program tutoring berhasil meningkatkan IPK rata-rata mahasiswa kuartil terbawah sebesar 0,10 poin, sementara dampaknya terhadap IPK keseluruhan kelas sebesar +0,07. Peningkatan ini konsisten di seluruh 20 replikasi *seed* (Tabel 4.9). **RQ3 dijawab secara afirmatif**, meskipun dampaknya lebih terasa pada peningkatan IPK absolut mahasiswa lemah dibandingkan eliminasi kegagalan (karena tingkat kegagalan baseline sudah 0%).

Temuan tambahan dari Gambar 4.6: peningkatan pengetahuan kuartil terbawah mulai terlihat pada minggu ke-8, dengan tren positif yang berlanjut hingga akhir semester meskipun program berakhir pada minggu 10. Ini mengindikasikan adanya efek *momentum* dari intervensi yang berlanjut pasca-program.

![Gambar 4.6](../../data/thesis_report/figures/dropout_timeline.png)
*Gambar 4.6: Profil putus studi dan perkembangan kelompok intervensi selama 14 minggu simulasi*

### 4.7 Eksperimen Lingkungan Fisik dan Mode Perkuliahan (RQ5)

#### 4.7.1 Suhu Ruangan

Tiga kondisi suhu dibandingkan: kelas panas (32°C), baseline (22°C), dan kelas dingin (16°C).

**Tabel 4.6: Perbandingan Suhu Ruangan**

| Skenario | IPK Rata-rata | Tingkat Kegagalan | Tingkat Kehadiran | Stres Akhir |
|---|---|---|---|---|
| Kelas Panas (32°C) | 2,72 | 3,3% | 79,5% | 0,23 |
| Baseline (22°C) | 3,01 | 0% | 92,6% | 0,21 |
| Kelas Dingin (16°C) | 2,87 | 0% | 86,7% | 0,22 |

Kedua kondisi suhu ekstrem menunjukkan penurunan IPK dibandingkan baseline. Kelas panas (32°C) menurunkan IPK sebesar 0,30 poin dengan dampak kehadiran yang signifikan (turun dari 92,6% menjadi 79,5%). Kelas dingin (16°C) menunjukkan dampak yang lebih kecil (IPK turun 0,15 poin). Pola ini konsisten dengan temuan Wargocki dan Wyon (2007).

Dalam konteks Indonesia, temuan ini memiliki relevansi praktis: banyak ruang kelas menghadapi masalah suhu tinggi akibat iklim tropis. Simulasi ini menunjukkan bahwa penyediaan sistem pendingin udara yang memadai berpotensi meningkatkan capaian akademik mahasiswa secara nyata. Gambar 4.7 menampilkan perbandingan tingkat kehadiran rata-rata pada kondisi suhu berbeda.

![Gambar 4.7](../../data/thesis_report/figures/attendance_over_time.png)
*Gambar 4.7: Evolusi tingkat kehadiran rata-rata kelas selama 14 minggu simulasi*

#### 4.7.2 Mode Perkuliahan

Tiga mode perkuliahan dibandingkan: tatap muka (baseline), hibrida, dan daring penuh.

**Tabel 4.7: Perbandingan Mode Perkuliahan**

| Skenario | IPK Rata-rata | Tingkat Kegagalan | Tingkat Kehadiran | Stres Akhir |
|---|---|---|---|---|
| Tatap Muka | 3,01 | 0% | 92,6% | 0,21 |
| Hibrida | 2,81 | 0% | 93,8% | 0,21 |
| Daring Penuh | 2,53 | 6,7% | 95,2% | 0,21 |

Perkuliahan daring penuh menunjukkan IPK rata-rata yang lebih rendah (2,53 vs 3,01), dengan tingkat kegagalan 6,7%, meskipun tingkat kehadiran secara teknis lebih tinggi karena tidak ada hambatan fisik. Perkuliahan hibrida berada di antara keduanya (IPK 2,81).

Temuan ini **mendukung RQ5** dan konsisten dengan meta-analisis Means et al. (2010). Penting dicatat bahwa dalam model ini mode daring mengurangi efektivitas pengajaran dan laju pembelajaran teman sebaya; asumsi ini mungkin tidak berlaku jika desain pembelajaran daring dioptimalkan.

### 4.8 Eksperimen Keberagaman Status Sosial Ekonomi (RQ4)

Dua kondisi dibandingkan: baseline (std SES = 0,20) dan keberagaman SES tinggi (std = 0,40).

**Tabel 4.8: Kesenjangan IPK Berdasarkan Kuartil SES**

| Skenario | IPK Q1 (SES Rendah) | IPK Q4 (SES Tinggi) | Kesenjangan (Q4 − Q1) |
|---|---|---|---|
| Keberagaman SES Sedang / Baseline (std=0,20) | 2,96 | 3,17 | 0,21 |
| Keberagaman SES Tinggi (std=0,40) | 2,89 | 2,95 | 0,06 |

Hasil simulasi menunjukkan temuan yang menarik: kesenjangan IPK antara Q1 dan Q4 justru **lebih kecil** pada skenario keberagaman SES tinggi (0,06) dibandingkan baseline (0,21). Namun, IPK absolut mahasiswa Q1 pada skenario ses_diverse (2,89) lebih rendah dari baseline (2,96), mengonfirmasi bahwa mahasiswa SES rendah tetap dirugikan secara absolut.

Temuan ini sebagian konsisten dengan Sirin (2005) dalam hal dampak negatif SES rendah terhadap IPK absolut. Namun, hipotesis bahwa keberagaman lebih tinggi memperlebar kesenjangan antar-kuartil tidak terkonfirmasi dalam simulasi ini. Penjelasan yang mungkin adalah bahwa pada skenario ses_diverse, interaksi kelompok belajar yang lebih heterogen justru memberikan efek negatif merata ke semua kuartil, sehingga kesenjangan relatif antar-kuartil mengecil.

Temuan ini menyiratkan bahwa kebijakan pemerataan tetap relevan, terutama untuk meningkatkan IPK absolut mahasiswa SES rendah.

![Gambar 4.8](../../data/thesis_report/figures/ses_equity.png)
*Gambar 4.8: Analisis kesenjangan IPK berdasarkan kuartil SES pada skenario baseline dan ses_diverse*

### 4.9 Hasil Analisis Sensitivitas OAT

Gambar 4.9 menampilkan *tornado chart* dari analisis sensitivitas OAT terhadap metrik IPK rata-rata. Hasil analisis menunjukkan urutan dampak parameter sebagai berikut (dari terbesar ke terkecil):

1. **Keterlambatan umpan balik:** pengurangan dari 4 minggu ke 0 minggu meningkatkan IPK sebesar **0,95 poin**
2. **Ukuran kelas:** pengurangan dari 60 ke 15 mahasiswa meningkatkan IPK sebesar **0,85 poin**
3. **Efektivitas pengajaran:** peningkatan dari 0,7 ke 1,3 meningkatkan IPK sebesar **0,70 poin**
4. **Mode perkuliahan:** perubahan dari daring ke tatap muka meningkatkan IPK sebesar **0,48 poin**
5. **Beban tugas:** pengurangan dari 3 ke 1 tugas/minggu meningkatkan IPK sebesar **0,37 poin**
6. **Suhu ruangan:** perubahan dari 32°C ke 22°C meningkatkan IPK sebesar **0,30 poin**
7. **Pembelajaran teman sebaya:** pengaktifan meningkatkan IPK sebesar **0,18 poin**

![Gambar 4.9](../../data/thesis_report/figures/at_risk_comparison.png)
*Gambar 4.9: Analisis deteksi mahasiswa berisiko dan perbandingan antar-skenario*

Temuan kunci dari analisis sensitivitas adalah bahwa **keterlambatan umpan balik mendominasi**, diikuti oleh ukuran kelas dan efektivitas pengajaran yang memiliki dampak serupa. Beban tugas, yang sering menjadi fokus keluhan mahasiswa, berada di peringkat kelima. Ini mengonfirmasi bahwa kualitas umpan balik, ukuran kelas, dan kualitas pengajaran adalah tiga faktor kebijakan yang paling strategis untuk ditingkatkan.

Implikasi praktis: program studi sebaiknya memprioritaskan kebijakan pengembalian nilai yang cepat sebelum mempertimbangkan restrukturisasi ukuran kelas, karena umpan balik memberikan dampak terbesar dengan biaya implementasi yang relatif rendah.

Catatan penting: analisis OAT mengasumsikan independensi antar-parameter. Kombinasi beban tugas tinggi dan keterlambatan umpan balik menunjukkan efek interaksi yang jauh melampaui prediksi aditif (lihat Bagian 4.5).

### 4.10 Uji Robustisitas Multi-*Seed*

Untuk memastikan temuan direktional tidak bergantung pada satu *seed*, enam skenario kunci dijalankan masing-masing 20 kali dengan *seed* berbeda (0–19).

**Tabel 4.9: Hasil Multi-Seed (20 Replikasi per Skenario)**

| Skenario | IPK Rata-rata ± CI95 | Tingkat Kegagalan ± CI95 |
|---|---|---|
| Baseline | 3,04 ± 0,04 | 0,3% ± 0,4% |
| Umpan Balik Segera | 3,17 ± 0,04 | 0,2% ± 0,3% |
| Umpan Balik Lambat | 2,29 ± 0,04 | 26,8% ± 3,7% |
| Beban Berat | 2,80 ± 0,04 | 3,2% ± 1,2% |
| Program Tutoring | 3,11 ± 0,04 | 0,0% ± 0,0% |
| Daring Penuh | 2,57 ± 0,04 | 8,0% ± 2,4% |

Semua temuan direktional **terkonfirmasi** di seluruh 20 replikasi. Interval kepercayaan tidak tumpang tindih antar-skenario ekstrem (umpan balik segera 3,17 vs umpan balik lambat 2,29), mengindikasikan bahwa perbedaan yang ditemukan bersifat *robust* secara statistik dalam konteks simulasi ini.

### 4.11 Uji Konvergensi

Gambar 4.10 menampilkan hasil uji konvergensi: IPK rata-rata ± CI95 sebagai fungsi dari jumlah mahasiswa N (10, 15, 20, 30, 45, 60, 90, 120), masing-masing dihitung dari 10 *seed*.

![Gambar 4.10](../../data/thesis_report/figures/executive_dashboard.png)
*Gambar 4.10: Dashboard eksekutif simulasi menampilkan ringkasan metrik kelas*

CI semakin menyempit seiring meningkatnya N, mengonfirmasi bahwa simulasi menghasilkan estimasi yang semakin stabil. Pada N = 30 (baseline), CI sudah berada pada rentang ±0,04, cukup sempit untuk mendukung kesimpulan direktional. Nilai ini dipilih sebagai keseimbangan antara kestabilan statistik dan waktu komputasi yang wajar.

### 4.12 Ringkasan Seluruh Skenario

Tabel 4.10 merangkum hasil semua skenario yang dijalankan, berurutan dari IPK tertinggi ke terendah.

**Tabel 4.10: Ringkasan Hasil Seluruh Skenario**

| Peringkat | Skenario | IPK Rata-rata | Delta vs Baseline | Tingkat Kegagalan | Putus Studi |
|---|---|---|---|---|---|
| 1 | Paket Kebijakan Terbaik | 3,47 | +0,46 | 0% | 0% |
| 2 | Umpan Balik Segera | 3,17 | +0,16 | 0% | 0% |
| 3 | Kelas Kecil (15) | 3,17 | +0,16 | 0% | 0% |
| 4 | Beban Ringan | 3,09 | +0,08 | 0% | 0% |
| 5 | Program Tutoring | 3,08 | +0,07 | 0% | 0% |
| 6 | **Baseline** | **3,01** | **—** | **0%** | **0%** |
| 7 | SES Beragam | 2,98 | −0,03 | 0% | 0% |
| 8 | Kelas Dingin (16°C) | 2,87 | −0,15 | 0% | 0% |
| 9 | Hibrida | 2,81 | −0,21 | 0% | 0% |
| 10 | Beban Berat | 2,72 | −0,30 | 6,7% | 0% |
| 11 | Kelas Panas (32°C) | 2,72 | −0,30 | 3,3% | 0% |
| 12 | Daring Penuh | 2,53 | −0,48 | 6,7% | 0% |
| 13 | Kelas Besar (60) | 2,32 | −0,70 | 10% | 0% |
| 14 | Umpan Balik Lambat | 2,22 | −0,79 | 30% | 0% |
| 15 | Skenario Terburuk | 1,72 | −1,30 | 90% | 10% |

Paket Kebijakan Terbaik (*Best-Practice Bundle*), yang menggabungkan umpan balik segera, beban tugas ringan, dan program tutoring, menghasilkan IPK tertinggi (3,47) di antara semua skenario. Selisih antara skenario terbaik dan terburuk mencapai 1,75 poin IPK, menunjukkan bahwa pilihan kebijakan memiliki rentang dampak yang sangat besar terhadap capaian akademik mahasiswa.

### 4.13 Implikasi Kebijakan Akademik

Berdasarkan keseluruhan hasil eksperimen di atas, terdapat beberapa implikasi kebijakan yang dapat dipertimbangkan oleh institusi pendidikan tinggi.

**Prioritas utama: percepatan pengembalian umpan balik.** Analisis sensitivitas OAT menunjukkan bahwa keterlambatan umpan balik adalah faktor dengan dampak terbesar terhadap IPK (2,37 SD). Berbeda dari pengurangan ukuran kelas yang memerlukan penambahan tenaga pengajar, percepatan pengembalian tugas sering kali dapat diwujudkan melalui optimasi alur kerja penilaian atau pemanfaatan platform *Learning Management System* (LMS) dengan fitur umpan balik otomatis. Dengan kata lain, ini adalah intervensi berdampak besar dengan biaya implementasi yang relatif rendah.

**Manajemen beban tugas secara hati-hati.** Hasil simulasi menunjukkan bahwa kualitas dan ketepatan waktu umpan balik lebih menentukan capaian akademik dibandingkan kuantitas tugas. Penambahan tugas tanpa disertai kapasitas umpan balik yang memadai justru menurunkan IPK rata-rata. Program studi dapat mempertimbangkan pengurangan jumlah tugas jika sumber daya penilaian terbatas, sambil memastikan setiap tugas mendapatkan umpan balik yang cepat dan bermakna.

**Intervensi bertarget lebih efisien daripada perubahan kebijakan menyeluruh.** Program tutoring yang ditargetkan kepada 25% mahasiswa terendah (Seksi 4.6) menghasilkan peningkatan IPK kelompok terbawah sebesar +0,10 poin dengan biaya sumber daya yang jauh lebih kecil dibandingkan pengurangan ukuran kelas secara keseluruhan (+0,85 poin potensi dampak tetapi memerlukan penggandaan kapasitas ruang kelas). Ini mengindikasikan bahwa identifikasi dini mahasiswa berisiko dan intervensi tepat sasaran dapat menjadi strategi yang efisien secara sumber daya.

**Kondisi fisik ruang kelas tidak dapat diabaikan.** Dalam konteks Indonesia yang beriklim tropis, suhu ruangan yang tinggi (32°C, tanpa AC) menurunkan kehadiran secara signifikan (−13,1 persen poin) dan IPK sebesar 0,75 SD. Investasi pada sistem pendingin udara yang memadai berpotensi memberikan *return on investment* yang terukur dalam bentuk peningkatan capaian akademik.

**Dampak non-linear skenario gabungan.** Kombinasi kondisi buruk secara bersamaan menghasilkan efek yang jauh lebih destruktif daripada jumlah dampak individual. Ini mengimplikasikan bahwa kebijakan pencegahan harus bersifat proaktif dan holistis — memperbaiki satu faktor saja tidak cukup jika faktor lain tetap dalam kondisi buruk.

### 4.14 Keterbatasan Model Simulasi

Hasil penelitian ini perlu diinterpretasikan dengan memperhatikan beberapa keterbatasan inheren dari model simulasi yang dikembangkan.

**Pertama, asumsi perilaku yang disederhanakan.** Model ini merepresentasikan motivasi, stres, dan proses pembelajaran mahasiswa melalui persamaan deterministik berbasis bobot parameter. Perilaku manusia nyata jauh lebih kompleks, tidak linear, dan dipengaruhi oleh faktor kontekstual yang tidak dimodelkan, seperti dinamika keluarga, kondisi kesehatan mental, atau pengaruh media sosial. Hasil simulasi karena itu tidak boleh diinterpretasikan sebagai prediksi perilaku individu.

**Kedua, parameter model bersifat ilustratif, bukan empiris.** Nilai-nilai parameter seperti `base_learning_rate`, `w_feedback`, dan `stress_threshold` diturunkan dari pertimbangan teoritis dan kalibrasi manual untuk menghasilkan pola yang masuk akal secara kualitatif. Tidak ada kalibrasi berbasis dataset empiris berskala besar yang dilakukan dalam penelitian ini. Oleh karena itu, besaran numerik absolut (misalnya, IPK 3,01 atau selisih 0,70 poin) tidak boleh diinterpretasikan secara harfiah sebagai prediksi kelas nyata.

**Ketiga, homogenitas asumsi dosen.** Model mengasumsikan satu dosen dengan parameter tetap sepanjang semester. Kenyataannya, kualitas pengajaran bervariasi antarindividu dan dapat berubah seiring waktu akibat kelelahan, motivasi, atau perbedaan pendekatan pedagogis. Variabilitas ini tidak dimodelkan dalam prototipe saat ini.

**Keempat, validitas eksternal belum diuji.** Sebagaimana dijelaskan pada Bagian 3.10, validasi yang dilakukan dalam penelitian ini terbatas pada validitas wajah (*face validity*) dan konsistensi internal. Kemampuan model untuk memprediksi kelas nyata secara kuantitatif — validitas eksternal — memerlukan kalibrasi parameter menggunakan data LMS aktual, yang merupakan arah penelitian lanjutan.

**Kelima, konteks sosial yang disederhanakan.** Jaringan pertemanan, dinamika kelompok, pengaruh media sosial, dan tekanan dari luar kampus tidak dimodelkan secara eksplisit. Faktor-faktor ini dapat memiliki dampak signifikan pada motivasi dan kinerja mahasiswa di kelas nyata.

Keterbatasan-keterbatasan di atas tidak mengurangi nilai kontribusi prototipe ini sebagai alat eksplorasi kebijakan berbasis bukti kualitatif. Namun, penelitian lanjutan yang mengintegrasikan data empiris nyata diperlukan sebelum model ini dapat digunakan sebagai *digital twin* dalam pengertian prediktif penuh (Rasheed et al., 2020).
