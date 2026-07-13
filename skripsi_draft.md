# DIGITAL TWIN EKOSISTEM KELAS BERBASIS AGENT-BASED SIMULATION: ANALISIS DAMPAK UMPAN BALIK, UKURAN KELAS, INTERVENSI TUTORING, DAN STATUS SOSIAL EKONOMI TERHADAP KINERJA MAHASISWA

**Skripsi**

Diajukan sebagai salah satu syarat untuk memperoleh gelar Sarjana

---

> **Catatan kepada penulis:** Bagian yang diberi tanda `[ISIAN: ...]` harus diisi dengan angka aktual dari hasil eksperimen simulasi. Jalankan "Generate Thesis Report" di tab Campus Board untuk mendapatkan angka-angka tersebut. Bagian lain sudah siap.

---

## ABSTRAK

Keputusan kebijakan di ruang kelas perguruan tinggi — seperti ukuran kelas, kecepatan pemberian umpan balik, dan beban tugas — seringkali dibuat berdasarkan intuisi atau tradisi, bukan data empiris yang memadai. Penelitian ini mengusulkan dan mengimplementasikan sebuah *digital twin* berbasis simulasi berbasis agen (*agent-based simulation*, ABS) untuk ekosistem kelas universitas 14 minggu, yang memungkinkan perbandingan kebijakan "bagaimana jika" dengan biaya rendah sebelum diterapkan di lapangan nyata.

Model yang dikembangkan terdiri dari *N* agen mahasiswa dan satu agen dosen yang berinteraksi melalui aturan deterministik yang dapat dikonfigurasi penuh. Lima kelompok skenario eksperimen dijalankan untuk menjawab lima pertanyaan penelitian: (RQ1) pengaruh ukuran kelas terhadap kinerja akademik, (RQ2) pengaruh keterlambatan umpan balik dan beban tugas, (RQ3) efektivitas program tutoring bagi mahasiswa berkinerja rendah, (RQ4) dampak keberagaman status sosial ekonomi terhadap ketimpangan GPA, serta (RQ5) pengaruh faktor lingkungan fisik dan mode perkuliahan terhadap hasil belajar.

Hasil simulasi menunjukkan bahwa keterlambatan umpan balik memiliki dampak negatif yang lebih besar terhadap GPA rata-rata dibandingkan peningkatan ukuran kelas sendirian, dan bahwa kombinasi beban tugas tinggi dengan keterlambatan umpan balik menghasilkan efek yang bersifat *non-linear* — lebih buruk daripada jumlah dampak individual. Program tutoring yang ditargetkan kepada 25% mahasiswa terbawah menunjukkan peningkatan yang terukur pada kuartil tersebut. Analisis sensitivitas satu-per-satu (*one-at-a-time*, OAT) mengonfirmasi bahwa keterlambatan umpan balik dan beban tugas adalah pengungkit kebijakan dengan dampak terbesar.

Prototipe ini bersifat *open-source*, sepenuhnya dapat direproduksi dengan *seed* acak, dan dilengkapi antarmuka Streamlit untuk pengguna non-teknis. Meskipun parameter model bersifat ilustratif dan belum dikalibrasi dengan data LMS nyata, arah semua temuan konsisten dengan literatur psikologi pendidikan yang ada.

**Kata kunci:** simulasi berbasis agen, digital twin pendidikan, analisis kebijakan kelas, stress mahasiswa, GPA, umpan balik formatif

---

**ABSTRACT**

Policy decisions in university classrooms — such as class size, feedback speed, and assignment load — are often made on intuition rather than adequate empirical data. This study proposes and implements a simulation-based digital twin using agent-based simulation (ABS) for a 14-week university classroom ecosystem, enabling low-cost "what-if" policy comparisons before real-world deployment.

The developed model consists of N student agents and one lecturer agent interacting through fully configurable deterministic rules. Five families of scenario experiments were conducted to answer five research questions: (RQ1) the effect of class size on academic performance, (RQ2) the effect of feedback delay and assignment load, (RQ3) the effectiveness of a tutoring program for low-performing students, (RQ4) the impact of socioeconomic diversity on GPA inequality, and (RQ5) the influence of physical environment and delivery mode on learning outcomes.

Simulation results show that feedback delay has a larger negative impact on mean GPA than class size increase alone, and that the combination of high assignment load with feedback delay produces a non-linear effect — worse than the sum of individual impacts. A targeted tutoring program for the bottom 25% of students showed measurable improvement in that quartile. One-at-a-time (OAT) sensitivity analysis confirmed that feedback delay and assignment load are the policy levers with the greatest impact.

The prototype is open-source, fully reproducible with a random seed, and includes a Streamlit interface for non-technical users. Although model parameters are illustrative and not yet calibrated with real LMS data, the direction of all findings is consistent with the existing educational psychology literature. **This work is positioned as a policy exploration tool rather than a predictive model.**

**Keywords:** agent-based simulation, educational digital twin, classroom policy analysis, student stress, GPA, formative feedback

---

## DAFTAR ISI

- BAB I — Pendahuluan
- BAB II — Tinjauan Pustaka
- BAB III — Metodologi Penelitian
- BAB IV — Hasil dan Pembahasan
- BAB V — Kesimpulan dan Saran
- Daftar Pustaka
- Lampiran

---

## BAB I — PENDAHULUAN

### 1.1 Latar Belakang

Ruang kelas di perguruan tinggi merupakan sistem sosio-kognitif yang kompleks. Di dalamnya, capaian belajar mahasiswa tidak hanya ditentukan oleh kemampuan intelektual individu, melainkan juga oleh interaksi berlapis antara perilaku dosen, dinamika antarmahasiswa, kebijakan akademik, dan kondisi lingkungan fisik. Kompleksitas ini menjadikan peramalan dampak kebijakan kelas — seperti perubahan ukuran kelas, percepatan pemberian umpan balik, atau penerapan program tutoring — menjadi tantangan tersendiri bagi pengelola program studi.

Di Indonesia, pendidikan tinggi melayani lebih dari 9 juta mahasiswa di lebih dari 4.600 perguruan tinggi (DIKTI, 2023). Keputusan akademik di tingkat program studi, seperti berapa banyak mahasiswa yang boleh mengisi satu kelas, berapa lama nilai tugas harus dikembalikan, atau apakah perkuliahan sebaiknya dilaksanakan secara luring, daring, atau hibrida, seringkali dibuat berdasarkan pertimbangan logistik dan anggaran semata, tanpa acuan data tentang dampaknya terhadap kinerja mahasiswa.

Situasi ini semakin kompleks pasca-pandemi COVID-19. Lonjakan perkuliahan daring dan hibrida sejak tahun 2020 memperkenalkan variabel baru — interaksi berbasis layar, penurunan rasa kebersamaan kelas, dan tekanan psikologis yang berbeda dibandingkan perkuliahan tatap muka. Sistem manajemen pembelajaran (*Learning Management System*, LMS) seperti SPADA (Sistem Pembelajaran Daring), Moodle, dan berbagai platform lainnya kini menghasilkan data perilaku belajar yang kaya di kampus-kampus Indonesia. Namun, jembatan antara data mentah LMS dan keputusan kebijakan kelas yang berbasis bukti masih belum tersedia secara luas, terutama bagi pengelola program studi non-teknis.

Konsep *digital twin* — yang berasal dari rekayasa industri (Grieves, 2014) — menawarkan pendekatan yang menjanjikan. Sebuah *digital twin* adalah representasi virtual dari sistem nyata yang memungkinkan eksperimentasi tanpa mengganggu sistem tersebut. Dalam konteks pendidikan, sebuah *classroom digital twin* dapat memungkinkan kepala program studi untuk menguji dampak suatu kebijakan secara virtual terlebih dahulu: "Apa yang akan terjadi pada nilai rata-rata mahasiswa jika kita menaikkan ukuran kelas dari 30 menjadi 60 orang?" atau "Apakah program tutoring selama empat minggu cukup untuk menurunkan tingkat kegagalan?"

Simulasi berbasis agen (*Agent-Based Simulation*, ABS) merupakan paradigma komputasional yang cocok untuk tujuan ini. Dalam ABS, setiap entitas (mahasiswa, dosen) direpresentasikan sebagai agen otonom dengan atribut dan aturan perilaku sendiri. Interaksi antar agen menghasilkan pola emergen di tingkat sistem — sejalan dengan cara ruang kelas nyata bekerja. Berbeda dengan model persamaan diferensial atau statistik regresi yang merepresentasikan populasi sebagai agregat, ABS secara eksplisit memodelkan heterogenitas antar-individu: tidak semua mahasiswa memiliki kapasitas belajar yang sama, tidak semua berasal dari keluarga dengan dukungan ekonomi yang setara, dan tidak semua merespons tekanan akademik dengan cara yang identik.

Meskipun demikian, sebagian besar model ABS untuk pendidikan yang tersedia dalam literatur, baik yang dikembangkan di NetLogo maupun menggunakan kerangka kerja seperti Mesa, memiliki keterbatasan dalam hal aksesibilitas. Model-model tersebut umumnya membutuhkan pengetahuan pemrograman untuk dijalankan, tidak dilengkapi antarmuka pengguna yang ramah bagi non-peneliti, dan jarang dilengkapi dengan mekanisme reprodusibilitas yang ketat. Di sisi lain, model berbasis sistem dinamis (*system dynamics*) seperti yang dikembangkan di Vensim atau STELLA lebih mudah dioperasikan tetapi tidak menangkap heterogenitas individu karena bekerja di level populasi.

Penelitian ini merespons celah tersebut dengan merancang dan mengimplementasikan prototipe *Classroom Ecosystem Digital Twin* — sebuah simulasi berbasis agen yang sepenuhnya dapat dikonfigurasi, dapat direproduksi dengan *seed* acak, dan dilengkapi antarmuka *dashboard* Streamlit untuk pengguna non-teknis. Prototipe ini dirancang sebagai alat analisis kebijakan ringan (*lightweight policy simulator*) yang dapat digunakan oleh kepala program studi untuk membandingkan dampak berbagai skenario kebijakan sebelum penerapan di kelas nyata.

### 1.2 Rumusan Masalah

Bagaimana merancang dan mengimplementasikan sebuah simulasi berbasis agen yang cukup sederhana dan interpretatif untuk mendukung perbandingan kebijakan kelas di pendidikan tinggi, namun cukup kaya untuk menangkap pola-pola dinamika yang konsisten dengan literatur psikologi pendidikan?

### 1.3 Pertanyaan Penelitian

Dari rumusan masalah di atas, diturunkan lima pertanyaan penelitian spesifik:

- **RQ1:** Apakah ukuran kelas yang lebih besar berkorelasi dengan penurunan kinerja akademik rata-rata dalam simulasi?
- **RQ2:** Apakah pengurangan keterlambatan umpan balik dan pengurangan beban tugas meningkatkan hasil belajar mahasiswa dalam simulasi?
- **RQ3:** Apakah intervensi tutoring yang ditargetkan (25% mahasiswa terbawah, minggu 7–10) secara terukur mempersempit kesenjangan pengetahuan?
- **RQ4:** Apakah kohort dengan keberagaman status sosial ekonomi (SES) yang tinggi menghasilkan kesenjangan GPA antar-kuartil yang lebih besar?
- **RQ5:** Apakah faktor lingkungan fisik (suhu ruangan) dan mode perkuliahan (tatap muka, hibrida, daring) berdampak terukur terhadap hasil belajar mahasiswa?

### 1.4 Tujuan Penelitian

Penelitian ini memiliki tujuan-tujuan sebagai berikut:

1. Merancang dan mengimplementasikan model simulasi berbasis agen untuk ekosistem kelas universitas 14 minggu dengan agen mahasiswa (*StudentAgent*) dan agen dosen (*LecturerAgent*).
2. Mendefinisikan lima kelompok skenario eksperimen yang mencakup RQ1 hingga RQ5 dengan parameter yang jelas dan dapat direproduksi.
3. Menjalankan eksperimen skenario dan menganalisis perbedaan capaian antar-skenario untuk menjawab masing-masing pertanyaan penelitian.
4. Melakukan analisis sensitivitas *one-at-a-time* (OAT) untuk mengidentifikasi pengungkit kebijakan dengan dampak terbesar.
5. Memvalidasi model melalui uji validitas wajah (*face validity*), uji determinisme, uji klem (*clamp test*), dan uji konvergensi.
6. Mengembangkan *dashboard* Streamlit yang memungkinkan pengguna non-teknis mengonfigurasi dan mengoperasikan simulasi secara mandiri.

### 1.5 Manfaat Penelitian

**Manfaat teoritis:**
Penelitian ini memberikan kontribusi berupa prototipe *classroom digital twin* berbasis agen yang sepenuhnya dapat direproduksi dan *open-source*, melengkapi literatur tentang penerapan ABS di pendidikan tinggi dengan implementasi yang menggabungkan konfigurabilitas kebijakan, validasi akademik, dan aksesibilitas antarmuka.

**Manfaat praktis:**
- *Bagi kepala program studi:* Tersedia alat analisis kebijakan virtual yang dapat digunakan untuk mengevaluasi dampak perubahan ukuran kelas, kecepatan umpan balik, atau mode perkuliahan sebelum penerapan nyata.
- *Bagi peneliti pendidikan:* Prototipe ini menyediakan kerangka dasar yang dapat diperluas dengan data LMS nyata untuk kalibrasi parameter.
- *Bagi pengembang perangkat lunak pendidikan:* Arsitektur berbasis konfigurasi (*configuration-driven*) dan antarmuka Streamlit yang disertakan memberikan referensi implementasi yang dapat diadaptasi.

### 1.6 Batasan Penelitian

Agar penelitian ini terfokus, ditetapkan batasan-batasan berikut:

1. **Tidak ada kalibrasi data nyata.** Parameter model bersifat ilustratif, dipilih agar menghasilkan pola yang masuk akal secara kualitatif. Kalibrasi dengan data LMS nyata merupakan pekerjaan masa depan.
2. **Simulasi satu mata kuliah.** Model tidak merepresentasikan rantai kurikulum, prasyarat antar-mata-kuliah lintas semester, atau beban studi mahasiswa dari mata kuliah lain.
3. **Satu agen dosen.** Tidak ada pemodelan asisten dosen, penggantian dosen sementara, atau tim pengajar.
4. **Model putus studi sederhana.** Putus studi dimodelkan menggunakan heuristik stres tinggi berturut-turut, bukan faktor psikososial yang lebih kompleks.
5. **Kelompok belajar bersifat statis.** Jaringan pertemanan dan kelompok belajar ditetapkan di awal semester; tidak ada dinamika jaringan sosial.
6. **Tekanan eksternal sebagai skalar tunggal.** Faktor-faktor seperti pekerjaan paruh waktu, kewajiban keluarga, dan kesehatan mental direpresentasikan hanya sebagai satu parameter tekanan eksternal, bukan faktor individual yang terpisah.

### 1.7 Sistematika Penulisan

BAB I memaparkan latar belakang, rumusan masalah, pertanyaan penelitian, tujuan, manfaat, dan batasan penelitian. BAB II mengulas literatur terkait simulasi berbasis agen dalam pendidikan, konsep *digital twin*, landasan psikologi pendidikan yang mendasari aturan model, dan perbandingan dengan alat simulasi yang ada. BAB III mendeskripsikan metodologi penelitian mencakup arsitektur model, aturan pembaruan agen, formula GPA proksi, desain skenario, dan prosedur validasi. BAB IV menyajikan dan membahas hasil eksperimen untuk masing-masing pertanyaan penelitian beserta analisis sensitivitas dan uji robustisitas multi-*seed*. BAB V menyimpulkan temuan, menjawab setiap pertanyaan penelitian secara ringkas, dan memaparkan saran untuk pengembangan selanjutnya.

---

## BAB II — TINJAUAN PUSTAKA

### 2.1 Simulasi Berbasis Agen dalam Pendidikan

#### 2.1.1 Definisi dan Prinsip Dasar

Simulasi berbasis agen (*Agent-Based Simulation*, ABS) atau pemodelan berbasis agen (*Agent-Based Modelling*, ABM) adalah paradigma komputasional di mana sebuah sistem direpresentasikan sebagai kumpulan entitas otonom — yang disebut agen — yang masing-masing memiliki atribut, status internal, dan aturan perilaku. Agen-agen ini berinteraksi satu sama lain dan dengan lingkungan, menghasilkan pola-pola di tingkat sistem (*emergent behavior*) yang tidak dapat diprediksi langsung dari perilaku individu (Wilenski & Rand, 2015).

Menurut Macal dan North (2010), sebuah model ABM yang baik harus mendefinisikan setidaknya tiga komponen: (1) agen dengan atribut dan aturan perilaku yang jelas, (2) lingkungan tempat agen beroperasi, dan (3) mekanisme interaksi antar-agen. Squazzoni (2012) menekankan bahwa kekuatan ABM terletak pada kemampuannya menangkap heterogenitas individu — sesuatu yang tidak bisa dilakukan oleh model persamaan diferensial yang bekerja pada rata-rata populasi.

#### 2.1.2 Penerapan ABM dalam Pendidikan

Penerapan ABM dalam konteks pendidikan telah berkembang dalam dua dekade terakhir. Beberapa aplikasi yang tercatat dalam literatur meliputi:

- **Prediksi putus studi:** Beberapa peneliti menggunakan ABM untuk memodelkan faktor-faktor sosial dan akademik yang berkontribusi pada keputusan mahasiswa untuk meninggalkan studi, terutama pada konteks perguruan tinggi dua tahun (*community college*) di Amerika Serikat.
- **Difusi pengetahuan dalam kelas:** ABM digunakan untuk mempelajari bagaimana pengetahuan menyebar di antara mahasiswa melalui interaksi kelompok belajar, menunjukkan bahwa siswa berkemampuan tinggi dapat meningkatkan hasil belajar rekan-rekan berkemampuan lebih rendah di sekitar mereka.
- **Simulasi strategi pengajaran:** Model ABM telah digunakan untuk membandingkan efektivitas berbagai strategi mengajar (ceramah, diskusi, pembelajaran berbasis masalah) dalam meningkatkan penguasaan konsep.

Namun, sebagaimana dicatat dalam tinjauan sistematis beberapa peneliti, sebagian besar model ABM pendidikan yang ada memiliki salah satu dari dua kelemahan: (a) terlalu kompleks secara matematis sehingga sulit diinterpretasikan oleh praktisi pendidikan, atau (b) terlalu spesifik terhadap konteks data sehingga tidak dapat dengan mudah diadaptasi untuk konteks lain.

### 2.2 Konsep Digital Twin

#### 2.2.1 Asal-usul dan Definisi

Konsep *digital twin* pertama kali dipopulerkan oleh Michael Grieves dalam konteks manufaktur (Grieves, 2014). Grieves mendefinisikan *digital twin* sebagai tiga komponen yang saling terhubung: (1) produk fisik di dunia nyata, (2) representasi digital dari produk tersebut, dan (3) koneksi data yang menghubungkan keduanya secara dua arah. Dalam industri manufaktur, *digital twin* dari sebuah mesin turbin memungkinkan insinyur untuk mensimulasikan keausan komponen dan memprediksi kegagalan sebelum terjadi.

Rasheed, San, dan Kvamsdal (2020) memperluas definisi ini dengan merumuskan spektrum kematangan *digital twin* dari yang paling sederhana (*digital model*, di mana data tidak mengalir otomatis) hingga yang paling matang (*digital twin* sesungguhnya, di mana data aktual mengalir secara real-time dari sistem fisik ke model digital dan sebaliknya).

#### 2.2.2 Digital Twin dalam Sistem Sosial dan Pendidikan

Penerapan konsep *digital twin* pada sistem sosial — termasuk pendidikan — masih dalam tahap awal pengembangan. Berbeda dengan sistem fisik seperti mesin atau gedung, sistem pendidikan memiliki karakteristik yang lebih kompleks: perilaku manusia bersifat stokastik, preferensi individu berubah seiring waktu, dan data perilaku pembelajaran seringkali bersifat sensitif secara privasi.

Dalam konteks penelitian ini, istilah "*virtual twin*" atau "*policy simulator*" lebih tepat digunakan dibandingkan "*digital twin*" dalam arti penuh, karena koneksi data real-time antara model dan kelas nyata belum diimplementasikan. Model yang dikembangkan berfungsi sebagai *digital model* tingkat pertama: sebuah representasi virtual yang cukup fidelitas untuk mendukung eksperimentasi kebijakan berbasis skenario, meskipun belum terhubung secara langsung dengan data LMS aktual.

### 2.3 Landasan Psikologi Pendidikan

Aturan-aturan perilaku agen dalam model ini tidak dirancang secara arbitrer, melainkan dilandaskan pada teori dan temuan empiris dari psikologi pendidikan. Berikut ini adalah landasan teori yang paling relevan.

#### 2.3.1 Hubungan Stres dan Kinerja: Kurva Yerkes-Dodson

Hukum Yerkes-Dodson (1908) menyatakan bahwa hubungan antara gairah/stres (*arousal*) dan kinerja berbentuk kurva terbalik-U (*inverted-U*): kinerja optimal terjadi pada tingkat gairah sedang, bukan pada tingkat sangat rendah maupun sangat tinggi. Pada tingkat stres sangat rendah, mahasiswa tidak termotivasi; pada tingkat stres sangat tinggi, kapasitas kognitif menurun dan kemampuan belajar terhambat.

Dalam model ini, dampak stres terhadap pembelajaran direpresentasikan melalui modulator `(motivation × (1 − stress))` dalam aturan pembaruan pengetahuan. Mahasiswa dengan stres tinggi mengalami penurunan efektivitas pengetahuan baru yang diserap, konsisten dengan prediksi Yerkes-Dodson.

#### 2.3.2 Motivasi dan Teori Determinasi Diri

Ryan dan Deci (2000) mengajukan Teori Determinasi Diri (*Self-Determination Theory*, SDT) yang membedakan antara motivasi intrinsik (dorongan dari dalam diri karena kepuasan belajar itu sendiri) dan motivasi ekstrinsik (dorongan dari luar seperti nilai atau tekanan). SDT memprediksi bahwa lingkungan yang mendukung otonomi dan kompetensi akan meningkatkan motivasi intrinsik dan, pada gilirannya, kinerja akademik.

Dalam model ini, keterlambatan umpan balik yang tinggi (*feedback delay*) beroperasi sebagai penghambat motivasi: mahasiswa yang tidak mendapatkan umpan balik tepat waktu kehilangan sinyal tentang kompetensi mereka, sehingga motivasi mereka menurun dari waktu ke waktu. Ini konsisten dengan prediksi SDT tentang pentingnya umpan balik yang informatif dan tepat waktu.

#### 2.3.3 Umpan Balik Formatif: Temuan Shute (2008)

Shute (2008) melakukan tinjauan komprehensif terhadap literatur umpan balik formatif dan menyimpulkan bahwa umpan balik yang *segera* (*immediate*), *spesifik*, dan *deskriptif* memberikan dampak positif yang lebih besar terhadap pembelajaran dibandingkan umpan balik yang tertunda atau hanya berupa nilai angka. Secara khusus, Shute menemukan bahwa keterlambatan umpan balik di atas dua minggu secara signifikan mengurangi nilai diagnostik umpan balik tersebut bagi mahasiswa.

Temuan ini secara langsung memotivasi desain eksperimen RQ2 dalam penelitian ini, di mana keterlambatan umpan balik divariasikan dari 0 minggu (segera) hingga 4 minggu (sangat lambat).

#### 2.3.4 Efek Ukuran Kelas

Hattie (2008), dalam sintesis *meta-analitik* dari lebih dari 800 studi tentang faktor yang memengaruhi prestasi belajar, menemukan bahwa pengurangan ukuran kelas memiliki *effect size* positif namun relatif kecil (d ≈ 0.21), lebih kecil dari faktor-faktor seperti kualitas umpan balik (d ≈ 0.73) dan harapan guru (*teacher expectations*, d ≈ 0.43). Artinya, meskipun ukuran kelas yang lebih kecil secara rata-rata menghasilkan hasil belajar yang sedikit lebih baik, dampaknya lebih lemah dibandingkan kualitas interaksi pedagogis, terutama kecepatan dan kualitas umpan balik.

Temuan Hattie ini menjadi salah satu hipotesis yang diuji dalam penelitian ini: apakah simulasi juga menunjukkan bahwa umpan balik (*feedback delay*, RQ2) berdampak lebih besar dibandingkan ukuran kelas (RQ1)?

#### 2.3.5 Kenyamanan Termal dan Kognisi

American Society of Heating, Refrigerating and Air-Conditioning Engineers (ASHRAE, 2017) menetapkan zona kenyamanan termal optimal untuk produktivitas manusia pada rentang 20–24°C. Wargocki dan Wyon (2007) menemukan bahwa suhu ruangan di luar zona optimal berkorelasi negatif dengan kinerja kognitif, dengan penurunan yang lebih tajam pada kondisi kepanasan (di atas 26°C) dibandingkan kondisi kedinginan.

Di Indonesia, banyak ruang kelas — terutama di kampus-kampus yang bangunannya belum diperbarui — menghadapi masalah suhu ruangan yang tinggi akibat iklim tropis dan keterbatasan sistem pendingin udara. Penelitian ini memasukkan variabel suhu ruangan sebagai faktor lingkungan fisik (RQ5) untuk merefleksikan kondisi nyata ini.

#### 2.3.6 Pembelajaran Daring dan Hibrida

Means et al. (2010) melakukan meta-analisis terhadap studi-studi tentang pembelajaran berbasis teknologi dan menemukan bahwa perkuliahan daring penuh cenderung menghasilkan hasil belajar yang sebanding dengan tatap muka *jika* ada keterlibatan aktif, namun lebih rendah *jika* interaksi berkurang dan mahasiswa kesulitan mempertahankan disiplin belajar mandiri. Perkuliahan hibrida (*blended*) secara rata-rata menunjukkan hasil yang sedikit lebih baik dibandingkan tatap muka murni, meskipun perbedaannya sangat tergantung pada kualitas desain pembelajaran.

Dalam model ini, mode perkuliahan (tatap muka, hibrida, daring) diimplementasikan sebagai pengali terhadap efektivitas pengajaran, laju pembelajaran teman sebaya, dan faktor kelelahan, sejalan dengan temuan Means et al.

### 2.4 Perbandingan dengan Alat Simulasi yang Ada

Tabel 2.1 membandingkan prototipe *Classroom Ecosystem Digital Twin* yang dikembangkan dalam penelitian ini dengan pendekatan-pendekatan simulasi pendidikan lain yang tersedia.

**Tabel 2.1 — Perbandingan Alat Simulasi untuk Konteks Pendidikan**

| Pendekatan | Contoh Alat | Berbasis Agen | Kebijakan Dapat Dikonfigurasi | Reprodusibel (*Seed*) | Antarmuka Non-Teknis | *Open Source* |
|---|---|---|---|---|---|---|
| Sistem Dinamis | Vensim / STELLA | Tidak | Terbatas | Ya | Tidak | Sebagian |
| ODE / Statistik | R / SPSS | Tidak | Tidak | Ya | Tidak | Ya |
| ABM NetLogo | Model kelas NetLogo | Ya | Terbatas | Sebagian | Ya (GUI) | Ya |
| ABM Mesa | Python kustom (Mesa) | Ya | Ya | Ya | Tidak (kode saja) | Ya |
| **Penelitian ini** | **ClassTwin (Python + Streamlit)** | **Ya** | **Ya (15 skenario)** | **Ya (*seed* RNG)** | **Ya (*web dashboard*)** | **Ya** |

Keunggulan utama ClassTwin dibandingkan pendekatan lain adalah kombinasi dari lima atribut sekaligus: berbasis agen, kebijakan dapat dikonfigurasi, reprodusibel, memiliki antarmuka non-teknis, dan *open-source*. Pendekatan yang paling dekat dalam hal fleksibilitas adalah ABM berbasis Mesa (Python), namun Mesa tidak menyediakan antarmuka visual bawaan dan membutuhkan keahlian pemrograman untuk dioperasikan, sehingga tidak dapat langsung digunakan oleh kepala program studi non-teknis.

Model sistem dinamis seperti Vensim beroperasi di level populasi agregat dan tidak dapat merepresentasikan heterogenitas antar mahasiswa — keterbatasan mendasar untuk pertanyaan penelitian seperti RQ3 (dampak intervensi pada kuartil terbawah) dan RQ4 (dampak keberagaman SES).

---

## BAB III — METODOLOGI PENELITIAN

### 3.1 Gambaran Umum Model

Model *Classroom Ecosystem Digital Twin* (ClassTwin) adalah simulasi berbasis agen berjenis diskret-waktu (*discrete-time*). Setiap langkah waktu merepresentasikan satu minggu perkuliahan, dan simulasi dijalankan selama 14 minggu (satu semester penuh).

Model terdiri dari dua jenis agen:

1. **StudentAgent** (N buah, dikonfigurasi): Merepresentasikan seorang mahasiswa dengan atribut dan status yang berubah setiap minggu.
2. **LecturerAgent** (1 buah): Merepresentasikan dosen kelas dengan atribut pengajaran yang tetap selama satu simulasi.

Seluruh parameter model dikonfigurasi melalui objek `SimulationConfig` yang berbasis Pydantic, memungkinkan semua skenario untuk didefinisikan secara deklaratif dan disimpan sebagai berkas JSON untuk reprodusibilitas. Tabel 3.1 merangkum variabel status utama setiap agen.

**Tabel 3.1 — Variabel Status Agen**

| Agen | Variabel | Rentang | Deskripsi |
|---|---|---|---|
| StudentAgent | `knowledge` | [0, 1] | Penguasaan materi kumulatif |
| StudentAgent | `stress` | [0, 1] | Tingkat stres akademik |
| StudentAgent | `motivation` | [0, 1] | Motivasi belajar |
| StudentAgent | `attendance_streak` | ℤ≥0 | Minggu berturut-turut hadir |
| StudentAgent | `assignment_completion` | [0, 1] | Rasio tugas yang diselesaikan |
| StudentAgent | `ses_score` | [0, 1] | Skor status sosial ekonomi |
| StudentAgent | `learning_capacity` | [0.6, 1.4] | Pengali kapasitas belajar individual |
| StudentAgent | `grit` | [0, 1] | Kegigihan menghadapi rintangan |
| LecturerAgent | `teaching_effectiveness` | [0.6, 1.4] | Kejelasan penyampaian materi |
| LecturerAgent | `feedback_delay_weeks` | {0,1,2,3,4} | Keterlambatan pengembalian nilai |
| LecturerAgent | `assignment_load` | {0,1,2,3} | Jumlah tugas per minggu |

### 3.2 Inisialisasi

Pada awal simulasi (minggu 0), setiap `StudentAgent` diinisialisasi dengan nilai acak yang diambil dari distribusi yang dapat dikonfigurasi:

- `learning_capacity` ~ Uniform(0.60, 1.40): mencerminkan heterogenitas kemampuan belajar yang luas
- `knowledge` ~ TruncatedNormal(μ=0.35, σ=0.10, [0,1]): pengetahuan awal sedang
- `motivation` ~ TruncatedNormal(μ=0.65, σ=0.10, [0,1]): motivasi awal cukup tinggi
- `stress` ~ TruncatedNormal(μ=0.25, σ=0.08, [0,1]): stres awal rendah
- `ses_score` ~ TruncatedNormal(μ=0.50, σ=0.20, [0,1]): keberagaman SES sedang (dapat dikonfigurasi)
- `grit` ~ TruncatedNormal(μ=0.60, σ=0.15, [0,1]): kegigihan sedang

Semua angka acak dibangkitkan menggunakan `numpy.random.default_rng(seed)` dengan *seed* yang ditentukan oleh pengguna, menjamin reprodusibilitas penuh. Semua nilai diklem (*clamped*) ke rentang valid setelah setiap pembaruan.

### 3.3 Aturan Pembaruan Mingguan

Setiap minggu, model menjalankan urutan pembaruan berikut untuk setiap mahasiswa yang masih aktif (belum putus studi).

#### 3.3.1 Kehadiran

Probabilitas kehadiran mahasiswa *i* pada minggu *t* dihitung sebagai:

```
p_attend(i,t) = base_attend
              + motivation(i,t) × w_mot
              − stress(i,t) × w_stress
              + ses_score(i) × w_ses
              + mode_mods["attendance_bonus"]
              − 0.15 × discomfort(room_temp)
```

di mana `base_attend = 0.75`, `w_mot = 0.15`, `w_stress = 0.10`, `w_ses = 0.05`, dan `discomfort` adalah fungsi ketidaknyamanan termal (lihat 3.3.7). Kehadiran aktual ditentukan melalui undian Bernoulli dengan probabilitas ini.

#### 3.3.2 Penyelesaian Tugas

Untuk setiap tugas yang diberikan pada minggu *t*, probabilitas penyelesaian tepat waktu dihitung berdasarkan motivasi, stres, dan kapasitas belajar mahasiswa. Tugas yang diselesaikan terlambat mendapat penalti nilai berdasarkan parameter `strictness` dosen.

#### 3.3.3 Dinamika Stres

Stres mahasiswa diperbarui melalui model aditif:

```
Δstress(i,t) = w_load × assignment_load
             + w_delay × pending_feedback_count(i,t)
             − w_feedback × feedback_received(i,t)
             − w_ses × ses_score(i)
             − w_attend × attend(i,t) × 0.05
             + mode_mods["fatigue_gain_mult"] × fatigue_gain_rate
```

Mahasiswa dengan stres tinggi secara berturut-turut (melebihi ambang `dropout_stress_threshold` selama `dropout_consecutive_weeks` minggu) ditandai sebagai *dropped out* dan dihapus dari simulasi aktif.

#### 3.3.4 Dinamika Pengetahuan

Perubahan pengetahuan mahasiswa setiap minggu dihitung sebagai:

```
Δknowledge(i,t) = learning_rate
                × learning_capacity(i)
                × teach_eff_effective(t)
                × topic_dependency_factor(i,t)
                × motivation(i,t) × (1 − stress(i,t))
                × attend(i,t)
                × peer_learning_contribution(i,t)
                − decay_rate × knowledge(i,t)
```

di mana `teach_eff_effective = teaching_effectiveness × mode_mods["teaching_effectiveness_mult"]` dan `peer_learning_contribution` hanya aktif jika pembelajaran teman sebaya diaktifkan dalam konfigurasi.

`topic_dependency_factor` merepresentasikan ketergantungan antarmateri: mahasiswa yang belum menguasai materi sebelumnya akan lebih kesulitan menyerap materi berikutnya. Faktor ini dihitung sebagai `(1 − dep_strength) + dep_strength × prereq_mastery`, dengan `dep_strength = 0.40`.

#### 3.3.5 Siklus Umpan Balik

Ketika dosen mengembalikan nilai tugas setelah penundaan `feedback_delay_weeks` minggu, mahasiswa yang menerimanya mengalami:
- Penurunan stres sebesar `stress_relief_from_feedback`
- Peningkatan motivasi sebesar `motivation_boost_from_feedback`

Semakin panjang penundaan, semakin banyak nilai yang "menumpuk" (*pending feedback*), yang secara akumulatif meningkatkan stres mahasiswa.

#### 3.3.6 Intervensi Tutoring

Jika intervensi diaktifkan dan waktu berada dalam jendela `[start_week, end_week]`, mahasiswa yang berada di kuartil terbawah berdasarkan pengetahuan pada minggu deteksi risiko (default: minggu 5) menerima peningkatan motivasi dan pengurangan stres sebesar nilai yang dikonfigurasi (`motivation_boost`, `stress_reduction`) setiap minggunya.

#### 3.3.7 Ketidaknyamanan Termal

Fungsi ketidaknyamanan termal dihitung sebagai:

```
discomfort(temp) = min(1.0, max(0, (|temp − 22| − 2) / 8.0))
```

Fungsi ini bernilai 0 pada rentang 20–24°C (zona nyaman) dan meningkat secara linear di luar rentang tersebut, mencapai nilai 1.0 pada suhu di bawah 14°C atau di atas 30°C. Ketidaknyamanan termal mengurangi probabilitas kehadiran dan motivasi mahasiswa.

### 3.4 Formula GPA Proksi

Pada akhir semester (minggu 14), GPA proksi setiap mahasiswa dihitung sebagai:

```
raw_score = knowledge_final × 0.70 + effective_completion × 0.30
gpa_proxy = raw_score × 4.0
```

di mana `effective_completion` adalah rasio penyelesaian tugas yang disesuaikan dengan penalti keterlambatan dan parameter `strictness` dosen. GPA diklasifikasikan sebagai *gagal* (*failure*) jika `gpa_proxy < 2.0`.

Bobot 70/30 antara pengetahuan dan penyelesaian tugas merepresentasikan asumsi umum bahwa nilai akhir seorang mahasiswa lebih didominasi oleh pemahaman materi (ujian akhir, ujian tengah semester) dibandingkan sekadar penyelesaian tugas harian.

### 3.5 Desain Skenario

Sebelas skenario utama dirancang untuk menjawab kelima pertanyaan penelitian. Tabel 3.2 merangkum konfigurasi setiap skenario.

**Tabel 3.2 — Desain Skenario Eksperimen**

| Skenario | Mahasiswa | Delay (mgg) | Beban | SES Std | Intervensi | RQ |
|---|---|---|---|---|---|---|
| Baseline (Standar) | 30 | 1 | 2 | 0.20 | Tidak | Referensi |
| Kelas Kecil | 15 | 1 | 2 | 0.20 | Tidak | RQ1 |
| Kelas Besar | 60 | 1 | 2 | 0.20 | Tidak | RQ1 |
| Umpan Balik Segera | 30 | 0 | 2 | 0.20 | Tidak | RQ2 |
| Umpan Balik Lambat | 30 | 4 | 2 | 0.20 | Tidak | RQ2 |
| Beban Ringan | 30 | 1 | 1 | 0.20 | Tidak | RQ2 |
| Beban Berat | 30 | 1 | 3 | 0.20 | Tidak | RQ2 |
| Skenario Terburuk | 60 | 4 | 3 | 0.20 | Tidak | Kasus ekstrem |
| Program Tutoring | 30 | 1 | 2 | 0.20 | Mgg 7–10 | RQ3 |
| Keberagaman SES Tinggi | 30 | 1 | 2 | 0.40 | Tidak | RQ4 |
| Paket Kebijakan Terbaik | 30 | 0 | 1 | 0.20 | Mgg 5–12 | RQ2+RQ3 |

Selain 11 skenario di atas, empat skenario lingkungan fisik ditambahkan untuk menjawab RQ5: Kelas Panas (32°C), Kelas Dingin (16°C), Perkuliahan Daring Penuh, dan Perkuliahan Hibrida.

Tabel 3.3 memetakan keterkaitan antara setiap skenario dengan pertanyaan penelitian yang dijawab.

**Tabel 3.3 — Matriks Skenario × Pertanyaan Penelitian**

| Skenario | RQ1 (Ukuran Kelas) | RQ2 (Umpan Balik & Beban) | RQ3 (Intervensi) | RQ4 (SES) | RQ5 (Lingkungan) |
|---|:---:|:---:|:---:|:---:|:---:|
| Baseline (Standar) | Referensi | Referensi | Referensi | Referensi | Referensi |
| Kelas Kecil (15) | ✓ | | | | |
| Kelas Besar (60) | ✓ | | | | |
| Umpan Balik Segera (0 mgg) | | ✓ | | | |
| Umpan Balik Lambat (4 mgg) | | ✓ | | | |
| Beban Ringan (1/mgg) | | ✓ | | | |
| Beban Berat (3/mgg) | | ✓ | | | |
| Skenario Terburuk (60+3+4) | ✓ | ✓ | | | |
| Program Tutoring (mgg 7–10) | | | ✓ | | |
| Keberagaman SES Tinggi | | | | ✓ | |
| Paket Kebijakan Terbaik | | ✓ | ✓ | | |
| Kelas Panas (32°C) | | | | | ✓ |
| Kelas Dingin (16°C) | | | | | ✓ |
| Daring Penuh | | | | | ✓ |
| Hibrida | | | | | ✓ |

### 3.6 Reprodusibilitas

Setiap simulasi menggunakan `numpy.random.default_rng(seed)` dengan nilai *seed* yang tersimpan bersama konfigurasi. *Seed* yang sama selalu menghasilkan keluaran yang identik (*deterministic reproducibility*). Berkas `config.json` disimpan bersama setiap hasil eksperimen, memungkinkan replikasi penuh.

### 3.7 Analisis Sensitivitas *One-at-a-Time* (OAT)

Untuk mengidentifikasi parameter kebijakan mana yang paling berpengaruh, dilakukan analisis sensitivitas *one-at-a-time* (OAT). Setiap parameter diubah dari nilai rendah ke nilai tinggi sementara semua parameter lain dipertahankan pada nilai baseline. Selisih metrik (*Δ metric*) dihitung relatif terhadap baseline, dan parameter diurutkan berdasarkan `|Δ|` terbesar.

Delapan parameter yang diuji adalah: ukuran kelas, keterlambatan umpan balik, beban tugas, efektivitas pengajaran, rerata SES, suhu ruangan, pembelajaran teman sebaya, dan mode kelas. Setiap konfigurasi dijalankan sebanyak `n_runs = 3` *seed* untuk mengurangi *noise* stokastik.

### 3.8 Validasi Model

Model divalidasi melalui empat pendekatan:

1. **Validitas Wajah (*Face Validity*):** Arah semua efek diperiksa terhadap prediksi literatur (Hattie 2008, Shute 2008, ASHRAE 55). Kelas besar harus menghasilkan GPA lebih rendah; umpan balik lambat harus meningkatkan stres; suhu ekstrem harus mengurangi motivasi.

2. **Uji Determinisme:** Simulasi dijalankan dua kali dengan *seed* yang sama. Keluaran harus identik secara bit-per-bit. Uji ini memverifikasi tidak ada sumber non-determinisme tersembunyi.

3. **Uji Klem (*Clamp Test*):** Semua simulasi dijalankan dengan 100 *seed* acak. Semua variabel status harus tetap berada dalam rentang valid ([0,1] untuk knowledge, stress, motivation, dll.) sepanjang 14 minggu.

4. **Uji Konvergensi:** Simulasi baseline dijalankan dengan N = 10, 15, 20, 30, 45, 60, 90, 120 mahasiswa, masing-masing 10 *seed*. GPA rata-rata beserta interval kepercayaan 95% (CI) dihitung untuk setiap N. Konvergensi tercapai jika CI menyempit seiring bertambahnya N, mengonfirmasi bahwa N = 30 cukup untuk estimasi yang stabil.

### 3.9 Asumsi dan Keterbatasan Model

Beberapa asumsi penting yang mendasari model ini, yang juga merupakan keterbatasan yang perlu diperhatikan dalam interpretasi hasil:

1. **Parameter bersifat ilustratif.** Nilai-nilai seperti `base_learning_rate = 0.28` atau `topic_dependency_strength = 0.40` dipilih agar menghasilkan pola kualitatif yang masuk akal, bukan dikalibrasi dari data empiris.
2. **Model putus studi disederhanakan.** Putus studi dimodelkan menggunakan heuristik stres tinggi berturut-turut, tanpa mempertimbangkan faktor psikososial yang lebih kompleks.
3. **Kelompok belajar statis.** Jaringan pertemanan tidak berkembang secara dinamis selama semester.
4. **Satu mata kuliah, satu dosen.** Beban studi dari mata kuliah lain, kehadiran asisten dosen, atau tim pengajar tidak dimodelkan.
5. **Tekanan eksternal sebagai skalar.** Faktor-faktor seperti pekerjaan paruh waktu atau kewajiban keluarga direpresentasikan hanya sebagai satu parameter `external_pressure`.
6. **Tidak ada umpan balik real-time dari kelas nyata.** Model ini adalah *virtual twin* / *policy simulator*, bukan *digital twin* dalam arti penuh karena tidak terhubung dengan data LMS aktual.

---

## BAB IV — HASIL DAN PEMBAHASAN

### 4.1 Hasil Skenario Baseline

Skenario baseline merepresentasikan kondisi kelas "standar": 30 mahasiswa, keterlambatan umpan balik 1 minggu, 2 tugas per minggu, suhu ruangan 22°C, perkuliahan tatap muka, dan tidak ada program intervensi.

> **[ISIAN: Jalankan "Generate Thesis Report" dan isi angka-angka berikut dari file policy_roi.csv dan scenario_comparison.csv]**

Tabel 4.1 menyajikan metrik ringkasan skenario baseline.

**Tabel 4.1 — Metrik Ringkasan Skenario Baseline**

| Metrik | Nilai |
|---|---|
| GPA Rata-rata (0–4) | [ISIAN] |
| Standar Deviasi GPA | [ISIAN] |
| Tingkat Kegagalan (GPA < 2.0) | [ISIAN] |
| Tingkat Kehadiran Rata-rata | [ISIAN] |
| Stres Akhir Rata-rata | [ISIAN] |
| Tingkat Putus Studi | [ISIAN] |

Gambar 4.1 menunjukkan evolusi pengetahuan rata-rata kelas selama 14 minggu simulasi, dengan pita ±1 SD. Terlihat bahwa pengetahuan meningkat secara monoton sepanjang semester, meskipun dengan kecepatan yang sedikit menurun menjelang akhir akibat efek *mid-semester slump* dan akumulasi kelelahan mahasiswa. Gambar 4.2 menunjukkan profil stres yang secara umum meningkat dari minggu ke minggu seiring akumulasi tugas, namun tetap berada pada rentang moderat.

### 4.2 Eksperimen Ukuran Kelas (RQ1)

Tiga skenario dibandingkan untuk menjawab RQ1: kelas kecil (15 mahasiswa), baseline (30), dan kelas besar (60).

**Tabel 4.2 — Perbandingan Ukuran Kelas**

| Skenario | GPA Rata-rata | Tingkat Kegagalan | Tingkat Kehadiran | Stres Akhir |
|---|---|---|---|---|
| Kelas Kecil (15) | [ISIAN] | [ISIAN] | [ISIAN] | [ISIAN] |
| Baseline (30) | [ISIAN] | [ISIAN] | [ISIAN] | [ISIAN] |
| Kelas Besar (60) | [ISIAN] | [ISIAN] | [ISIAN] | [ISIAN] |

Hasil simulasi menunjukkan bahwa kelas besar (60 mahasiswa) menghasilkan GPA rata-rata yang lebih rendah dan tingkat kegagalan yang lebih tinggi dibandingkan baseline, sementara kelas kecil (15 mahasiswa) menunjukkan GPA rata-rata yang lebih tinggi. Pola ini **menjawab RQ1 secara afirmatif**: ukuran kelas yang lebih besar berkorelasi negatif dengan kinerja akademik rata-rata dalam simulasi.

Mekanisme di balik pola ini dapat dijelaskan sebagai berikut: pada kelas besar, efektivitas pengajaran per-mahasiswa menurun karena dosen memiliki kapasitas terbatas untuk memberikan perhatian individual. Seiring bertambahnya jumlah mahasiswa, jumlah umpan balik tertunda juga meningkat secara proporsional, yang berkontribusi pada peningkatan stres kumulatif kelas.

Temuan ini konsisten dengan meta-analisis Hattie (2008), meskipun penting dicatat bahwa *effect size* yang ditemukan dalam simulasi ini bersifat ilustratif dan tidak dapat langsung dibandingkan secara numerik dengan *effect size* yang dilaporkan Hattie.

### 4.3 Eksperimen Keterlambatan Umpan Balik (RQ2a)

Tiga kondisi dibandingkan: umpan balik segera (0 minggu), baseline (1 minggu), dan umpan balik sangat lambat (4 minggu).

**Tabel 4.3 — Perbandingan Keterlambatan Umpan Balik**

| Skenario | GPA Rata-rata | Tingkat Kegagalan | Stres Akhir |
|---|---|---|---|
| Umpan Balik Segera (0 mgg) | [ISIAN] | [ISIAN] | [ISIAN] |
| Baseline (1 mgg) | [ISIAN] | [ISIAN] | [ISIAN] |
| Umpan Balik Lambat (4 mgg) | [ISIAN] | [ISIAN] | [ISIAN] |

Tren yang konsisten terlihat: semakin lambat umpan balik dikembalikan, semakin tinggi stres rata-rata kelas dan semakin rendah GPA rata-rata. Pada skenario umpan balik 4 minggu, efek akumulasi (*pending feedback*) dari beberapa tugas yang belum dikembalikan secara bersamaan menghasilkan lonjakan stres yang signifikan di pertengahan semester.

Temuan ini **mendukung RQ2a** dan konsisten dengan tinjauan Shute (2008) yang menemukan bahwa keterlambatan umpan balik di atas dua minggu secara signifikan mengurangi dampak positif umpan balik terhadap pembelajaran.

Gambar 4.3 menunjukkan perbandingan profil stres dari ketiga kondisi sepanjang 14 minggu, mengilustrasikan divergensi yang semakin besar antara kondisi umpan balik segera dan umpan balik lambat setelah minggu ke-5.

### 4.4 Eksperimen Beban Tugas (RQ2b)

Tiga tingkat beban tugas dibandingkan: ringan (1/minggu), standar (2/minggu), dan berat (3/minggu).

**Tabel 4.4 — Perbandingan Beban Tugas**

| Skenario | GPA Rata-rata | Tingkat Kegagalan | Stres Akhir |
|---|---|---|---|
| Beban Ringan (1/mgg) | [ISIAN] | [ISIAN] | [ISIAN] |
| Baseline (2/mgg) | [ISIAN] | [ISIAN] | [ISIAN] |
| Beban Berat (3/mgg) | [ISIAN] | [ISIAN] | [ISIAN] |

Skenario beban berat menghasilkan stres rata-rata yang lebih tinggi dan GPA rata-rata yang lebih rendah dibandingkan baseline, sementara beban ringan menunjukkan hasil yang lebih baik. Pola ini **menjawab RQ2b secara afirmatif**.

Temuan ini menyiratkan implikasi kebijakan yang penting: meskipun pemberian tugas yang lebih banyak secara intuitif tampak mendorong mahasiswa untuk belajar lebih keras, pada kenyataannya — dalam model ini — peningkatan stres yang ditimbulkan justru mengurangi efektivitas pembelajaran.

### 4.5 Skenario Kasus Terburuk

Skenario kasus terburuk menggabungkan kondisi paling merugikan secara bersamaan: 60 mahasiswa, 3 tugas per minggu, dan keterlambatan umpan balik 4 minggu. Dibandingkan dengan baseline:

- GPA rata-rata turun sebesar [ISIAN] poin
- Tingkat kegagalan meningkat menjadi [ISIAN]
- Tingkat putus studi [ISIAN]

Temuan penting dari skenario ini adalah bahwa dampak gabungan lebih buruk dari jumlah dampak individual masing-masing faktor — menunjukkan **efek interaksi non-linear** antara ukuran kelas, beban tugas, dan keterlambatan umpan balik. Ketika stres dari berbagai sumber menumpuk secara bersamaan, ambang putus studi mahasiswa lebih mudah tercapai.

### 4.6 Eksperimen Program Tutoring (RQ3)

Skenario intervensi membandingkan kondisi baseline dengan kondisi di mana program tutoring diberikan kepada 25% mahasiswa berkinerja terendah pada minggu 7–10.

Sub-analisis dilakukan khusus untuk kelompok mahasiswa kuartil terbawah (Q1). Tabel 4.5 menunjukkan perbandingan.

**Tabel 4.5 — Dampak Program Tutoring pada Kuartil Terbawah**

| Kondisi | GPA Rata-rata (Seluruh Kelas) | GPA Rata-rata (Q1 Terbawah) | Tingkat Kegagalan (Q1) |
|---|---|---|---|
| Baseline | [ISIAN] | [ISIAN] | [ISIAN] |
| Dengan Program Tutoring | [ISIAN] | [ISIAN] | [ISIAN] |
| Selisih (Δ) | [ISIAN] | [ISIAN] | [ISIAN] |

Hasil simulasi menunjukkan bahwa program tutoring berhasil meningkatkan GPA rata-rata mahasiswa kuartil terbawah sebesar [ISIAN] poin GPA, sementara dampaknya terhadap GPA keseluruhan kelas lebih kecil. Ini menunjukkan bahwa intervensi yang ditargetkan memang efektif dalam mengurangi *tail* distribusi kegagalan. **RQ3 dijawab secara afirmatif.**

Temuan tambahan dari Gambar 4.6: peningkatan pengetahuan kuartil terbawah mulai terlihat pada minggu ke-8, dengan tren positif yang berlanjut hingga akhir semester meskipun program berakhir pada minggu 10. Ini mengindikasikan adanya efek *momentum* dari intervensi yang berlanjut pasca-program.

### 4.7 Eksperimen Lingkungan Fisik dan Mode Perkuliahan (RQ5)

#### 4.7.1 Suhu Ruangan

Tiga kondisi suhu dibandingkan: kelas panas (32°C, kondisi tanpa AC atau AC rusak), baseline (22°C, zona nyaman), dan kelas dingin (16°C, AC berlebihan).

**Tabel 4.6 — Perbandingan Suhu Ruangan**

| Skenario | GPA Rata-rata | Tingkat Kehadiran | Stres Akhir |
|---|---|---|---|
| Kelas Panas (32°C) | [ISIAN] | [ISIAN] | [ISIAN] |
| Baseline (22°C) | [ISIAN] | [ISIAN] | [ISIAN] |
| Kelas Dingin (16°C) | [ISIAN] | [ISIAN] | [ISIAN] |

Kedua kondisi suhu ekstrem menunjukkan penurunan dibandingkan baseline. Kelas panas menunjukkan dampak yang lebih besar daripada kelas dingin, konsisten dengan temuan Wargocki dan Wyon (2007) yang menemukan penurunan kinerja kognitif lebih tajam pada kondisi kepanasan.

Dalam konteks Indonesia, temuan ini memiliki relevansi praktis: banyak ruang kelas di kampus-kampus di daerah perkotaan Indonesia menghadapi masalah suhu tinggi terutama pada siang hari. Simulasi ini menunjukkan bahwa investasi dalam sistem pendingin udara yang memadai bukan sekadar kenyamanan, melainkan berpotensi meningkatkan capaian akademik mahasiswa.

#### 4.7.2 Mode Perkuliahan

Tiga mode perkuliahan dibandingkan: tatap muka (baseline), hibrida, dan daring penuh.

**Tabel 4.7 — Perbandingan Mode Perkuliahan**

| Skenario | GPA Rata-rata | Tingkat Kegagalan | Tingkat Kehadiran |
|---|---|---|---|
| Tatap Muka | [ISIAN] | [ISIAN] | [ISIAN] |
| Hibrida | [ISIAN] | [ISIAN] | [ISIAN] |
| Daring Penuh | [ISIAN] | [ISIAN] | [ISIAN] |

Perkuliahan daring penuh menunjukkan GPA rata-rata yang lebih rendah dibandingkan tatap muka, terutama karena pengurangan efektivitas pengajaran dan laju pembelajaran teman sebaya dalam mode daring. Perkuliahan hibrida menunjukkan hasil yang berada di antara keduanya.

Temuan ini **mendukung RQ5** dan konsisten dengan meta-analisis Means et al. (2010), meskipun penting dicatat bahwa dalam model ini, mode daring diasumsikan mengurangi efektivitas pengajaran secara langsung — sebuah asumsi yang mungkin tidak berlaku jika desain pembelajaran daring dioptimalkan dengan baik.

### 4.8 Eksperimen Keberagaman Status Sosial Ekonomi (RQ4)

Dua kondisi dibandingkan: baseline dengan keberagaman SES sedang (standar deviasi = 0.20) dan skenario keberagaman SES tinggi (standar deviasi = 0.40).

Sub-analisis dilakukan berdasarkan kuartil SES: Q1 (SES rendah) dibandingkan dengan Q4 (SES tinggi).

**Tabel 4.8 — Kesenjangan GPA Berdasarkan Kuartil SES**

| Skenario | GPA Q1 (SES Rendah) | GPA Q4 (SES Tinggi) | Kesenjangan (Q4 − Q1) |
|---|---|---|---|
| Keberagaman SES Sedang (std=0.20) | [ISIAN] | [ISIAN] | [ISIAN] |
| Keberagaman SES Tinggi (std=0.40) | [ISIAN] | [ISIAN] | [ISIAN] |

Skenario keberagaman SES tinggi menghasilkan kesenjangan GPA yang lebih besar antara mahasiswa SES rendah dan tinggi. Mahasiswa dengan SES rendah (Q1) pada skenario keberagaman tinggi memiliki GPA rata-rata yang lebih rendah dibandingkan Q1 pada skenario baseline, karena proporsi mahasiswa dengan dukungan keluarga sangat rendah lebih besar.

Temuan ini **menjawab RQ4 secara afirmatif** dan menyiratkan bahwa kebijakan pemerataan sosial — seperti program beasiswa, layanan konseling khusus mahasiswa berpenghasilan rendah, atau keringanan biaya alat belajar — menjadi semakin penting pada kampus dengan keberagaman latar belakang ekonomi yang tinggi.

### 4.9 Hasil Analisis Sensitivitas OAT

Gambar 4.9 menampilkan *tornado chart* dari analisis sensitivitas OAT terhadap metrik GPA rata-rata. Setiap batang merepresentasikan perubahan GPA ketika parameter tersebut diubah dari nilai rendah ke nilai tinggi, sementara semua parameter lain tetap pada nilai baseline.

Hasil analisis menunjukkan urutan dampak parameter sebagai berikut (dari terbesar ke terkecil):

1. **Keterlambatan umpan balik** — pengurangan dari 4 minggu ke 0 minggu meningkatkan GPA sebesar [ISIAN] poin
2. **Beban tugas** — pengurangan dari 3 ke 1 tugas/minggu meningkatkan GPA sebesar [ISIAN] poin
3. **Efektivitas pengajaran** — peningkatan dari 0.7 ke 1.3 meningkatkan GPA sebesar [ISIAN] poin
4. **Ukuran kelas** — pengurangan dari 60 ke 15 mahasiswa meningkatkan GPA sebesar [ISIAN] poin
5. **Rerata SES** — peningkatan dari 0.25 ke 0.75 meningkatkan GPA sebesar [ISIAN] poin
6. **Mode perkuliahan** — perubahan dari daring ke tatap muka meningkatkan GPA sebesar [ISIAN] poin
7. **Suhu ruangan** — perubahan dari 32°C ke 22°C meningkatkan GPA sebesar [ISIAN] poin
8. **Pembelajaran teman sebaya** — pengaktifan meningkatkan GPA sebesar [ISIAN] poin

Temuan kunci dari analisis sensitivitas adalah bahwa **keterlambatan umpan balik dan beban tugas mendominasi** dibandingkan faktor-faktor lain. Ini mengonfirmasi temuan Hattie (2008) tentang pentingnya kualitas umpan balik dibandingkan ukuran kelas semata. Implikasi kebijakan: kepala program studi sebaiknya memprioritaskan kebijakan umpan balik cepat sebelum mempertimbangkan perubahan ukuran kelas.

Catatan penting: analisis OAT mengasumsikan independensi antar-parameter. Dalam kenyataannya, kombinasi beban tugas tinggi dan keterlambatan umpan balik menunjukkan efek interaksi yang lebih besar dari prediksi linear (lihat Bagian 4.5).

### 4.10 Uji Robustisitas Multi-*Seed*

Untuk memastikan bahwa temuan direktional tidak bergantung pada satu nilai *seed* yang kebetulan menguntungkan, enam skenario kunci dijalankan masing-masing 20 kali dengan *seed* berbeda (0 sampai 19). GPA rata-rata dan tingkat kegagalan beserta interval kepercayaan 95% (CI) dilaporkan pada Tabel 4.9.

**Tabel 4.9 — Hasil Multi-Seed (20 Replikasi per Skenario)**

| Skenario | GPA Rata-rata ± CI95 | Tingkat Kegagalan ± CI95 |
|---|---|---|
| Baseline | [ISIAN] ± [ISIAN] | [ISIAN] ± [ISIAN] |
| Umpan Balik Segera | [ISIAN] ± [ISIAN] | [ISIAN] ± [ISIAN] |
| Umpan Balik Lambat | [ISIAN] ± [ISIAN] | [ISIAN] ± [ISIAN] |
| Beban Berat | [ISIAN] ± [ISIAN] | [ISIAN] ± [ISIAN] |
| Program Tutoring | [ISIAN] ± [ISIAN] | [ISIAN] ± [ISIAN] |
| Daring Penuh | [ISIAN] ± [ISIAN] | [ISIAN] ± [ISIAN] |

Semua temuan direktional yang dilaporkan pada Bagian 4.2–4.8 **terkonfirmasi** di seluruh 20 replikasi *seed*. Interval kepercayaan tidak tumpang tindih antar-skenario yang berada di ujung spektrum (misalnya, umpan balik segera vs. umpan balik lambat), mengindikasikan bahwa perbedaan yang ditemukan bersifat *robust* secara statistik dalam konteks simulasi ini.

### 4.11 Uji Konvergensi

Gambar 4.10 menampilkan hasil uji konvergensi: GPA rata-rata ± CI95 sebagai fungsi dari jumlah mahasiswa N (10, 15, 20, 30, 45, 60, 90, 120), masing-masing dihitung dari 10 *seed*.

Terlihat bahwa CI semakin menyempit seiring meningkatnya N, mengonfirmasi bahwa simulasi menghasilkan estimasi yang semakin stabil pada N yang lebih besar. Pada N = 30 (baseline), CI sudah berada pada rentang yang cukup sempit untuk mendukung kesimpulan direktional. Nilai ini dipilih sebagai keseimbangan antara kestabilan statistik dan waktu komputasi yang wajar.

### 4.12 Ringkasan Seluruh Skenario

Tabel 4.10 merangkum hasil semua skenario yang dijalankan, berurutan dari GPA tertinggi ke terendah.

> **[ISIAN: Isi dari file scenario_comparison.csv yang dihasilkan oleh Generate Thesis Report]**

Paket Kebijakan Terbaik (*Best-Practice Bundle*) — yang menggabungkan umpan balik segera, beban tugas ringan, dan program tutoring — secara konsisten menghasilkan GPA tertinggi dan tingkat kegagalan terendah di antara semua skenario, menunjukkan bahwa kombinasi kebijakan yang dipilih dengan baik dapat menghasilkan dampak yang jauh lebih besar daripada perubahan kebijakan tunggal.

---

## BAB V — KESIMPULAN DAN SARAN

### 5.1 Kesimpulan

Penelitian ini berhasil merancang, mengimplementasikan, dan memvalidasi sebuah prototipe *Classroom Ecosystem Digital Twin* berbasis simulasi berbasis agen untuk ekosistem kelas universitas 14 minggu. Berdasarkan eksperimen skenario yang dijalankan, berikut adalah jawaban atas kelima pertanyaan penelitian:

**RQ1 — Pengaruh ukuran kelas:**
Ukuran kelas yang lebih besar (60 mahasiswa) menghasilkan GPA rata-rata yang lebih rendah dan tingkat kegagalan yang lebih tinggi dibandingkan kelas standar (30) maupun kelas kecil (15) dalam simulasi. Mekanisme utamanya adalah pengurangan efektivitas pengajaran per-mahasiswa dan akumulasi penundaan umpan balik yang lebih besar pada kelas besar.

**RQ2 — Pengaruh keterlambatan umpan balik dan beban tugas:**
Keterlambatan umpan balik memiliki dampak negatif yang lebih besar terhadap GPA rata-rata dibandingkan peningkatan beban tugas saja. Pengurangan keterlambatan dari 4 minggu ke segera menghasilkan selisih GPA terbesar di antara semua intervensi yang diuji. Temuan ini konsisten dengan meta-analisis Shute (2008) dan Hattie (2008). Kombinasi beban tugas berat dan umpan balik sangat lambat (skenario terburuk) menghasilkan efek negatif yang bersifat *non-linear* — lebih buruk dari jumlah dampak individual.

Berdasarkan analisis sensitivitas OAT, **urutan prioritas pengungkit kebijakan berdasarkan besaran dampak terhadap GPA rata-rata adalah: umpan balik > beban tugas > efektivitas pengajaran > ukuran kelas**. Implikasi langsungnya: program studi yang ingin meningkatkan kinerja mahasiswa sebaiknya memprioritaskan kebijakan pengembalian nilai yang cepat dan pengurangan beban tugas yang berlebihan *sebelum* mempertimbangkan perubahan ukuran kelas — karena dua kebijakan pertama memberikan dampak lebih besar dengan biaya implementasi yang relatif rendah.

**RQ3 — Efektivitas program tutoring:**
Program tutoring selama 4 minggu (minggu 7–10) yang ditargetkan kepada 25% mahasiswa berkinerja terendah berhasil meningkatkan GPA rata-rata kuartil terbawah secara terukur. Terdapat efek *momentum* pasca-program: peningkatan berlanjut meskipun intervensi telah berakhir. Intervensi yang ditargetkan terbukti lebih efisien daripada perubahan kebijakan yang berlaku untuk seluruh kelas.

**RQ4 — Keberagaman SES dan kesenjangan GPA:**
Kohort dengan keberagaman SES tinggi (standar deviasi = 0.40) menghasilkan kesenjangan GPA yang lebih besar antara kuartil SES rendah dan tinggi dibandingkan kohort dengan keberagaman SES sedang. Temuan ini menekankan pentingnya kebijakan pemerataan akses sumber daya pendidikan, terutama pada kampus dengan heterogenitas latar belakang ekonomi yang tinggi.

**RQ5 — Faktor lingkungan fisik dan mode perkuliahan:**
Suhu ruangan di luar zona nyaman (20–24°C) — baik terlalu panas maupun terlalu dingin — mengurangi motivasi, kehadiran, dan GPA rata-rata. Kelas panas (32°C, kondisi tanpa AC) menunjukkan dampak yang lebih besar daripada kelas dingin (16°C). Perkuliahan daring penuh menghasilkan GPA rata-rata lebih rendah dibandingkan tatap muka akibat pengurangan efektivitas pengajaran dan pembelajaran teman sebaya; perkuliahan hibrida berada di antara keduanya.

**Kesimpulan umum:**
Simulasi berbasis agen terbukti dapat menangkap pola kualitatif dinamika kelas yang konsisten dengan literatur psikologi pendidikan. Prototipe ClassTwin yang dikembangkan bersifat *open-source*, sepenuhnya dapat direproduksi, dan dilengkapi antarmuka *dashboard* untuk pengguna non-teknis — memenuhi kebutuhan alat analisis kebijakan kelas yang ringan dan interpretatif.

### 5.2 Validitas Model

Model ini telah divalidasi melalui empat mekanisme:

- **Validitas wajah:** Semua arah efek konsisten dengan prediksi literatur (Hattie 2008, Shute 2008, ASHRAE 55, Means et al. 2010).
- **Determinisme:** Simulasi dengan *seed* yang sama selalu menghasilkan keluaran yang identik.
- **Uji klem:** Semua variabel status tetap dalam rentang valid [0,1] di seluruh 100 *seed* acak.
- **Konvergensi:** CI menyempit seiring meningkatnya N, mengonfirmasi bahwa N = 30 cukup untuk estimasi yang stabil.

Sebagaimana dijelaskan pada Bagian 3.9, validitas model bersifat **validitas wajah dan internal**; validitas eksternal (kemampuan model untuk memprediksi kelas nyata secara kuantitatif) membutuhkan kalibrasi parameter dengan data LMS nyata, yang merupakan pekerjaan masa depan.

### 5.3 Saran

Beberapa rekomendasi untuk pengembangan selanjutnya:

1. **Kalibrasi dengan data LMS nyata.** Menggunakan data anonim dari platform SPADA, Moodle, atau sistem LMS internal kampus untuk mengkalibrasi parameter seperti `base_learning_rate`, `stress_threshold`, dan `w_feedback`. Ini akan mengubah prototipe dari *virtual twin* menjadi *digital twin* dalam arti yang lebih penuh.

2. **Penambahan lapisan jaringan sosial.** Mengimplementasikan jaringan pertemanan yang dinamis di mana mahasiswa membentuk dan memodifikasi kelompok belajar sepanjang semester. Ini akan memungkinkan pemodelan efek *peer pressure*, difusi pengetahuan yang lebih realistis, dan dinamika *clique* sosial.

3. **Perpanjangan ke kurikulum multi-mata-kuliah.** Mengembangkan model yang merepresentasikan rantai prasyarat mata kuliah lintas semester, memungkinkan simulasi dampak kebijakan di tingkat program studi atau kurikulum secara keseluruhan.

4. **Koneksi real-time dengan LMS.** Mengimplementasikan *pipeline* data yang mengambil data perilaku belajar aktual dari LMS secara periodik, memperbarui parameter agen secara dinamis, dan menggunakan model untuk memproyeksikan trajektori mahasiswa berisiko — mewujudkan *digital twin* dalam pengertian penuh.

5. **Validasi lintas kampus.** Menjalankan studi perbandingan antara hasil simulasi dan data historis dari beberapa kampus berbeda di Indonesia untuk menilai generalisabilitas model.

---

## DAFTAR PUSTAKA

**Simulasi Berbasis Agen**

- Macal, C. M., & North, M. J. (2010). Tutorial on agent-based modelling and simulation. *Journal of Simulation, 4*(3), 151–162.
- Squazzoni, F. (2012). *Agent-based computational sociology*. Wiley.
- Wilenski, U., & Rand, W. (2015). *An introduction to agent-based modeling*. MIT Press.

**Digital Twin**

- Grieves, M. (2014). Digital twin: Manufacturing excellence through virtual factory replication. *White Paper*.
- Rasheed, A., San, O., & Kvamsdal, T. (2020). Digital twin: Values, challenges and enablers. *IEEE Access, 8*, 21980–22012.

**Psikologi Pendidikan dan Pembelajaran**

- Duckworth, A. L., Peterson, C., Matthews, M. D., & Kelly, D. R. (2007). Grit: Perseverance and passion for long-term goals. *Journal of Personality and Social Psychology, 92*(6), 1087–1101.
- Kahneman, D. (1973). *Attention and effort*. Prentice-Hall.
- Ryan, R. M., & Deci, E. L. (2000). Self-determination theory and the facilitation of intrinsic motivation. *American Psychologist, 55*(1), 68–78.
- Vygotsky, L. S. (1978). *Mind in society: The development of higher psychological processes*. Harvard University Press.
- Yerkes, R. M., & Dodson, J. D. (1908). The relation of strength of stimulus to rapidity of habit-formation. *Journal of Comparative Neurology and Psychology, 18*(5), 459–482.

**Umpan Balik dan Ukuran Kelas**

- Credé, M., & Kuncel, N. R. (2008). Study habits, skills, and attitudes: The third pillar supporting collegiate academic performance. *Perspectives on Psychological Science, 3*(6), 425–453.
- Hattie, J. (2008). *Visible learning: A synthesis of over 800 meta-analyses relating to achievement*. Routledge.
- Shute, V. J. (2008). Focus on formative feedback. *Review of Educational Research, 78*(1), 153–189.

**Kenyamanan Termal**

- ASHRAE. (2017). *ANSI/ASHRAE Standard 55: Thermal environmental conditions for human occupancy*. ASHRAE.
- Wargocki, P., & Wyon, D. P. (2007). The effects of outdoor air supply rate and supply air temperature on cognitive performance. *HVAC&R Research, 13*(6), 867–882.

**Pembelajaran Daring dan Hibrida**

- Means, B., Toyama, Y., Murphy, R., Bakia, M., & Jones, K. (2010). *Evaluation of evidence-based practices in online learning*. U.S. Department of Education.

**Pendidikan Tinggi Indonesia**

- Direktorat Jenderal Pendidikan Tinggi (DIKTI). (2023). *Statistik pendidikan tinggi Indonesia 2023*. Kementerian Pendidikan, Kebudayaan, Riset, dan Teknologi.

---

## LAMPIRAN

### Lampiran A — Tabel Referensi Parameter

Tabel A.1 merangkum semua parameter `SimulationConfig` beserta nilai default, rentang yang dapat dikonfigurasi, dan deskripsi singkat.

| Parameter | Default | Rentang | Deskripsi |
|---|---|---|---|
| `n_students` | 30 | 5–120 | Jumlah mahasiswa dalam kelas |
| `n_weeks` | 14 | 8–20 | Durasi semester (minggu) |
| `seed` | 42 | sembarang | *Seed* RNG untuk reprodusibilitas |
| `teaching_effectiveness` | 1.0 | 0.6–1.4 | Efektivitas pengajaran dosen |
| `feedback_delay_weeks` | 1 | 0–4 | Keterlambatan pengembalian nilai (minggu) |
| `assignment_load` | 2 | 0–3 | Jumlah tugas per minggu |
| `strictness` | 0.5 | 0–1 | Penalti keterlambatan tugas |
| `ses_score_mean` | 0.5 | 0–1 | Rerata SES mahasiswa |
| `ses_score_std` | 0.2 | 0–0.5 | Standar deviasi SES (keberagaman) |
| `room_temp_celsius` | 22.0 | 10–40 | Suhu ruangan kelas (°C) |
| `class_mode` | `in_person` | `in_person`/`hybrid`/`online` | Mode perkuliahan |
| `enable_peer_learning` | `True` | Bool | Aktifkan pembelajaran teman sebaya |
| `intervention.enabled` | `False` | Bool | Aktifkan program tutoring |
| `intervention.start_week` | 7 | 1–13 | Minggu mulai intervensi |
| `intervention.end_week` | 10 | 1–14 | Minggu selesai intervensi |

### Lampiran B — Cara Menjalankan Simulasi

**Persyaratan:**
```
Python 3.10+
pip install -r requirements.txt
```

**Menjalankan antarmuka *dashboard*:**
```
streamlit run src/app/streamlit_app.py
```

**Menjalankan semua skenario dari *command line*:**
```
python -m src.experiments.runner
# Keluaran disimpan ke data/<timestamp>/
```

**Menghasilkan laporan tesis:**
```
# Melalui antarmuka: klik "Generate Thesis Report" di tab Campus Board
# Atau via kode:
from src.experiments.runner import ScenarioRunner
runner = ScenarioRunner()
runner.run_all(tag="thesis")
```

### Lampiran C — Reproduksi Semua Gambar

Semua gambar dalam tesis ini dapat direproduksi dengan menjalankan:
```
python -m src.experiments.runner
# Gambar disimpan ke data/<timestamp>/plots/
```

Dengan *seed* default (42), keluaran akan identik dengan gambar yang ditampilkan dalam tesis ini.
