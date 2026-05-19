# Paper / Skripsi Outline
## Pengembangan Digital Twin Ekosistem Kelas Berbasis Agent-Based Simulation untuk Analisis Faktor yang Mempengaruhi Kinerja Mahasiswa

*(English: Classroom Ecosystem Digital Twin Based on Agent-Based Simulation: Analysis of the Impact of Feedback, Class Size, Tutoring Intervention, and Socioeconomic Status on Student Performance)*

---

## Abstract (≈ 200 words)
- State the problem: educators need low-cost "what-if" tools before implementing policy changes
- State the approach: agent-based simulation with simple, interpretable rules
- State the contribution: reproducible prototype with scenario experiments
- Mention key findings: feedback delay and assignment overload have measurable negative effects on GPA proxy and stress; tutoring intervention improves bottom-quartile outcomes

---

## 1. Introduction
- **1.1 Motivation**
  - University classrooms are complex socio-cognitive systems where student outcomes emerge from the interplay of lecturer behaviour, peer dynamics, and environmental conditions
  - In Indonesia, higher education serves over 9 million students across more than 4,600 institutions (DIKTI, 2023), yet classroom-level policy decisions (class size, grading policies, feedback speed, delivery mode) are often made with limited empirical evidence
  - The rapid expansion of hybrid and fully online delivery following the COVID-19 pandemic has created urgent demand for tools that can help department heads evaluate policy trade-offs before implementation — at low cost and without disrupting real students
  - Learning Management Systems (LMS) such as SPADA and Moodle now generate rich behavioural data on Indonesian campuses; a simulation that mirrors these systems can bridge the gap between raw data and actionable policy insight
  - Digital twins allow low-cost virtual experimentation before real-world deployment; existing computational models in education are often too mathematically complex for classroom practitioners and require specialist software

- **1.2 Problem Statement**
  - How can we build a lightweight, interpretable simulation of classroom dynamics that supports policy comparison?

- **1.3 Research Questions**
  - RQ1: Does larger class size correlate with lower average academic performance in the simulation?
  - RQ2: Does reduced feedback delay improve student outcomes?
  - RQ3: Can a targeted intervention (bottom-quartile tutoring) measurably close the knowledge gap?
  - RQ4: Does a high-SES-diversity cohort produce a larger GPA inequality gap than a low-diversity cohort?
  - RQ5: Do physical environment factors (room temperature, delivery mode) measurably affect student outcomes?

- **1.4 Contributions**
  - A fully configurable, seed-reproducible classroom simulation
  - Five scenario families with clear parameter definitions
  - Open-source prototype with Streamlit dashboard for non-technical users

- **1.5 Paper Structure** (one sentence per section)

---

## 2. Background and Related Work
- **2.1 Agent-Based Modelling (ABM) in Education**
  - Brief overview: Wilenski & Rand (2015); Squazzoni (2012)
  - Examples: classroom ABM for dropout prediction, diffusion of knowledge
  - Gap: most ABMs are either too complex or not classroom-focused

- **2.2 Digital Twin Concept**
  - Origin in engineering (Grieves 2014)
  - Extension to social systems; educational digital twins
  - Distinction from simulation: bidirectional data coupling (this work is a "virtual twin" / policy simulator)

- **2.3 Educational Psychology Foundations**
  - Stress–performance relationship (Yerkes–Dodson inverted-U)
  - Motivation and self-determination theory (Ryan & Deci 2000)
  - Feedback timing: Shute (2008) on formative feedback
  - Class size effects: meta-analyses (Hattie 2008)

- **2.4 Existing Simulation Tools**
  - NetLogo classroom models, Mesa-based ABM, system dynamics (Vensim), and regression/ODE-based statistical models each occupy different points in the complexity–accessibility–reproducibility space
  - Comparison table (Table 1):

  | Approach | Example Tool | Agent-Based | Configurable Policies | Reproducible Seed | Non-Technical UI | Open Source |
  |---|---|---|---|---|---|---|
  | System Dynamics | Vensim / STELLA | No | Limited | Yes | No | Partial |
  | ODE / Statistical | R / SPSS | No | No | Yes | No | Yes |
  | NetLogo ABM | NetLogo classroom models | Yes | Limited | Partial | Yes (GUI) | Yes |
  | Mesa ABM | Custom Python (Mesa) | Yes | Yes | Yes | No (code only) | Yes |
  | **This work** | **ClassTwin (Python + Streamlit)** | **Yes** | **Yes (11 scenarios)** | **Yes (seeded RNG)** | **Yes (web UI)** | **Yes** |

  - Key differentiator: ClassTwin combines full agent-based dynamics, scenario configurability, seeded reproducibility, and a non-technical Streamlit dashboard in a single open-source Python package — a combination not found in existing tools
  - Closest competitor is Mesa-based ABM: more flexible but requires Python programming and has no built-in policy dashboard

---

## 3. Methodology
- **3.1 Model Overview**
  - Agent types: StudentAgent (N), LecturerAgent (1)
  - Time step: 1 week; 14 weeks total
  - State variables for each agent (table)
  - Configuration-driven: all parameters in SimulationConfig

- **3.2 Initialisation**
  - Student heterogeneity: learning_capacity ~ Uniform(0.6, 1.4)
  - Initial motivation, stress, knowledge: truncated Normal distributions
  - Lecturer parameters: set by scenario (Table 1)

- **3.3 Weekly Update Rules**
  - **3.3.1 Attendance** — Bernoulli draw with stress/motivation adjustment
  - **3.3.2 Assignment Completion** — per-assignment Bernoulli; on-time vs late vs missed
  - **3.3.3 Stress Dynamics** — additive model with workload and feedback drivers
  - **3.3.4 Knowledge Dynamics** — multiplicative model; decay term; motivation×(1−stress) modulator
  - **3.3.5 Feedback Loop** — delayed feedback reduces stress and boosts motivation
  - **3.3.6 Intervention** — bottom-quartile students receive weekly stress/motivation boost in weeks 7–10

- **3.4 GPA Proxy Computation**
  - End-of-semester formula: knowledge × 0.7 + effective_completion × 0.3, scaled to [0, 4]
  - Strictness parameter penalises late submissions

- **3.5 Scenario Design** (Table 2)
  | Scenario | n_students | delay | load | ses_std | intervention | notes |
  |---|---|---|---|---|---|---|
  | Baseline | 30 | 1 | 2 | 0.20 | off | reference |
  | Small class | 15 | 1 | 2 | 0.20 | off | RQ1 |
  | Large class | 60 | 1 | 2 | 0.20 | off | RQ1 |
  | Fast feedback | 30 | 0 | 2 | 0.20 | off | RQ2 |
  | Slow feedback | 30 | 4 | 2 | 0.20 | off | RQ2 |
  | Low load | 30 | 1 | 1 | 0.20 | off | RQ2 |
  | High load | 30 | 1 | 3 | 0.20 | off | RQ2 |
  | Stress test | 60 | 4 | 3 | 0.20 | off | worst case |
  | Intervention | 30 | 1 | 2 | 0.20 | on (wk 7–10) | RQ3 |
  | SES diverse | 30 | 1 | 2 | 0.40 | off | RQ4 |
  | Combined | 30 | 0 | 1 | 0.20 | on (wk 7–10) | best-practice |

- **3.6 Reproducibility**
  - All runs seeded via numpy default_rng(seed)
  - config.json saved with every run
  - Section: "How to reproduce all figures"

- **3.7 Sensitivity Analysis (OAT)**
  - One-at-a-time (OAT) parameter sweep: each of 8 key parameters varied from low to high while others held at baseline
  - Parameters tested: class size, feedback delay, assignment load, teaching effectiveness, SES mean, room temperature, peer learning, class mode
  - Target metrics: mean GPA, failure rate, stress
  - Output: tornado chart ranked by |Δ metric| — quantifies which policy levers matter most
  - n_runs=3 seeds per level to reduce stochastic noise

- **3.8 Model Validation**
  - **Face validity**: direction of all effects matches educational literature (Section 5.2)
  - **Convergence test**: scenario run with N = 10, 15, 20, 30, 45, 60, 90, 120 students across 10 seeds each; CI narrows as N increases, confirming stability at N=30
  - **Determinism test**: same seed always produces identical output
  - **Clamp test**: all state variables bounded to valid ranges across 100 random seeds

- **3.9 Model Assumptions and Limitations**
  - Parameters are illustrative; not calibrated to real LMS data (future work)
  - Dropout uses a simple consecutive-stress heuristic; no psychosocial nuance modelled
  - Study groups are fixed at semester start; no dynamic peer network or social influence
  - Single lecturer agent; no TA support, substitute lecturers, or multi-staff modelling
  - External stressors (part-time work, family obligations) represented only as a single scalar pressure term
  - Single course simulation; inter-course dependencies and degree-level curriculum chains not modelled

---

## 4. Experiments and Results
- **4.1 Baseline Run**
  - Figure: stress_over_time, knowledge_over_time (single run)
  - Table: summary metrics for baseline

- **4.2 Class Size Experiment (RQ1)**
  - Compare: small_class (15), baseline (30), large_class (60)
  - Expected: GPA decreases / stress increases with class size
  - Figure: scenario_comparison bar chart

- **4.3 Feedback Delay Experiment (RQ2)**
  - Compare: fast_feedback (0), baseline (1), slow_feedback (4)
  - Expected: longer delay → higher stress → lower GPA
  - Figure: stress_over_time for 3 conditions

- **4.4 Assignment Load Experiment**
  - Compare: low_load (1), baseline (2), high_load (3)
  - Expected: high load → higher stress, lower GPA
  - Figure: knowledge_over_time showing divergence

- **4.5 Stress Test (Combined Worst Case)**
  - 60 students + load=3 + delay=4 vs baseline
  - Figure: comparison of GPA distribution histograms

- **4.6 Intervention Experiment (RQ3)**
  - Baseline vs intervention
  - Sub-analysis: bottom-quartile students specifically
  - Figure: knowledge_over_time with vertical band marking intervention weeks

- **4.7 Physical Environment Experiment (RQ5)**
  - Compare: baseline (22°C, in-person) vs hot_classroom (32°C) vs cold_classroom (16°C)
  - Compare: in-person vs hybrid vs online delivery mode
  - Expected: thermal discomfort reduces motivation and attendance; online reduces knowledge gain via teaching effectiveness and peer learning penalties
  - Figure: multi-scenario GPA bar chart across temperature conditions
  - Figure: knowledge_over_time for in-person vs hybrid vs online

- **4.8 SES Equity Experiment (RQ4)**
  - Compare: baseline (ses_std=0.20) vs ses_diverse (ses_std=0.40)
  - Sub-analysis: GPA by SES quartile (Q1 Low vs Q4 High)
  - Expected: wider SES spread → larger GPA gap between quartiles
  - Figure: ses_equity grouped bar chart (Q1 vs Q4 per scenario)
  - Table: equity_dataframe output — mean_gpa, failure_rate, dropout_rate per quartile

- **4.9 Sensitivity Analysis Results**
  - Tornado chart: feedback delay and assignment load ranked highest impact on GPA
  - Interaction note: high_load + slow_feedback combined is worse than either alone (non-linear)
  - Room temperature and class mode ranked in middle tier — meaningful but secondary
  - Table: full OAT results (parameter, low delta, high delta, max impact)

- **4.10 Robustness Check (Multi-Seed)**
  - Key scenarios re-run with 20 seeds; report mean ± 95% CI
  - Confirms all directional findings hold across random seeds
  - Table: scenario, mean_gpa ± CI, failure_rate ± CI (use this as the definitive Table 3)

- **4.11 Summary of Results** (Table 3)
  - All scenarios side by side: mean_gpa ± CI, failure_rate ± CI, mean_stress, attendance_rate, at_risk_rate

---

## 5. Discussion
- **5.1 Interpretation of Findings**
  - Feedback timing has larger effect than class size alone (reference: Shute 2008)
  - High load + slow feedback combination is disproportionately damaging (interaction effect)
  - Targeted intervention shows diminishing returns after week 10 — implications for real scheduling

- **5.2 Model Validity**
  - **Face validity**: all directional effects align with literature (Hattie 2008, Shute 2008, ASHRAE 55)
  - **Internal validity**: determinism test (same seed → identical output); clamp test (all variables in bounds)
  - **Convergence validity**: CI narrows as N increases from 10→120, confirming N=30 is sufficient for stable estimates (Figure X)
  - **Sensitivity robustness**: OAT analysis shows feedback delay and load consistently dominate; room temperature and class mode are secondary but non-negligible
  - **External validity**: parameters not calibrated to real LMS data — remains future work; directional conclusions are defensible

- **5.3 Comparison with Existing Work**
  - Simpler and more accessible than ODE-based models
  - More configurable than static statistical models

- **5.4 Practical Implications**
  - Department heads can use the Streamlit UI to test policies before implementation
  - A "fast feedback" policy costs little but shows meaningful stress reduction

- **5.5 Limitations**
  - No real dataset used for parameter calibration
  - Social dynamics (peer learning, competition) not modelled
  - Lecturer fatigue not modelled
  - Single course — no curriculum or prerequisite chain

---

## 6. Conclusion
- Summary of contributions
- Answer to each RQ in one sentence
- Future work:
  - Calibrate with anonymised LMS data
  - Add social network layer (peer tutoring)
  - Extend to multi-course curriculum twin
  - Real-time coupling with LMS for true digital-twin feedback loop

---

## References (replace with full APA citations)

**Agent-Based Modelling & Simulation**
- Wilenski, U., & Rand, W. (2015). *An introduction to agent-based modeling*. MIT Press.
- Squazzoni, F. (2012). *Agent-based computational sociology*. Wiley.
- Macal, C. M., & North, M. J. (2010). Tutorial on agent-based modelling and simulation. *Journal of Simulation, 4*(3), 151–162.

**Digital Twins**
- Grieves, M. (2014). Digital twin: manufacturing excellence through virtual factory replication. *White Paper*.
- Rasheed, A., San, O., & Kvamsdal, T. (2020). Digital twin: values, challenges and enablers. *IEEE Access, 8*, 21980–22012.

**Educational Psychology & Learning**
- Ryan, R. M., & Deci, E. L. (2000). Self-determination theory and the facilitation of intrinsic motivation. *American Psychologist, 55*(1), 68–78.
- Duckworth, A. L., Peterson, C., Matthews, M. D., & Kelly, D. R. (2007). Grit: perseverance and passion for long-term goals. *Journal of Personality and Social Psychology, 92*(6), 1087–1101.
- Kahneman, D. (1973). *Attention and effort*. Prentice-Hall.
- Vygotsky, L. S. (1978). *Mind in society: the development of higher psychological processes*. Harvard University Press.

**Feedback & Class Size**
- Shute, V. J. (2008). Focus on formative feedback. *Review of Educational Research, 78*(1), 153–189.
- Hattie, J. (2008). *Visible learning: a synthesis of over 800 meta-analyses relating to achievement*. Routledge.
- Credé, M., & Kuncel, N. R. (2008). Study habits, skills, and attitudes: the third pillar supporting collegiate academic performance. *Perspectives on Psychological Science, 3*(6), 425–453.

**Thermal Comfort & Learning**
- ASHRAE. (2017). *ANSI/ASHRAE Standard 55: Thermal environmental conditions for human occupancy*. ASHRAE.
- Wargocki, P., & Wyon, D. P. (2007). The effects of outdoor air supply rate and supply air temperature on cognitive performance. *HVAC&R Research, 13*(6), 867–882.

**Online & Hybrid Learning**
- Means, B., Toyama, Y., Murphy, R., Bakia, M., & Jones, K. (2010). *Evaluation of evidence-based practices in online learning*. U.S. Department of Education.

---

## Appendix A — Parameter Reference Table
(All SimulationConfig fields with default values, range, and description)

## Appendix B — Source Code Listing
(Key files: config.py, agents.py, dynamics.py — include for thesis submission)

## Appendix C — Running the Dashboard
```
pip install -r requirements.txt
streamlit run src/app/streamlit_app.py
```

## Appendix D — Reproducing All Figures
```
python -m src.experiments.runner
# outputs saved to data/<timestamp>/plots/
```
