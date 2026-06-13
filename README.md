# Finnish Weather Pipeline

A data pipeline that ingests hourly weather observations from the Finnish Meteorological Institute (FMI) open data API and transforms them into daily summaries using dbt.

## Overview

The pipeline fetches observations from five stations (Tampere, Helsinki, Turku, Oulu, and Rovaniemi) on a daily schedule. Raw data is stored in DuckDB and transformed through two dbt layers: a staging model that pivots the raw parameter rows into typed columns, and a mart model that aggregates hourly readings into daily min/avg/max statistics.

## Stack

- **Ingestion**: Python + Prefect
- **Storage**: DuckDB (`data/weather.db`)
- **Transformation**: dbt-core with dbt-duckdb adapter

## Project Structure

```
ingestion/
  fmi_client.py        # FMI WFS API client, XML parser, DuckDB writer
prefect_flows/
  daily_ingest.py      # Prefect flow that runs ingestion for all stations
dbt_project/
  models/
    staging/
      stg_observations.sql   # Pivots raw parameter rows into typed columns
    mart/
      daily_summary.sql      # Daily min/avg/max aggregates per station
  dbt_project.yml
data/
  weather.db           # DuckDB database (not committed)
```

## Data Source

Observations come from the FMI open data WFS endpoint using the `fmi::observations::weather::hourly::simple` stored query. The following parameters are captured:

| Parameter      | Description           |
| -------------- | --------------------- |
| `TA_PT1H_AVG`  | Air temperature (C)   |
| `RH_PT1H_AVG`  | Relative humidity (%) |
| `WS_PT1H_AVG`  | Wind speed (m/s)      |
| `WD_PT1H_AVG`  | Wind direction (deg)  |
| `PRA_PT1H_ACC` | Precipitation (mm)    |
| `PA_PT1H_AVG`  | Air pressure (hPa)    |

## Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure a dbt profile named `weather_pipeline` pointing at the DuckDB file. Example `~/.dbt/profiles.yml`:

```yaml
weather_pipeline:
  target: dev
  outputs:
    dev:
      type: duckdb
      path: /absolute/path/to/finnish-weather-pipeline/data/weather.db
```

Note: dbt requires an absolute path here. Replace the path above with the actual location on your machine.

## Running

Run ingestion manually:

```bash
python prefect_flows/daily_ingest.py
```

Run dbt transformations:

```bash
cd dbt_project
dbt run
```
