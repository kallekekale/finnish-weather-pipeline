import pandas as pd
import requests
from lxml import etree
from datetime import datetime, timedelta, timezone

def fetch_observations(station_id, start_time, end_time):
    start_time = start_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    end_time = end_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    url = "https://opendata.fmi.fi/wfs"
    params = {
        "service": "WFS",
        "version": "2.0.0",
        "request": "GetFeature",
        "storedquery_id": "fmi::observations::weather::hourly::simple",
        "fmisid": station_id,
        "starttime": start_time,
        "endtime": end_time
    }

    res = requests.get(url, params=params)
    res.raise_for_status()

    return res.content


if __name__ == "__main__":
    end = datetime.now(timezone.utc)
    start = end - timedelta(hours=24)
    print(fetch_observations(101118, start, end))
