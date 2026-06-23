import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from prefect import flow, task
from datetime import datetime, timedelta, timezone
from ingestion.fmi_client import fetch_observations, parse_observations, save_to_duckdb
from config import STATIONS

@task(retries=3)
def ingest_station(station_id, start, end):
    observations = fetch_observations(station_id, start, end)
    parsed = parse_observations(observations, station_id)
    save_to_duckdb(parsed)

@flow(log_prints=True)
def run_ingestion():
    end = datetime.now(timezone.utc)
    start = end - timedelta(hours=24)
    for station_id in STATIONS.values():
        ingest_station(station_id, start, end)

if __name__ == "__main__":
    run_ingestion()