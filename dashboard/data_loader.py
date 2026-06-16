import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import duckdb
import pandas as pd
from config import DB_PATH


def _execute_query(query: str) -> pd.DataFrame:
	connection = duckdb.connect(DB_PATH)
	try:
		return connection.execute(query).fetchdf()
	except duckdb.Error as exc:
		raise RuntimeError(f"Failed to load dashboard data from DuckDB: {query}") from exc
	finally:
		connection.close()

def load_daily_summary() -> pd.DataFrame:
	return _execute_query("SELECT * FROM daily_summary")

def load_stg_observations() -> pd.DataFrame:
	return _execute_query("SELECT * FROM stg_observations")
