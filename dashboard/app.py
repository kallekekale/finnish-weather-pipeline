import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
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
