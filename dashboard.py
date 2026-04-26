import json
import streamlit as st
import pandas as pd
from workout.config import MD_PATH, WEIGHT_MD, MUSCLE_DIAGRAMS_PATH, WORKOUTS_CSV, WEIGHT_CSV
from workout.gdrive import GdriveHandler
from workout.parser import parseMD, parseWeightMD
from workout.storage import loadCSV, writeCSV
from workout.plots import TEXT
from workout.ui import CSS, kpi
from workout.views import overview, exercise, progress, muscles, body, adherence

with open(MUSCLE_DIAGRAMS_PATH) as f:
    MUSCLE_DIAGRAM = json.load(f)

st.set_page_config(page_title="Workout Dashboard", layout="wide", page_icon="🏋️", initial_sidebar_state="collapsed")
st.markdown(CSS, unsafe_allow_html=True)


@st.cache_data
def load_data():
    gdrive = GdriveHandler()
    gdrive.downloadFile()
    writeCSV(parseMD(MD_PATH))

    gdrive.downloadFile(folder_name="Workouts", file_name="Weight")
    writeCSV(parseWeightMD(WEIGHT_MD), csv_path=WEIGHT_CSV, cols=["date", "weight", "unit"])

    return loadCSV(WORKOUTS_CSV), loadCSV(WEIGHT_CSV)


df, weight_df = load_data()
all_exercises = sorted(df["exercise"].unique())
all_muscles = sorted(df["muscle"].unique())
min_date, max_date = df["date"].min().date(), df["date"].max().date()

# ── Header ────────────────────────────────────────────────────────────────────
hdr_left, hdr_right = st.columns([3, 1])
hdr_left.markdown(f"<h2 style='color:{TEXT};margin:0'>🏋️ Workout Tracker</h2>", unsafe_allow_html=True)
date_range = hdr_right.date_input("Date Range", value=(min_date, max_date), min_value=min_date, max_value=max_date, label_visibility="collapsed")
st.divider()

# ── Date filter ───────────────────────────────────────────────────────────────
if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
    start, end = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])
else:
    start, end = pd.Timestamp(min_date), pd.Timestamp(max_date)

filtered = df[(df["date"] >= start) & (df["date"] <= end)].copy()

# ── Global KPIs ───────────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
c1.markdown(kpi(filtered["date"].nunique(), "Sessions"), unsafe_allow_html=True)
c2.markdown(kpi(f"{filtered['volume'].sum():,.0f} kg", "Total Volume"), unsafe_allow_html=True)
c3.markdown(kpi(filtered["exercise"].nunique(), "Exercises"), unsafe_allow_html=True)
c4.markdown(kpi(len(filtered), "Total Sets"), unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab_overview, tab_exercise, tab_progress, tab_muscle, tab_body, tab_adherence = st.tabs(
    ["📊  Overview", "🔍  Exercise", "🏆  Progress", "💪 Muscles", "⚖️  Body Metrics", "📅  Adherence"]
)

with tab_overview:
    overview.render(df, filtered)

with tab_exercise:
    exercise.render(filtered, all_exercises)

with tab_progress:
    progress.render(filtered)

with tab_muscle:
    muscles.render(filtered, all_muscles, start, end, MUSCLE_DIAGRAM)

with tab_body:
    body.render(weight_df)

with tab_adherence:
    adherence.render(df)
