import pandas as pd
import streamlit as st
from workout.plots import calendar_heatmap, overview_weight, overview_volume


def render(df: pd.DataFrame, filtered: pd.DataFrame):
    last_date = df["date"].max()
    days_ago = (pd.Timestamp.now().normalize() - last_date).days
    days_ago_str = "Today" if days_ago == 0 else "Yesterday" if days_ago == 1 else f"{days_ago} days ago"

    st.markdown(f"### Last Session — {last_date.strftime('%d %b %Y')} · {days_ago_str}")
    last_session = df[df["date"] == last_date]
    session_log = (
        last_session.groupby("exercise", sort=False)
        .apply(lambda g: " · ".join(f"{row.weight_kg:.1f}kg×{row.reps}" for _, row in g.iterrows()))
        .reset_index()
    )
    session_log.columns = ["Exercise", "Sets"]
    st.dataframe(session_log, use_container_width=True, hide_index=True)

    st.divider()
    st.markdown("<h3 style='text-align:center'>Training Frequency</h3>", unsafe_allow_html=True)
    st.plotly_chart(calendar_heatmap(filtered), use_container_width=True)

    st.markdown("<h3 style='text-align:center'>Max Weight per Session</h3>", unsafe_allow_html=True)
    st.plotly_chart(overview_weight(filtered), use_container_width=True)

    st.markdown("<h3 style='text-align:center'>Volume per Session</h3>", unsafe_allow_html=True)
    st.plotly_chart(overview_volume(filtered), use_container_width=True)
