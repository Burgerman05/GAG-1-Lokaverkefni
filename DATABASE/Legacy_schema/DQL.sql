-- A2 Query 1
-- Monthly energy flow per power plant


SELECT
    eining_heiti AS power_plant_source,
    EXTRACT(YEAR FROM timi) AS year,
    EXTRACT(MONTH FROM timi) AS month,
    tegund_maelingar AS test_measurement_type,
    SUM(gildi_kwh) AS total_kwh
FROM;
