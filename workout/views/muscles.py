import base64
import pandas as pd
import streamlit as st
from workout.plots import exercise_chart
from workout.ui import kpi


def render(filtered: pd.DataFrame, all_muscles: list, start: pd.Timestamp, end: pd.Timestamp, muscle_diagram: dict):
    selected_muscle = st.selectbox("Select muscle", all_muscles, label_visibility="collapsed")
    ex_df = filtered[filtered["muscle"] == selected_muscle].copy()
    muscle_exercises = sorted(ex_df["exercise"].unique())

    if ex_df.empty:
        st.info("No data for this muscle in the selected date range.")
        return

    n_weeks = max((end - start).days / 7, 1)
    avg_sets_per_week = len(ex_df) / n_weeks
    total_volume = ex_df["volume"].sum()
    this_week_sets = len(ex_df[ex_df["date"].dt.to_period("W") == pd.Timestamp.now().to_period("W")])

    m1, m2, m3 = st.columns(3)
    m1.markdown(kpi(this_week_sets, "Sets This Week"), unsafe_allow_html=True)
    m2.markdown(kpi(f"{avg_sets_per_week:.1f}", "Avg Sets / Week"), unsafe_allow_html=True)
    m3.markdown(kpi(f"{total_volume:,.0f} kg", "Total Volume"), unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    for ex in muscle_exercises:
        ex_data = filtered[filtered["exercise"] == ex]
        latest_e1rm = ex_data[ex_data["date"] == ex_data["date"].max()]["e1rm"].max()
        best_e1rm = ex_data["e1rm"].max()

        last_date = ex_data["date"].max()
        days_ago = (pd.Timestamp.now().normalize() - last_date).days
        days_ago_str = "Today" if days_ago == 0 else "Yesterday" if days_ago == 1 else f"{days_ago} days ago"

        st.markdown(f"#### {ex}")
        st.markdown(f"<p style='margin:-10px 0 12px 0;font-size:0.85rem;color:#888'>Last performed: {last_date.strftime('%d %b %Y')} · {days_ago_str}</p>", unsafe_allow_html=True)
        ec1, ec2 = st.columns(2)
        ec1.markdown(kpi(f"{latest_e1rm:.1f} kg", "Latest e1RM"), unsafe_allow_html=True)
        ec2.markdown(kpi(f"{best_e1rm:.1f} kg", "Best e1RM"), unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        chart_col, img_col = st.columns([3, 1])
        with chart_col:
            st.plotly_chart(exercise_chart(filtered, ex), use_container_width=True, key=f"muscle_{ex}")
        with img_col:
            if ex in muscle_diagram:
                img_b64 = base64.b64encode(open(muscle_diagram[ex], "rb").read()).decode()
                st.markdown(
                    f"<div style='height:720px;display:flex;align-items:center;justify-content:center;'>"
                    f"<img src='data:image/png;base64,{img_b64}' style='width:60%;max-height:400px;object-fit:contain;'>"
                    f"</div>",
                    unsafe_allow_html=True,
                )
