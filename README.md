# Workout Tracker

A personal fitness dashboard built with Streamlit. Syncs workout and body weight logs from Google Drive, parses them automatically, and renders interactive dark-themed analytics across five views.

![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=flat&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.56-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-6.7-3F4F75?style=flat&logo=plotly&logoColor=white)
![Google Drive](https://img.shields.io/badge/Google%20Drive-API-4285F4?style=flat&logo=googledrive&logoColor=white)

---

## Features

### Overview
A high-level snapshot of your training. Shows the last session's exercises and sets, a calendar heatmap of training frequency by day of week, and faceted grids of max weight and volume trends across all exercises.

### Exercise
Drill into any individual exercise. Displays a three-panel chart — max weight, total volume, and estimated 1-rep max (e1RM) over time — alongside a full session log filtered to that movement.

> e1RM is calculated using the Epley formula: `weight × (1 + reps / 30)`

### Progress
Your personal records at a glance. A horizontal bar chart of max weight per exercise, top 10 best volume sessions, and a cumulative volume trend over the selected date range.

### Muscles
Filter by muscle group and see every exercise that targets it, weekly set counts, average volume per session, and an anatomical diagram highlighting the relevant muscle.

### Body Metrics
Body weight tracking over time. Plots weekly averages, shows total change, and logs every weigh-in entry in a clean table.

---

## Tech Stack

| Layer | Library |
|---|---|
| UI & Routing | Streamlit |
| Charts | Plotly |
| Data | Pandas |
| Cloud Sync | Google Drive API |
| Auth | Google OAuth 2.0 |
| Package Manager | uv |

---

## Project Structure

```
├── dashboard.py          # App entry point
├── launch.sh             # One-command launcher
├── workout/
│   ├── gdrive.py         # Google Drive sync & OAuth
│   ├── parser.py         # Markdown → structured data
│   ├── storage.py        # CSV caching & calculated columns
│   ├── plots.py          # All Plotly chart functions
│   ├── ui.py             # Dark theme CSS & KPI cards
│   └── views/            # One module per tab
│       ├── overview.py
│       ├── exercise.py
│       ├── progress.py
│       ├── muscles.py
│       └── body.py
├── config/
│   ├── exercises.json    # Shorthand → full exercise name
│   ├── muscles.json      # Exercise → muscle group
│   └── muscle_diagrams.json
└── assets/               # Anatomical muscle diagram PNGs
```

---

## How to Use

### 1. Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) package manager
- A Google account with Drive API enabled

### 2. Clone the repo

```bash
git clone https://github.com/hwasim6/workout-tracker.git
cd workout-tracker
```

### 3. Set up Google Drive credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/) → APIs & Services → Credentials
2. Create an OAuth 2.0 Client ID (Desktop app)
3. Download the JSON and save it as `credentials.json` in the project root

Use `credentials.example.json` as a reference for the expected format.

### 4. Prepare your workout data on Google Drive

The app expects two folders in your Drive root:

**`Workouts/Workouts.md`** — one entry per session:
```
Month Day
Exercise: weight1,weight2;unit;reps1,reps2
```
Example:
```
April 20
BP: 60,70,80;kg;10,8,6
SP: 40,45;kg;10,8
```

**`Weight/Weight.md`** — a markdown table:
```
| Date       | Weight | Unit |
|------------|--------|------|
| 2026-04-20 | 78.5   | kg   |
```

Exercise shorthands are defined in `config/exercises.json` (e.g. `BP` → Bench Press, `SP` → Shoulder Press).

### 5. Run

```bash
./launch.sh
```

Or directly:
```bash
uv run streamlit run dashboard.py
```

On first run, a browser window will open for Google OAuth consent. After approval, a `token.json` is saved locally and reused for all future syncs — you won't be prompted again.

The app opens at **http://localhost:8501**.

---

## Data Flow

```
Google Drive (Workouts.md, Weight.md)
        ↓  gdrive.py
  Raw Markdown Files
        ↓  parser.py
  Structured DataFrames
        ↓  storage.py
  CSV Cache + Derived Columns (volume, e1RM, weight_kg)
        ↓  plots.py + views/
  Streamlit Dashboard
```

---

## Configuration

| File | Purpose |
|---|---|
| `credentials.json` | OAuth client secrets — **never commit** |
| `token.json` | Auto-generated OAuth token — **never commit** |
| `config/exercises.json` | Map shorthand codes to full exercise names |
| `config/muscles.json` | Map exercises to muscle groups |
