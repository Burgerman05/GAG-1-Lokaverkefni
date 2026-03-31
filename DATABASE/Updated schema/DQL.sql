-- Task C5
-- # 1
EXPLAIN ANALYZE
SELECT
    AM.heiti as power_plant_source,
    EXTRACT(YEAR FROM AM.timi) as year,
    EXTRACT(MONTH FROM AM.timi) as month,
    AM.maeling_type as test_measurement_type,
    SUM(AM.gildi_kwh) as total_kwh
FROM raforka_updated.allar_maelingar AM
WHERE
    EXTRACT(YEAR FROM AM.timi) = 2025
GROUP BY
    AM.heiti,
    year,
    month,
    AM.maeling_type
ORDER BY
    AM.heiti ASC,
    month ASC,
    total_kwh DESC;

-- # 2
EXPLAIN ANALYZE
SELECT
    PP.heiti as power_plant_source,
    EXTRACT(YEAR FROM M.timi) AS year,
    EXTRACT(MONTH FROM M.timi) AS month,
    E.heiti as customer_name,
    SUM(M.gildi_kwh) as total_kwh
FROM raforka_updated.uttekt U
JOIN raforka_updated.maelingar M ON M.ID = U.ID
JOIN raforka_updated.stod PP ON PP.ID = M.power_plant_ID
JOIN raforka_updated.eigandi E ON E.ID = U.notandi_id
WHERE
    EXTRACT(YEAR FROM M.timi) = 2025
GROUP BY
    power_plant_source,
    year,
    month,
    customer_name
ORDER BY
    power_plant_source ASC,
    month ASC,
    customer_name ASC;

-- # 3
-- View
CREATE OR REPLACE VIEW raforka_updated.monthly_plant_losses AS
SELECT
    AM.heiti as power_plant_source,
    EXTRACT(YEAR FROM AM.timi) AS year,
    EXTRACT(MONTH FROM AM.timi) AS month,
    SUM(CASE WHEN AM.maeling_type = 'Framleiðsla' THEN AM.gildi_kwh ELSE 0 END) AS total_production,
    SUM(CASE WHEN AM.maeling_type = 'Innmötun' THEN AM.gildi_kwh ELSE 0 END) AS total_substation_input,
    SUM(CASE WHEN AM.maeling_type = 'Úttekt' THEN AM.gildi_kwh ELSE 0 END) AS total_withdrawal
FROM raforka_updated.allar_maelingar AM
GROUP BY
    power_plant_source,
    year,
    month;

-- Query
EXPLAIN ANALYZE
SELECT
    MPL.power_plant_source,
    AVG((MPL.total_production - MPL.total_substation_input)::FLOAT / NULLIF(MPL.total_production, 0)) AS plant_to_substation_loss_ratio,
    AVG((MPL.total_production - MPL.total_withdrawal)::FLOAT / NULLIF(MPL.total_production, 0)) AS total_system_loss_ratio
FROM raforka_updated.monthly_plant_losses MPL
WHERE
    MPL.year = 2025
GROUP BY
    MPL.power_plant_source
ORDER BY
    MPL.power_plant_source;