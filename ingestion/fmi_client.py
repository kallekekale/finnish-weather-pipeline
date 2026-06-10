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

def parse_observations(xml_bytes, station_id):
    root = etree.fromstring(xml_bytes)
    ns = {
        "wfs": "http://www.opengis.net/wfs/2.0",
        "BsWfs": "http://xml.fmi.fi/schema/wfs/2.0"
    }
    parsed_observations = []
    members = root.findall("wfs:member", ns)
    for member in members:
        time = member.find(".//BsWfs:Time", ns)
        parameter_name = member.find(".//BsWfs:ParameterName", ns)
        parameter_value = member.find(".//BsWfs:ParameterValue", ns)
        if time is not None and parameter_name is not None and parameter_value is not None:
            value = parameter_value.text
            if value == 'NaN':
                value = None
            else:
                value = float(value)

            entry = {
                "station_id": station_id,
                "time": time.text,
                "parameter_name": parameter_name.text,
                "parameter_value": value
            }
            parsed_observations.append(entry)
            
    return parsed_observations


if __name__ == "__main__":
    end = datetime.now(timezone.utc)
    start = end - timedelta(hours=24)
    observations = fetch_observations(101118, start, end)
    parsed_observations = parse_observations(observations, 101118)
    print(parsed_observations)
