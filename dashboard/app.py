import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
import streamlit as st
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from data_loader import load_daily_summary, load_stg_observations
from config import STATIONS

daily_summary = load_daily_summary()
stg_observations = load_stg_observations()

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

st.subheader("Temperature")
obs = stg_observations[stg_observations["station_id"] == station_id].sort_values("time")

days = st.radio("Range", ["7 days", "30 days", "All"], horizontal=True)
if days != "All":
    cutoff = obs["time"].max() - pd.Timedelta(days=int(days.split()[0]))
    obs = obs[obs["time"] >= cutoff]

fig = px.line(obs, x="time", y="temp_c", labels={"time": "", "temp_c": "°C"})
fig.update_yaxes(rangemode="normal")
st.plotly_chart(fig, use_container_width=True)

st.subheader("Temperature & precipitation")
fig2 = make_subplots(specs=[[{"secondary_y": True}]])
fig2.add_trace(go.Scatter(x=obs["time"], y=obs["temp_c"], name="Temperature (°C)", line={"color": "#ef553b"}), secondary_y=False)
fig2.add_trace(go.Bar(x=obs["time"], y=obs["precipitation_mm"], name="Precipitation (mm)", marker_color="#636efa", opacity=0.5), secondary_y=True)
fig2.update_yaxes(title_text="°C", secondary_y=False, rangemode="normal")
fig2.update_yaxes(title_text="mm", secondary_y=True, rangemode="tozero")
fig2.update_layout(legend={"orientation": "h", "y": -0.2})
st.plotly_chart(fig2, use_container_width=True)
