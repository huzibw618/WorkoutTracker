import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

ACCENT = '#4C72B0'
GREEN = '#55a868'
BG = '#0f0f0f'
PANEL = '#1a1a1a'
TEXT = '#e0e0e0'
SUBTEXT = '#888888'
GRID = '#2a2a2a'

_BASE_LAYOUT = dict(
    paper_bgcolor=BG,
    plot_bgcolor=PANEL,
    font=dict(color=TEXT, family='Inter, sans-serif'),
    xaxis=dict(showgrid=True, gridcolor=GRID, zeroline=False, tickfont=dict(color=SUBTEXT)),
    yaxis=dict(showgrid=True, gridcolor=GRID, zeroline=False, tickfont=dict(color=SUBTEXT)),
)


def _apply_axis_style(fig, row, col, ylabel):
    fig.update_xaxes(
        showgrid=True, gridcolor=GRID, zeroline=False,
        tickfont=dict(color=SUBTEXT), tickformat='%d %b %y',
        row=row, col=col
    )
    fig.update_yaxes(
        showgrid=True, gridcolor=GRID, zeroline=False,
        tickfont=dict(color=SUBTEXT), title_text=ylabel,
        title_font=dict(color=SUBTEXT, size=11),
        row=row, col=col
    )


def exercise_chart(data: pd.DataFrame, exercise: str) -> go.Figure:
    """Weight, volume, and e1RM over time for a single exercise."""
    df = data[data['exercise'] == exercise].copy()
    daily_max = df.groupby('date')['weight_kg'].max().reset_index()
    daily_vol = df.groupby('date')['volume'].sum().reset_index()
    daily_e1rm = df.groupby('date')['e1rm'].max().reset_index()

    fig = make_subplots(
        rows=3, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.08,
        subplot_titles=('Max Weight (kg)', 'Volume (kg · reps)', 'Est. 1RM (kg)')
    )

    fig.add_trace(go.Scatter(
        x=daily_max['date'], y=daily_max['weight_kg'],
        mode='lines+markers',
        line=dict(color=ACCENT, width=2),
        marker=dict(size=6, color=ACCENT, line=dict(color='white', width=1.5)),
        hovertemplate='%{x|%d %b %Y}<br><b>%{y:.1f} kg</b><extra></extra>',
        name='Weight'
    ), row=1, col=1)

    fig.add_trace(go.Scatter(
        x=daily_vol['date'], y=daily_vol['volume'],
        mode='lines+markers',
        line=dict(color=GREEN, width=2),
        marker=dict(size=6, color=GREEN, line=dict(color='white', width=1.5)),
        hovertemplate='%{x|%d %b %Y}<br><b>%{y:.0f} kg</b><extra></extra>',
        name='Volume'
    ), row=2, col=1)

    fig.add_trace(go.Scatter(
        x=daily_e1rm['date'], y=daily_e1rm['e1rm'],
        mode='lines+markers',
        line=dict(color='#e07b39', width=2),
        marker=dict(size=6, color='#e07b39', line=dict(color='white', width=1.5)),
        hovertemplate='%{x|%d %b %Y}<br><b>%{y:.1f} kg</b><extra></extra>',
        name='e1RM'
    ), row=3, col=1)

    fig.update_layout(
        paper_bgcolor=BG,
        plot_bgcolor=PANEL,
        font=dict(color=TEXT),
        showlegend=False,
        height=720,
        margin=dict(l=60, r=30, t=40, b=40),
    )

    for annotation in fig.layout.annotations:
        annotation.font.color = SUBTEXT
        annotation.font.size = 12

    _apply_axis_style(fig, row=1, col=1, ylabel='kg')
    _apply_axis_style(fig, row=2, col=1, ylabel='kg')
    _apply_axis_style(fig, row=3, col=1, ylabel='kg')

    return fig


def overview_weight(data: pd.DataFrame) -> go.Figure:
    """Max weight per session for every exercise, faceted grid."""
    daily_max = data.groupby(['date', 'exercise'])['weight_kg'].max().reset_index()
    exercises = sorted(daily_max['exercise'].unique())

    n_cols = 3
    n_rows = -(-len(exercises) // n_cols)

    fig = make_subplots(
        rows=n_rows, cols=n_cols,
        subplot_titles=exercises,
        vertical_spacing=0.08,
        horizontal_spacing=0.06,
    )

    for i, exercise in enumerate(exercises):
        row, col = divmod(i, n_cols)
        ex = daily_max[daily_max['exercise'] == exercise].sort_values('date')
        fig.add_trace(go.Scatter(
            x=ex['date'], y=ex['weight_kg'],
            mode='lines+markers',
            line=dict(color=ACCENT, width=1.8),
            marker=dict(size=5, color=ACCENT),
            hovertemplate='%{x|%d %b %Y}<br><b>%{y:.1f} kg</b><extra></extra>',
            name=exercise,
            showlegend=False,
        ), row=row + 1, col=col + 1)

    fig.update_layout(
        paper_bgcolor=BG,
        plot_bgcolor=PANEL,
        font=dict(color=TEXT),
        height=320 * n_rows,
        margin=dict(l=50, r=30, t=40, b=40),
    )

    for annotation in fig.layout.annotations:
        annotation.font.color = TEXT
        annotation.font.size = 14

    fig.update_xaxes(showgrid=True, gridcolor=GRID, zeroline=False, tickfont=dict(color=SUBTEXT), tickformat='%d %b %y')
    fig.update_yaxes(showgrid=True, gridcolor=GRID, zeroline=False, tickfont=dict(color=SUBTEXT))

    return fig


def pr_chart(data: pd.DataFrame) -> go.Figure:
    """Max weight per exercise — horizontal bar."""
    prs = data.groupby("exercise")["weight_kg"].max().sort_values(ascending=False).reset_index()
    prs["weight_kg"] = prs["weight_kg"].round(1)
    fig = go.Figure(go.Bar(
        x=prs["weight_kg"], y=prs["exercise"],
        orientation="h", marker_color=ACCENT,
        hovertemplate="%{y}<br><b>%{x:.1f} kg</b><extra></extra>",
    ))
    fig.update_layout(
        paper_bgcolor=BG, plot_bgcolor=PANEL, font=dict(color=TEXT),
        xaxis=dict(showgrid=True, gridcolor=GRID, zeroline=False, tickfont=dict(color=SUBTEXT), title_text="kg", title_font=dict(color=SUBTEXT)),
        yaxis=dict(showgrid=False, zeroline=False, tickfont=dict(color=TEXT)),
        margin=dict(l=10, r=20, t=20, b=40), height=500,
    )
    return fig


def best_volume_chart(data: pd.DataFrame) -> go.Figure:
    """Top 10 volume sessions — horizontal bar."""
    best = (
        data.groupby(["date", "exercise"])["volume"].sum().reset_index()
        .sort_values("volume", ascending=False).head(10)
    )
    best["volume"] = best["volume"].round(0).astype(int)
    best["label"] = best["exercise"] + " (" + best["date"].dt.strftime("%d %b %Y") + ")"
    fig = go.Figure(go.Bar(
        x=best["volume"], y=best["label"],
        orientation="h", marker_color=GREEN,
        hovertemplate="%{y}<br><b>%{x:,} kg</b><extra></extra>",
    ))
    fig.update_layout(
        paper_bgcolor=BG, plot_bgcolor=PANEL, font=dict(color=TEXT),
        xaxis=dict(showgrid=True, gridcolor=GRID, zeroline=False, tickfont=dict(color=SUBTEXT), title_text="kg", title_font=dict(color=SUBTEXT)),
        yaxis=dict(showgrid=False, zeroline=False, tickfont=dict(color=TEXT)),
        margin=dict(l=10, r=20, t=20, b=40), height=500,
    )
    return fig


def volume_trend_chart(data: pd.DataFrame) -> go.Figure:
    """Total volume per day — area line."""
    daily = data.groupby("date")["volume"].sum().reset_index()
    fig = go.Figure(go.Scatter(
        x=daily["date"], y=daily["volume"],
        mode="lines+markers", fill="tozeroy",
        fillcolor="rgba(76,114,176,0.15)",
        line=dict(color=ACCENT, width=2), marker=dict(size=6, color=ACCENT),
        hovertemplate="%{x|%d %b %Y}<br><b>%{y:,.0f} kg</b><extra></extra>",
    ))
    fig.update_layout(
        paper_bgcolor=BG, plot_bgcolor=PANEL, font=dict(color=TEXT),
        xaxis=dict(showgrid=True, gridcolor=GRID, zeroline=False, tickfont=dict(color=SUBTEXT), tickformat="%d %b %y"),
        yaxis=dict(showgrid=True, gridcolor=GRID, zeroline=False, tickfont=dict(color=SUBTEXT), title_text="kg", title_font=dict(color=SUBTEXT)),
        margin=dict(l=60, r=30, t=20, b=40), height=280,
    )
    return fig


def calendar_heatmap(data: pd.DataFrame) -> go.Figure:
    """Training frequency calendar heatmap — one cell per day, coloured by session volume."""
    daily = data.groupby("date")["volume"].sum().reset_index()
    daily["date"] = pd.to_datetime(daily["date"])

    start = daily["date"].min() - pd.Timedelta(days=daily["date"].min().weekday())
    end = daily["date"].max()
    all_days = pd.date_range(start, end, freq="D")
    grid = pd.DataFrame({"date": all_days})
    grid = grid.merge(daily, on="date", how="left")
    grid["volume"] = grid["volume"].fillna(0)
    grid["week"] = (grid["date"] - start).dt.days // 7
    grid["dow"] = grid["date"].dt.weekday  # 0=Mon, 6=Sun

    n_weeks = grid["week"].max() + 1
    z = [[None] * n_weeks for _ in range(7)]
    text = [[""] * n_weeks for _ in range(7)]
    for _, row in grid.iterrows():
        w, d = int(row["week"]), int(row["dow"])
        z[d][w] = row["volume"] if row["volume"] > 0 else 0
        text[d][w] = f"{row['date'].strftime('%d %b %Y')}<br>{int(row['volume']):,} kg" if row["volume"] > 0 else row["date"].strftime("%d %b %Y")

    week_starts = [start + pd.Timedelta(weeks=i) for i in range(n_weeks)]
    x_labels = [d.strftime("%d %b") for d in week_starts]

    fig = go.Figure(go.Heatmap(
        z=z,
        x=x_labels,
        y=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        text=text,
        hovertemplate="%{text}<extra></extra>",
        colorscale=[[0, PANEL], [0.001, "#1a3a5c"], [1, ACCENT]],
        showscale=False,
        xgap=3,
        ygap=3,
    ))
    fig.update_layout(
        paper_bgcolor=BG, plot_bgcolor=BG,
        font=dict(color=TEXT),
        xaxis=dict(showgrid=False, zeroline=False, tickfont=dict(color=SUBTEXT), tickangle=-45, tickmode="array", tickvals=x_labels[::4], ticktext=x_labels[::4]),
        yaxis=dict(showgrid=False, zeroline=False, tickfont=dict(color=SUBTEXT), autorange="reversed"),
        margin=dict(l=50, r=20, t=20, b=60),
        height=260,
    )
    return fig


def body_weight_chart(data: pd.DataFrame) -> go.Figure:
    """Body weight over time."""
    df = data.copy().sort_values("date")
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["date"], y=df["weight_kg"],
        mode="lines+markers",
        fill="tozeroy",
        fillcolor="rgba(76,114,176,0.15)",
        line=dict(color=ACCENT, width=2),
        marker=dict(size=6, color=ACCENT, line=dict(color="white", width=1.5)),
        hovertemplate="%{x|%d %b %Y}<br><b>%{y:.1f} kg</b><extra></extra>",
    ))
    fig.update_layout(
        paper_bgcolor=BG, plot_bgcolor=PANEL,
        font=dict(color=TEXT),
        xaxis=dict(showgrid=True, gridcolor=GRID, zeroline=False, tickfont=dict(color=SUBTEXT), tickformat="%d %b %y"),
        yaxis=dict(showgrid=True, gridcolor=GRID, zeroline=False, tickfont=dict(color=SUBTEXT), title_text="kg", title_font=dict(color=SUBTEXT, size=11)),
        margin=dict(l=60, r=30, t=20, b=40),
        height=320,
    )
    return fig


def adherence_chart(planned: list, actual_dates: set) -> go.Figure:
    """Planned workout days coloured by completion — one marker per planned date."""
    today = pd.Timestamp.now().normalize()
    MISSED = '#e07b39'
    UPCOMING = GRID

    groups = {"Completed": ([], ACCENT), "Missed": ([], MISSED), "Upcoming": ([], UPCOMING)}

    for d in planned:
        if d in actual_dates:
            groups["Completed"][0].append(d)
        elif d < today:
            groups["Missed"][0].append(d)
        else:
            groups["Upcoming"][0].append(d)

    fig = go.Figure()
    for label, (dates, color) in groups.items():
        if dates:
            fig.add_trace(go.Scatter(
                x=dates,
                y=[d.strftime("%a") for d in dates],
                mode="markers",
                marker=dict(size=20, color=color, line=dict(color="white", width=1.5)),
                name=label,
                hovertemplate="%{x|%A, %d %b %Y}<br>" + label + "<extra></extra>",
            ))

    fig.update_layout(
        paper_bgcolor=BG, plot_bgcolor=PANEL,
        font=dict(color=TEXT),
        xaxis=dict(showgrid=True, gridcolor=GRID, zeroline=False, tickfont=dict(color=SUBTEXT), tickformat="%d %b"),
        yaxis=dict(showgrid=False, zeroline=False, tickfont=dict(color=TEXT),
                   categoryorder="array", categoryarray=["Sun", "Sat", "Fri", "Thu", "Wed", "Tue", "Mon"]),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color=TEXT)),
        margin=dict(l=60, r=30, t=40, b=40),
        height=320,
    )
    return fig


def overview_volume(data: pd.DataFrame) -> go.Figure:
    """Total volume per session for every exercise, faceted grid."""
    daily_vol = data.groupby(['date', 'exercise'])['volume'].sum().reset_index()
    exercises = sorted(daily_vol['exercise'].unique())

    n_cols = 3
    n_rows = -(-len(exercises) // n_cols)

    fig = make_subplots(
        rows=n_rows, cols=n_cols,
        subplot_titles=exercises,
        vertical_spacing=0.08,
        horizontal_spacing=0.06,
    )

    for i, exercise in enumerate(exercises):
        row, col = divmod(i, n_cols)
        ex = daily_vol[daily_vol['exercise'] == exercise].sort_values('date')
        fig.add_trace(go.Scatter(
            x=ex['date'], y=ex['volume'],
            mode='lines+markers',
            line=dict(color=GREEN, width=1.8),
            marker=dict(size=5, color=GREEN),
            hovertemplate='%{x|%d %b %Y}<br><b>%{y:.0f} kg</b><extra></extra>',
            name=exercise,
            showlegend=False,
        ), row=row + 1, col=col + 1)

    fig.update_layout(
        paper_bgcolor=BG,
        plot_bgcolor=PANEL,
        font=dict(color=TEXT),
        height=320 * n_rows,
        margin=dict(l=50, r=30, t=40, b=40),
    )

    for annotation in fig.layout.annotations:
        annotation.font.color = TEXT
        annotation.font.size = 14

    fig.update_xaxes(showgrid=True, gridcolor=GRID, zeroline=False, tickfont=dict(color=SUBTEXT), tickformat='%d %b %y')
    fig.update_yaxes(showgrid=True, gridcolor=GRID, zeroline=False, tickfont=dict(color=SUBTEXT))

    return fig
