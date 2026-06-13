SELECT
    station_id,
    CAST(DATE_TRUNC('day', time) AS DATE) AS date,
    ROUND(AVG(temp_c), 1) AS avg_temp_c,
    ROUND(MIN(temp_c), 1) AS min_temp_c,
    ROUND(MAX(temp_c), 1) AS max_temp_c,
    ROUND(AVG(humidity_pct), 1) AS avg_humidity_pct,
    ROUND(MIN(humidity_pct), 1) AS min_humidity_pct,
    ROUND(MAX(humidity_pct), 1) AS max_humidity_pct,
    ROUND(AVG(wind_speed_ms), 1) AS avg_wind_speed_ms,
    ROUND(MIN(wind_speed_ms), 1) AS min_wind_speed_ms,
    ROUND(MAX(wind_speed_ms), 1) AS max_wind_speed_ms,
    ROUND(AVG(wind_direction_deg), 1) AS avg_wind_direction_deg,
    ROUND(AVG(precipitation_mm), 1) AS avg_precipitation_mm,
    ROUND(MIN(precipitation_mm), 1) AS min_precipitation_mm,
    ROUND(MAX(precipitation_mm), 1) AS max_precipitation_mm,
    ROUND(AVG(pressure_hpa), 1) AS avg_pressure_hpa,
    ROUND(MIN(pressure_hpa), 1) AS min_pressure_hpa,
    ROUND(MAX(pressure_hpa), 1) AS max_pressure_hpa

FROM {{ ref("stg_observations") }}
GROUP BY station_id, DATE_TRUNC('day', time)
