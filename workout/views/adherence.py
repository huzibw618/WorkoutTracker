import calendar
import pandas as pd
import streamlit as st
from workout.plots import adherence_chart, ACCENT, BG, PANEL, GRID, TEXT, SUBTEXT
from workout.ui import kpi

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
COMPLETED_COLOR = ACCENT
MISSED_COLOR = '#e07b39'


def _calendar_html(today, month_start, selected_weekdays, actual_dates):
    month_end = (month_start + pd.offsets.MonthEnd(0)).normalize()
    first_dow = month_start.weekday()  # 0=Mon

    cells = []
    # leading empty cells
    for _ in range(first_dow):
        cells.append(f'<div class="cal-cell empty"></div>')

    day = month_start
    while day <= month_end:
        num = day.day
        is_planned = day.weekday() in selected_weekdays
        is_past = day <= today
        is_today = day == today

        if is_planned and is_past:
            if day in actual_dates:
                cls, label = "done", "✓"
            else:
                cls, label = "missed", "✗"
        elif is_today:
            cls, label = "today", ""
        else:
            cls, label = "rest", ""

        today_ring = "border: 2px solid #e0e0e0;" if is_today else ""
        cells.append(f'<div class="cal-cell {cls}" style="{today_ring}"><span class="day-num">{num}</span><span class="day-badge">{label}</span></div>')
        day += pd.Timedelta(days=1)

    header_cells = "".join(
        f'<div class="cal-header">{d}</div>'
        for d in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    )
    grid = "".join(cells)
    month_label = month_start.strftime("%B %Y")

    return f"""
    <style>
        .cal-wrap {{ max-width: 700px; margin: 0 auto; }}
        .cal-title {{ text-align: center; font-size: 1.2rem; font-weight: 600;
                      color: {TEXT}; margin-bottom: 14px; letter-spacing: 0.04em; }}
        .cal-grid {{ display: grid; grid-template-columns: repeat(7, 1fr); gap: 6px; }}
        .cal-header {{ text-align: center; font-size: 0.72rem; color: {SUBTEXT};
                       text-transform: uppercase; letter-spacing: 0.06em; padding-bottom: 4px; }}
        .cal-cell {{ background: {PANEL}; border-radius: 8px; aspect-ratio: 1;
                     display: flex; flex-direction: column; align-items: center;
                     justify-content: center; position: relative; border: 2px solid transparent; }}
        .cal-cell.empty {{ background: transparent; }}
        .cal-cell.done {{ background: {COMPLETED_COLOR}22; }}
        .cal-cell.missed {{ background: {MISSED_COLOR}22; }}
        .cal-cell.rest {{ background: {PANEL}; }}
        .cal-cell.today {{ background: {GRID}; }}
        .day-num {{ font-size: 1rem; font-weight: 600; color: {TEXT}; }}
        .cal-cell.done .day-num {{ color: {COMPLETED_COLOR}; }}
        .cal-cell.missed .day-num {{ color: {MISSED_COLOR}; }}
        .day-badge {{ font-size: 0.9rem; font-weight: 700; line-height: 1; }}
        .cal-cell.done .day-badge {{ color: {COMPLETED_COLOR}; }}
        .cal-cell.missed .day-badge {{ color: {MISSED_COLOR}; }}
        .legend {{ display: flex; gap: 20px; justify-content: center; margin-top: 14px; }}
        .legend-item {{ display: flex; align-items: center; gap: 6px;
                        font-size: 0.78rem; color: {SUBTEXT}; }}
        .legend-dot {{ width: 10px; height: 10px; border-radius: 50%; }}
    </style>
    <div class="cal-wrap">
        <div class="cal-title">{month_label}</div>
        <div class="cal-grid">
            {header_cells}
            {grid}
        </div>
        <div class="legend">
            <div class="legend-item">
                <div class="legend-dot" style="background:{COMPLETED_COLOR}"></div> Completed
            </div>
            <div class="legend-item">
                <div class="legend-dot" style="background:{MISSED_COLOR}"></div> Missed
            </div>
            <div class="legend-item">
                <div class="legend-dot" style="background:{SUBTEXT}"></div> Rest day
            </div>
        </div>
    </div>
    """


def render(df: pd.DataFrame):
    today = pd.Timestamp.now().normalize()
    month_start = today.replace(day=1)

    selected_days = st.multiselect(
        "Planned workout days",
        options=DAYS,
        default=["Monday", "Wednesday", "Friday"],
    )

    if not selected_days:
        st.info("Select at least one workout day above.")
        return

    selected_weekdays = {DAYS.index(d) for d in selected_days}

    planned = [d for d in pd.date_range(month_start, today, freq="D") if d.weekday() in selected_weekdays]

    actual_dates = set(
        df[(df["date"] >= month_start) & (df["date"] <= today)]["date"].dt.normalize().unique()
    )

    done = [d for d in planned if d in actual_dates]
    missed = [d for d in planned if d not in actual_dates]

    planned_count = len(planned)
    actual_count = len(done)
    missed_count = len(missed)
    adherence_pct = round(actual_count / planned_count * 100) if planned_count else 0

    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(kpi(planned_count, "Planned"), unsafe_allow_html=True)
    c2.markdown(kpi(actual_count, "Completed"), unsafe_allow_html=True)
    c3.markdown(kpi(missed_count, "Missed"), unsafe_allow_html=True)
    c4.markdown(kpi(f"{adherence_pct}%", "Adherence"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(_calendar_html(today, month_start, selected_weekdays, actual_dates), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.plotly_chart(adherence_chart(planned, actual_dates), use_container_width=True)
