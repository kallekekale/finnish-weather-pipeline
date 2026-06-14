# Finnish Weather Pipeline

A data pipeline that ingests hourly weather observations from the Finnish Meteorological Institute (FMI) open data API and transforms them into daily summaries using dbt.

## Overview

The pipeline fetches observations from five stations (Tampere, Helsinki, Turku, Oulu, and Rovaniemi) on a daily schedule. Raw data is stored in DuckDB and transformed through two dbt layers: a staging model that pivots the raw parameter rows into typed columns, and a mart model that aggregates hourly readings into daily min/avg/max statistics.

## Stack

- **Ingestion**: Python + Prefect
- **Storage**: DuckDB (`data/weather.db`)
- **Transformation**: dbt-core with dbt-duckdb adapter
- **Dashboard**: Streamlit

## Architecture

The pipeline follows a layered structure loosely based on the medallion pattern:

- **Bronze** — raw observations stored as-is from the FMI API (`raw.weather`). FMI returns data in EAV format (one row per parameter per timestamp), so the table reflects that structure without modification.
- **Silver** — `stg_observations` pivots the EAV rows into typed wide columns (one row per station per hour).
- **Gold** — `daily_summary` aggregates hourly readings into daily min/avg/max statistics per station.

A full medallion implementation would store raw XML in bronze and push all parsing into dbt. At this scale and with a single source that would be over-engineering.

## Project Structure

```
config.py                    # Shared config (stations, DB path)
ingestion/
  fmi_client.py              # FMI WFS API client, XML parser, DuckDB writer
prefect_flows/
  daily_ingest.py            # Prefect flow that runs ingestion for all stations
dbt_project/
  models/
    staging/
      stg_observations.sql   # Pivots raw EAV rows into typed columns
      stg_observations.yml   # dbt tests: not_null, unique, accepted_range
      sources.yml            # Source definition with not_null tests on raw data
    mart/
      daily_summary.sql      # Daily min/avg/max aggregates per station
  packages.yml               # dbt_utils dependency
dashboard/
  app.py                     # Streamlit dashboard with station selector and KPI metrics
  data_loader.py             # DuckDB query helpers
data/
  weather.db                 # DuckDB database (not committed)
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
dbt deps
dbt run
```

Run dbt tests:

```bash
dbt test
```

Run the dashboard:

```bash
streamlit run dashboard/app.py
```
