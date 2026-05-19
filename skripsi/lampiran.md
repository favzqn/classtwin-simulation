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
