WITH base AS (
    SELECT *
    FROM {{ source('raw', 'weather') }}
)

SELECT
    station_id,
    time,

    MAX(CASE WHEN parameter_name = 'TA_PT1H_AVG' THEN parameter_value END) AS temp_c,
    MAX(CASE WHEN parameter_name = 'RH_PT1H_AVG' THEN parameter_value END) AS humidity_pct,
    MAX(CASE WHEN parameter_name = 'WS_PT1H_AVG' THEN parameter_value END) AS wind_speed_ms,
    MAX(CASE WHEN parameter_name = 'WD_PT1H_AVG' THEN parameter_value END) AS wind_direction_deg,
    MAX(CASE WHEN parameter_name = 'PRA_PT1H_ACC' THEN parameter_value END) AS precipitation_mm,
    MAX(CASE WHEN parameter_name = 'PA_PT1H_AVG' THEN parameter_value END) AS pressure_hpa

FROM base
GROUP BY station_id, time