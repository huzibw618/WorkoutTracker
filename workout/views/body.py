import pandas as pd
import streamlit as st
from workout.plots import body_weight_chart
from workout.ui import kpi


def render(weight_df: pd.DataFrame):
    if weight_df.empty:
        st.info("No body weight data available.")
        return

    wdf = weight_df.copy()
    wdf["weight_kg"] = wdf.apply(
        lambda r: r["weight"] * 0.453592 if r["unit"].strip().lower() == "lbs" else r["weight"], axis=1
    )
    wdf = wdf.sort_values("date")

    latest = wdf.iloc[-1]["weight_kg"]
    first = wdf.iloc[0]["weight_kg"]

    last7 = wdf.tail(7)
    has_weekly_avg = len(last7) == 7 and (last7["date"].iloc[-1] - last7["date"].iloc[0]).days == 6
    weekly_avg_val = last7["weight_kg"].mean() if has_weekly_avg else None
    weekly_avg_str = f"{weekly_avg_val:.1f} kg" if has_weekly_avg else "-"

    avg_change = weekly_avg_val - first if has_weekly_avg else None
    avg_change_str = f"{'+'if avg_change >= 0 else ''}{avg_change:.1f} kg" if avg_change is not None else "-"

    k1, k2, k3, k4 = st.columns(4)
    k1.markdown(kpi(f"{latest:.1f} kg", "Latest Weight"), unsafe_allow_html=True)
    k2.markdown(kpi(f"{first:.1f} kg", "Starting Weight"), unsafe_allow_html=True)
    k3.markdown(kpi(avg_change_str, "Total Change"), unsafe_allow_html=True)
    k4.markdown(kpi(weekly_avg_str, "7-Day Average"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### Weight Over Time")
    st.plotly_chart(body_weight_chart(wdf), use_container_width=True)

    st.markdown("### Log")
    log = wdf[["date", "weight_kg"]].sort_values("date", ascending=False).copy()
    log["date"] = log["date"].dt.strftime("%d %b %Y")
    log.columns = ["Date", "Weight (kg)"]
    log["Weight (kg)"] = log["Weight (kg)"].round(1)
    st.dataframe(log, use_container_width=True, hide_index=True)
