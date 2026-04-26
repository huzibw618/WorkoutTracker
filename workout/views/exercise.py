import pandas as pd
import streamlit as st
from workout.plots import exercise_chart
from workout.ui import kpi


def render(filtered: pd.DataFrame, all_exercises: list):
    selected = st.selectbox("Select exercise", all_exercises, label_visibility="collapsed")
    ex_df = filtered[filtered["exercise"] == selected].copy()

    if ex_df.empty:
        st.info("No data for this exercise in the selected date range.")
        return

    last_date = ex_df["date"].max()
    days_ago = (pd.Timestamp.now().normalize() - last_date).days
    days_ago_str = "Today" if days_ago == 0 else "Yesterday" if days_ago == 1 else f"{days_ago} days ago"

    st.markdown(f"### {selected}")
    st.markdown(f"<p style='margin:-10px 0 12px 0;font-size:0.85rem;color:#888'>Last performed: {last_date.strftime('%d %b %Y')} · {days_ago_str}</p>", unsafe_allow_html=True)

    latest_e1rm = ex_df[ex_df["date"] == last_date]["e1rm"].max()
    best_e1rm = ex_df["e1rm"].max()
    c1, c2 = st.columns(2)
    c1.markdown(kpi(f"{latest_e1rm:.1f} kg", "Latest e1RM"), unsafe_allow_html=True)
    c2.markdown(kpi(f"{best_e1rm:.1f} kg", "Best e1RM"), unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    st.plotly_chart(exercise_chart(filtered, selected), use_container_width=True)

    st.markdown("#### Session Log")
    summary = (
        ex_df.groupby("date")
        .agg(sets=("set_number", "count"), max_weight_kg=("weight_kg", "max"), total_volume=("volume", "sum"))
        .reset_index()
        .sort_values("date", ascending=False)
    )
    summary["date"] = summary["date"].dt.strftime("%d %b %Y")
    summary.columns = ["Date", "Sets", "Max Weight (kg)", "Volume (kg)"]
    summary["Max Weight (kg)"] = summary["Max Weight (kg)"].round(1)
    summary["Volume (kg)"] = summary["Volume (kg)"].round(0).astype(int)
    st.dataframe(summary, use_container_width=True, hide_index=True)
