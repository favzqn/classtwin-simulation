# PENGEMBANGAN DIGITAL TWIN EKOSISTEM KELAS BERBASIS AGENT-BASED SIMULATION UNTUK ANALISIS FAKTOR YANG MEMPENGARUHI KINERJA MAHASISWA

**Skripsi**

Diajukan sebagai salah satu syarat untuk memperoleh gelar Sarjana Komputer
pada Program Studi Sistem Informasi
Fakultas Teknik
Universitas Widyatama

&nbsp;

Disusun oleh:

**Muhammad Fauzan Fathurrahman**
NPM: 241117001

&nbsp;

Program Studi Sistem Informasi
Fakultas Teknik
Universitas Widyatama
Bandung

---

## ABSTRAK

Keputusan kebijakan di ruang kelas perguruan tinggi, seperti ukuran kelas, kecepatan pemberian umpan balik, dan beban tugas, seringkali diambil berdasarkan intuisi atau kebiasaan yang sudah lama berjalan, bukan atas dasar data empiris yang memadai. Penelitian ini membangun sebuah *digital twin* berbasis simulasi berbasis agen (*agent-based simulation*, ABS) untuk ekosistem kelas universitas selama satu semester (14 minggu perkuliahan aktif), sehingga berbagai skenario kebijakan dapat dibandingkan secara "bagaimana jika" tanpa harus langsung diujicobakan di kelas nyata.

Model terdiri dari *N* agen mahasiswa dan satu agen dosen yang berinteraksi melalui aturan-aturan yang sepenuhnya dapat dikonfigurasi. Lima kelompok skenario eksperimen dijalankan untuk menjawab lima pertanyaan penelitian, yaitu: (RQ1) pengaruh ukuran kelas terhadap kinerja akademik, (RQ2) pengaruh keterlambatan umpan balik dan beban tugas, (RQ3) efektivitas program tutoring bagi mahasiswa berkinerja rendah, (RQ4) dampak keberagaman status sosial ekonomi terhadap ketimpangan IPK, serta (RQ5) pengaruh faktor lingkungan fisik dan mode perkuliahan terhadap hasil belajar.

Hasil simulasi menunjukkan bahwa keterlambatan umpan balik berdampak lebih buruk terhadap IPK rata-rata kelas dibandingkan sekadar memperbesar ukuran kelas. Lebih jauh, kombinasi beban tugas tinggi dan keterlambatan umpan balik menghasilkan efek *non-linear*, yakni dampak gabungannya lebih parah daripada sekadar menjumlahkan pengaruh masing-masing faktor secara terpisah. Program tutoring yang difokuskan pada 25% mahasiswa dengan performa terendah terbukti memberikan peningkatan yang nyata pada kelompok tersebut. Analisis sensitivitas satu-per-satu (*one-at-a-time*, OAT) menegaskan bahwa keterlambatan umpan balik dan beban tugas merupakan dua faktor yang paling menentukan hasil pembelajaran.

Prototipe ini bersifat *open-source*, dapat direproduksi sepenuhnya menggunakan *random seed* yang tetap, dan dilengkapi antarmuka Streamlit agar dapat digunakan oleh pengguna non-teknis tanpa perlu menulis kode. Walaupun parameter model masih bersifat ilustratif dan belum dikalibrasi menggunakan data LMS yang sesungguhnya, arah semua temuan sejalan dengan literatur psikologi pendidikan yang sudah ada.

**Kata kunci:** simulasi berbasis agen, digital twin pendidikan, analisis kebijakan kelas, stres mahasiswa, IPK, umpan balik formatif

---

**ABSTRACT**

Policy decisions in university classrooms, such as class size, feedback speed, and assignment load, are often made based on intuition rather than solid empirical evidence. This study builds a simulation-based digital twin using agent-based simulation (ABS) for a one-semester (14-week) university classroom, allowing policy options to be explored in a "what-if" fashion before they are ever tried in a real classroom.

The model has N student agents and one lecturer agent, all interacting through configurable deterministic rules. Five groups of scenario experiments were run to address five research questions: (RQ1) how class size affects academic performance, (RQ2) how feedback delay and assignment load affect student outcomes, (RQ3) whether a tutoring program meaningfully helps low-performing students, (RQ4) how socioeconomic diversity relates to GPA inequality, and (RQ5) how physical environment and delivery mode shape learning outcomes.

Simulation results show that feedback delay hurts mean GPA more than simply increasing class size, and that pairing high assignment load with feedback delay produces a non-linear effect, meaning the combined damage exceeds what either factor would cause on its own. A tutoring program focused on the bottom 25% of students produced a measurable improvement in that group. One-at-a-time (OAT) sensitivity analysis confirmed that feedback delay and assignment load are the two policy levers that matter most.

The prototype is open-source, fully reproducible using a fixed random seed, and comes with a Streamlit interface so that non-technical users can explore scenarios without writing code. The model parameters are illustrative at this stage and have not been calibrated against real LMS data, though every finding points in the same direction as the existing educational psychology literature. **This work is intended as a policy exploration tool, not a predictive model.**

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
