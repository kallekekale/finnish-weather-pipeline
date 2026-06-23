import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from data_loader import load_daily_summary
from config import STATIONS

daily_summary = load_daily_summary()

st.title("Weather stats")

station_name = st.selectbox("Station", list(STATIONS.keys()))
station_id = STATIONS[station_name]
filtered = daily_summary[daily_summary["station_id"] == station_id]

dates = sorted(filtered["date"].unique(), reverse=True)
latest = filtered[filtered["date"] == dates[0]].mean(numeric_only=True)
prev = filtered[filtered["date"] == dates[1]].mean(numeric_only=True) if len(dates) > 1 else None

def delta(col):
    if prev is None:
        return None
    return round(latest[col] - prev[col], 1)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Temperature", f"{latest['avg_temp_c']:.1f} °C", delta=delta("avg_temp_c"))
col2.metric("Humidity", f"{latest['avg_humidity_pct']:.1f} %", delta=delta("avg_humidity_pct"))
col3.metric("Wind speed", f"{latest['avg_wind_speed_ms']:.1f} m/s", delta=delta("avg_wind_speed_ms"))
col4.metric("Air pressure", f"{latest['avg_pressure_hpa']:.1f} hPa", delta=delta("avg_pressure_hpa"))

days = st.radio("Range", ["7 days", "30 days", "All"], horizontal=True)
if days != "All":
    cutoff = filtered["date"].max() - pd.Timedelta(days=int(days.split()[0]))
    chart_data = filtered[filtered["date"] >= cutoff].sort_values("date")
else:
    chart_data = filtered.sort_values("date")

st.subheader("Temperature")
fig = go.Figure()
fig.add_trace(go.Scatter(x=chart_data["date"], y=chart_data["min_temp_c"], mode="lines", line={"width": 0}, showlegend=False))
fig.add_trace(go.Scatter(x=chart_data["date"], y=chart_data["max_temp_c"], mode="lines", line={"width": 0}, fill="tonexty", fillcolor="rgba(239,85,59,0.15)", name="Min–Max range"))
fig.add_trace(go.Scatter(x=chart_data["date"], y=chart_data["avg_temp_c"], mode="lines", name="Daily avg", line={"color": "#ef553b"}))
fig.update_layout(yaxis_title="°C", legend={"orientation": "h", "y": -0.2})
st.plotly_chart(fig, use_container_width=True)

st.subheader("Precipitation")
fig2 = px.bar(chart_data, x="date", y="total_precipitation_mm", labels={"date": "", "total_precipitation_mm": "mm"})
st.plotly_chart(fig2, use_container_width=True)
