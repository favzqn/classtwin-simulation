## BAB V: KESIMPULAN DAN SARAN

### 5.1 Kesimpulan

Penelitian ini berhasil merancang, mengimplementasikan, dan memvalidasi sebuah prototipe *Classroom Ecosystem Digital Twin* berbasis simulasi berbasis agen untuk ekosistem kelas universitas satu semester (14 minggu). Berdasarkan eksperimen skenario yang dijalankan, berikut adalah jawaban atas kelima pertanyaan penelitian:

**RQ1 — Pengaruh ukuran kelas:**
Ukuran kelas yang lebih besar (60 mahasiswa) menghasilkan IPK rata-rata yang lebih rendah dan tingkat kegagalan yang lebih tinggi dibandingkan kelas standar (30) maupun kelas kecil (15) dalam simulasi. Mekanisme utamanya adalah pengurangan efektivitas pengajaran per-mahasiswa dan akumulasi penundaan umpan balik yang lebih besar pada kelas besar.

**RQ2 — Pengaruh keterlambatan umpan balik dan beban tugas:**
Keterlambatan umpan balik memiliki dampak negatif yang lebih besar terhadap IPK rata-rata dibandingkan peningkatan beban tugas saja. Pengurangan keterlambatan dari 4 minggu ke segera menghasilkan selisih IPK terbesar di antara semua intervensi yang diuji. Temuan ini konsisten dengan meta-analisis Shute (2008) dan Hattie (2008). Kombinasi beban tugas berat dan umpan balik sangat lambat (skenario terburuk) menghasilkan efek negatif yang bersifat *non-linear*, lebih buruk dari jumlah dampak individual.

Berdasarkan analisis sensitivitas OAT, **urutan prioritas faktor kebijakan berdasarkan besaran dampak terhadap IPK rata-rata adalah: umpan balik (+0,95) > ukuran kelas (+0,85) > efektivitas pengajaran (+0,70) > mode perkuliahan (+0,48) > beban tugas (+0,37)**. Implikasi langsungnya: program studi yang ingin meningkatkan kinerja mahasiswa sebaiknya memprioritaskan kebijakan pengembalian nilai yang cepat — faktor dengan dampak terbesar dan biaya implementasi yang relatif rendah — sebelum mempertimbangkan perubahan ukuran kelas yang membutuhkan investasi lebih besar.

**RQ3 — Efektivitas program tutoring:**
Program tutoring selama 4 minggu (minggu 7–10) yang ditargetkan kepada 25% mahasiswa berkinerja terendah berhasil meningkatkan IPK rata-rata kuartil terbawah secara terukur. Terdapat efek *momentum* pasca-program: peningkatan berlanjut meskipun intervensi telah berakhir. Intervensi yang ditargetkan terbukti lebih efisien daripada perubahan kebijakan yang berlaku untuk seluruh kelas.

**RQ4 — Keberagaman SES dan kesenjangan IPK:**
Hasil simulasi menunjukkan bahwa kohort dengan keberagaman SES tinggi (std = 0,40) tidak menghasilkan kesenjangan IPK antar-kuartil yang lebih besar dibandingkan baseline (std = 0,20); kesenjangan justru lebih kecil (0,06 vs 0,21). Namun, IPK absolut mahasiswa Q1 pada skenario ses_diverse (2,89) lebih rendah dari baseline (2,96), mengonfirmasi bahwa mahasiswa SES rendah tetap dirugikan secara absolut oleh keberagaman yang tinggi. Temuan ini sebagian konsisten dengan Sirin (2005) dalam hal dampak negatif SES rendah terhadap IPK absolut, namun tidak mengkonfirmasi hipotesis bahwa keberagaman lebih tinggi memperlebar kesenjangan antar-kuartil dalam konteks simulasi ini.

**RQ5 — Faktor lingkungan fisik dan mode perkuliahan:**
Suhu ruangan di luar zona nyaman (20–24°C), baik terlalu panas maupun terlalu dingin, mengurangi motivasi, kehadiran, dan IPK rata-rata. Kelas panas (32°C, kondisi tanpa AC) menunjukkan dampak yang lebih besar daripada kelas dingin (16°C). Perkuliahan daring penuh menghasilkan IPK rata-rata lebih rendah dibandingkan tatap muka akibat pengurangan efektivitas pengajaran dan pembelajaran teman sebaya; perkuliahan hibrida berada di antara keduanya.

**Kesimpulan umum:**
Simulasi berbasis agen terbukti dapat menangkap pola kualitatif dinamika kelas yang konsisten dengan literatur psikologi pendidikan. Prototipe ClassTwin yang dikembangkan bersifat *open-source*, sepenuhnya dapat direproduksi, dan dilengkapi antarmuka *dashboard* untuk pengguna non-teknis, memenuhi kebutuhan alat analisis kebijakan kelas yang ringan dan interpretatif.

### 5.2 Validitas Model

Model ini telah divalidasi melalui empat mekanisme:

- **Validitas wajah:** Semua arah efek konsisten dengan prediksi literatur (Hattie 2008, Shute 2008, ASHRAE 55, Means et al. 2010).
- **Determinisme:** Simulasi dengan *seed* yang sama selalu menghasilkan keluaran yang identik.
- **Uji klem:** Semua variabel status tetap dalam rentang valid [0,1] di seluruh 100 *seed* acak.
- **Konvergensi:** CI menyempit seiring meningkatnya N, mengonfirmasi bahwa N = 30 cukup untuk estimasi yang stabil.

Sebagaimana dijelaskan pada Bagian 3.10, validitas model bersifat **validitas wajah dan internal**; validitas eksternal (kemampuan model untuk memprediksi kelas nyata secara kuantitatif) membutuhkan kalibrasi parameter dengan data LMS nyata, yang merupakan pekerjaan masa depan.

### 5.3 Saran

Beberapa rekomendasi untuk pengembangan selanjutnya:

1. **Kalibrasi dengan data LMS nyata.** Menggunakan data anonim dari platform SPADA, Moodle, atau sistem LMS internal kampus untuk mengkalibrasi parameter seperti `base_learning_rate`, `stress_threshold`, dan `w_feedback`. Ini akan mengubah prototipe dari *virtual twin* menjadi *digital twin* dalam arti yang lebih penuh (Rasheed et al., 2020).

2. **Penambahan lapisan jaringan sosial.** Mengimplementasikan jaringan pertemanan yang dinamis di mana mahasiswa membentuk dan memodifikasi kelompok belajar sepanjang semester. Ini akan memungkinkan pemodelan efek *peer pressure*, difusi pengetahuan yang lebih realistis, dan dinamika *clique* sosial (Vygotsky, 1978).

3. **Perpanjangan ke kurikulum multi-mata-kuliah.** Mengembangkan model yang merepresentasikan rantai prasyarat mata kuliah lintas semester, memungkinkan simulasi dampak kebijakan di tingkat program studi atau kurikulum secara keseluruhan.

4. **Koneksi real-time dengan LMS.** Mengimplementasikan *pipeline* data yang mengambil data perilaku belajar aktual dari LMS secara periodik, memperbarui parameter agen secara dinamis, dan menggunakan model untuk memproyeksikan trajektori mahasiswa berisiko, mewujudkan *digital twin* dalam pengertian penuh (Baker & Yacef, 2009).

5. **Validasi lintas kampus.** Menjalankan studi perbandingan antara hasil simulasi dan data historis dari beberapa kampus berbeda di Indonesia untuk menilai generalisabilitas model.
