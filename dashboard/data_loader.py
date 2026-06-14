from pathlib import Path
import duckdb
import pandas as pd


def _execute_query(db_path: str | Path, query: str) -> pd.DataFrame:
	connection = duckdb.connect(str(db_path), read_only=True)
	try:
		return connection.execute(query).fetchdf()
	except duckdb.Error as exc:
		raise RuntimeError(f"Failed to load dashboard data from DuckDB: {query}") from exc
	finally:
		connection.close()

def load_daily_summary(db_path: str | Path = "data/weather.db") -> pd.DataFrame:
	return _execute_query(db_path, "SELECT * FROM daily_summary")

def load_stg_observations(db_path: str | Path = "data/weather.db") -> pd.DataFrame:
	return _execute_query(db_path, "SELECT * FROM stg_observations")
