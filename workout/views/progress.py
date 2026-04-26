import pandas as pd
import streamlit as st
from workout.plots import pr_chart, best_volume_chart, volume_trend_chart


def render(filtered: pd.DataFrame):
    col_left, col_right = st.columns(2)
    with col_left:
        st.markdown("### 🥇 Personal Records (Max Weight)")
        st.plotly_chart(pr_chart(filtered), use_container_width=True)
    with col_right:
        st.markdown("### 📈 Best Volume Sessions")
        st.plotly_chart(best_volume_chart(filtered), use_container_width=True)

    st.markdown("### 📅 Volume Over Time (All Exercises)")
    st.plotly_chart(volume_trend_chart(filtered), use_container_width=True)
