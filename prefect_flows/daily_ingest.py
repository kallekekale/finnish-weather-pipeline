from prefect import flow
from datetime import datetime, timedelta, timezone
from ingestion.fmi_client import fetch_observations, parse_observations, save_to_duckdb
from config import STATIONS

@flow(log_prints=True)
def run_ingestion():
    end = datetime.now(timezone.utc)
    start = end - timedelta(hours=24)
    for name, station_id in STATIONS.items():
        print(name)
        print(station_id)
        observations = fetch_observations(station_id, start, end)
        parsed_observations = parse_observations(observations, station_id)
        save_to_duckdb(parsed_observations)

if __name__ == "__main__":
    run_ingestion()