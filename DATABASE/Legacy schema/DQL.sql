-- Task A2
--nr 1
SELECT
    eining_heiti AS power_plant_source,
    EXTRACT(YEAR FROM timi) AS year,
    EXTRACT(MONTH FROM timi) AS month,
    tegund_maelingar AS test_measurement_type,
    SUM(gildi_kwh) AS total_kwh
FROM
    raforka_legacy.orku_maelingar
WHERE EXTRACT(YEAR FROM timi) = 2025
GROUP BY
    eining_heiti,
    year,
    month,
    tegund_maelingar
ORDER BY
    eining_heiti,
    month ASC,
    total_kwh DESC;
-- LIMIT 50;
-- Viljum flokka eftir hverri orkuveitu, fyrir hvern mánðuð, samtals orkan frá hverjum flokk

--nr 2
SELECT
    om.eining_heiti AS power_plant_source,
    EXTRACT(YEAR FROM om.timi) AS year,
    EXTRACT(MONTH FROM om.timi) AS month,
    om.notandi_heiti AS customer_name,
    SUM(om.gildi_kwh) AS total_kwh
FROM raforka_legacy.orku_maelingar om
WHERE
    EXTRACT(YEAR FROM om.timi) = 2025
    AND om.tegund_maelingar = 'Úttekt'
    AND om.notandi_heiti IS NOT NULL
GROUP BY
    om.eining_heiti,
    EXTRACT(YEAR FROM om.timi),
    EXTRACT(MONTH FROM om.timi),
    om.notandi_heiti
ORDER BY
    om.eining_heiti ASC,
    month ASC,
    om.notandi_heiti ASC;

--nr 3
CREATE OR REPLACE VIEW raforka_legacy.monthly_plant_losses AS
SELECT
    eining_heiti AS power_plant_source,
    EXTRACT(YEAR FROM timi) AS year,
    EXTRACT(MONTH FROM timi) AS month,
    SUM(CASE WHEN tegund_maelingar = 'Framleiðsla' THEN gildi_kwh ELSE 0 END) AS total_production,
    SUM(CASE WHEN tegund_maelingar = 'Innmötun' THEN gildi_kwh ELSE 0 END) AS total_substation_input,
    SUM(CASE WHEN tegund_maelingar = 'Úttekt' THEN gildi_kwh ELSE 0 END) AS total_withdrawal
FROM raforka_legacy.orku_maelingar
GROUP BY
    eining_heiti,
    EXTRACT(YEAR FROM timi),
    EXTRACT(MONTH FROM timi);
SELECT
    power_plant_source,
    AVG((total_production - total_substation_input)::FLOAT / NULLIF(total_production, 0)) AS plant_to_substation_loss_ratio,
    AVG((total_production - total_withdrawal)::FLOAT / NULLIF(total_production, 0)) AS total_system_loss_ratio
FROM raforka_legacy.monthly_plant_losses
WHERE year = 2025
GROUP BY power_plant_source
ORDER BY power_plant_source;
