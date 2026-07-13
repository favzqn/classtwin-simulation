<div align="center">

# ClassTwin

### Classroom Ecosystem Digital Twin

**Agent-based simulation for "what-if" policy analysis in higher education**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-40%20passed-brightgreen)]()
[![Streamlit](https://img.shields.io/badge/dashboard-Streamlit-ff4b4b)](https://share.streamlit.io/)

*Explore how class size, feedback timing, workload, and environment shape student outcomes — before applying changes in the real classroom.*

[**Try the Live Dashboard →**](https://classtwin-simulation.streamlit.app)
[**Read the Paper**](#citation) · [**Quick Start**](#quick-start) · [**API Reference**](#python-api)

</div>

---

## What is ClassTwin?

University classrooms are complex systems where stress, motivation, attendance, and knowledge interact in non-obvious ways. ClassTwin lets you simulate an entire 14-week semester and run policy experiments — no real students affected.

It's a **digital model** (level 1 of the [digital twin spectrum](https://doi.org/10.1109/ACCESS.2020.2970143)) built on agent-based modeling. Each of the 30 students has their own knowledge, stress, motivation, and socioeconomic background. They interact through peer learning groups. A lecturer agent manages feedback timing and assignment load. The simulation runs for 14 weeks, and you get GPA distributions, dropout rates, attendance curves, and more.

## Key Results

| Policy Scenario | GPA (0–4) | Failure Rate | vs Baseline |
|---|---|---|---|
| **Best Practice Bundle** (fast feedback + low load + tutoring) | **3.47** | 0% | +0.46 |
| Immediate Feedback (0-week delay) | 3.17 | 0% | +0.16 |
| Small Class (15 students) | 3.17 | 0% | +0.16 |
| **Baseline** (30 students, 1-week delay) | **3.01** | 0% | — |
| Heavy Workload (3 assignments/week) | 2.72 | 6.7% | −0.30 |
| Large Class (60 students) | 2.32 | 10% | −0.70 |
| Slow Feedback (4-week delay) | 2.22 | 30% | −0.79 |
| **Worst Case** (60 students + overload + slow feedback) | **1.72** | 90% | −1.30 |

**Total policy impact range: 1.75 GPA points** between best and worst scenarios.

The #1 policy lever? **Feedback speed** — reducing delay from 4 weeks to 0 has a larger effect than halving class size.

## Quick Start

```bash
# Install
git clone https://github.com/favzqn/classtwin-simulation.git
cd classtwin-simulation
pip install -r requirements.txt

# Launch the interactive dashboard
streamlit run src/app/streamlit_app.py

# Run all scenarios from CLI
python -m src.experiments.runner

# Run specific scenarios
python -m src.experiments.runner baseline high_load slow_feedback

# Run tests
pytest tests/ -v
```

## Dashboard

The Streamlit dashboard has three tabs:

1. **Simulator** — adjust every parameter interactively and see results in real time
2. **Campus Board** — executive summary, policy ROI comparison, equity analysis by SES quartile
3. **Deep Dive** — topic mastery heatmap, at-risk student list, dropout timeline

## Python API

```python
from src.config import SimulationConfig
from src.model.classroom_model import ClassroomModel

# Custom scenario
cfg = SimulationConfig(n_students=40, seed=42)
cfg.lecturer.feedback_delay_weeks = 2
cfg.lecturer.assignment_load = 3

model = ClassroomModel(cfg)
model.run()

print(model.summary())
# {'mean_gpa': 2.81, 'failure_rate': 0.05, 'mean_final_stress': 0.34, ...}

# Access full student-level data
df = model.student_dataframe()     # one row per student
weekly = model.weekly_dataframe()  # one row per week
equity = model.equity_dataframe()  # SES quartile breakdown
```

### Reproducibility

Every simulation uses a fixed random seed. Same config + same seed = identical output, guaranteed.

```python
import json
cfg = SimulationConfig(seed=42)
# Save config
Path("config.json").write_text(cfg.model_dump_json(indent=2))
# Reload and reproduce
cfg2 = SimulationConfig.model_validate_json(Path("config.json").read_text())
```

## Scenarios

| Name | Students | Feedback Delay | Load | Description |
|---|---|---|---|---|
| `baseline` | 30 | 1 wk | 2/wk | Standard reference class |
| `large_class` | 60 | 1 wk | 2/wk | Double class size |
| `small_class` | 15 | 1 wk | 2/wk | Half class size |
| `fast_feedback` | 30 | 0 wk | 2/wk | Same-week return |
| `slow_feedback` | 30 | 4 wk | 2/wk | Very slow grading |
| `low_load` | 30 | 1 wk | 1/wk | Light workload |
| `high_load` | 30 | 1 wk | 3/wk | Heavy workload |
| `stress_test` | 60 | 4 wk | 3/wk | Worst-case combined |
| `intervention` | 30 | 1 wk | 2/wk | Tutoring weeks 7–10 |
| `ses_diverse` | 30 | 1 wk | 2/wk | High SES variance |
| `combined_intervention` | 30 | 0 wk | 1/wk | Best-practice bundle |

## How It Works

```
┌─────────────────────────────────────────────────┐
│  SimulationConfig (Pydantic — fully serializable) │
└──────────────────────┬──────────────────────────┘
                       │
          ┌────────────▼────────────┐
          │     ClassroomModel      │
          │  14-week simulation loop │
          └────────────┬────────────┘
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
  StudentAgent × N  LecturerAgent   Study Groups
  (stress, knowledge, (feedback delay,  (peer learning,
   motivation, SES,   assignment load,   mixed formation)
   grit, fatigue)     adaptivity)
        │              │              │
        └──────────────┼──────────────┘
                       ▼
          Weekly aggregates → End-of-semester GPA
```

**Weekly update per student:** Attendance → Assignments → Stress → Knowledge → Motivation → Fatigue → Satisfaction → Peer Learning → Intervention

**End-of-semester:** GPA = 0.7 × knowledge + 0.3 × completion_rate (scaled to 0–4)

## Validation

| Test | What it checks |
|---|---|
| Determinism | Same seed → bit-identical output |
| Clamp | All state variables stay in [0, 1]; GPA in [0, 4] |
| Scenario ordering | Higher load ≤ lower load GPA; higher delay ≥ higher stress |
| Config round-trip | JSON serialize → deserialize → identical run |
| Convergence | CI narrows as N increases; N=30 is sufficient |
| Face validity | All effect directions match published literature |

## Tech Stack

| Library | Purpose |
|---|---|
| [NumPy](https://numpy.org/) | Random number generation, array math |
| [Pydantic](https://docs.pydantic.dev/) | Configuration validation & JSON serialization |
| [pandas](https://pandas.pydata.org/) | DataFrames, CSV export |
| [Matplotlib](https://matplotlib.org/) | Publication-quality figures |
| [Seaborn](https://seaborn.pydata.org/) | Statistical visualization |
| [Streamlit](https://streamlit.io/) | Interactive dashboard |
| [pytest](https://docs.pytest.org/) | Unit testing |

## Project Structure

```
classtwin-simulation/
├── src/
│   ├── config.py                # SimulationConfig (Pydantic)
│   ├── model/
│   │   ├── agents.py            # StudentAgent, LecturerAgent
│   │   ├── classroom_model.py   # Orchestration engine
│   │   └── dynamics.py          # Pure-function update rules
│   ├── experiments/
│   │   ├── scenarios.py         # 19 named scenario configs
│   │   └── runner.py            # Batch runner + CLI
│   ├── viz/
│   │   └── plots.py             # Matplotlib figures
│   └── app/
│       └── streamlit_app.py     # Interactive dashboard
├── tests/
│   └── test_simulation.py       # 40 tests
├── data/
│   └── example_run/             # Pre-generated results
└── docs/
    └── skripsi/                 # Full thesis (Indonesian)
```

## Citation

If you use ClassTwin in your research, please cite:

```bibtex
@mastersthesis{fauzan2026classtwin,
  title     = {Classroom Ecosystem Digital Twin: Agent-Based Simulation
               for Policy Analysis in Higher Education},
  author    = {Fauzan},
  year      = {2026},
  school    = {Universitas Widyatama},
  address   = {Bandung, Indonesia},
  type      = {Bachelor's thesis (Skripsi)},
  url       = {https://github.com/favzqn/classtwin-simulation}
}
```

## Contributing

Contributions welcome. Open an issue or submit a PR. For major changes, open an issue first to discuss what you'd like to change.

## License

[MIT](LICENSE)
