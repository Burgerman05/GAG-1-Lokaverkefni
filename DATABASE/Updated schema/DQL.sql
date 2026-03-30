-- Task C5
--1
SELECT
    O.heiti AS power_plante,
    EXTRACT(YEAR from M.timi) AS YEAR,
    EXTRACT(MONTH from M.timi) AS MONTH,
    T.tegund AS test_mesurement,
    SUM(M.gildi_kwh) AS total_kwh
FROM mælingar M
JOIN orku_einingar O ON M.orku_eining_id = O.id
JOIN tegund_mælingar T ON M.tegund_mælingar_id = T.id
WHERE EXTRACT(YEAR FROM M.timi) = 2025
GROUP BY
    O.heiti,
    year,
    month,
    T.tegund,
	M.gildi_kwh
ORDER BY
    O.heiti,
    month ASC,
    M.gildi_kwh DESC;

--2
SELECT
    O.heiti AS power_plant_source,
    EXTRACT(YEAR FROM M.timi) AS year,
    EXTRACT(MONTH FROM M.timi) AS month,
    N.notandi_heiti AS Name_of_customer,
    SUM(M.gildi_kwh) AS total_kwh
FROM mælingar M
JOIN orku_einingar O ON M.orku_eining_id = O.id
JOIN tegund_mælingar T ON M.tegund_mælingar_id = T.id
LEFT JOIN notandi N ON M.notandi_id = N.id
WHERE
    EXTRACT(YEAR FROM M.timi) = 2025
    AND T.tegund = 'Úttekt'
    AND N.notandi_heiti IS NOT NULL
GROUP BY
    O.heiti,
    year,
    month,
    N.notandi_heiti
ORDER BY
    O.heiti ASC,
    month ASC,
    N.notandi_heiti ASC;

--3

CREATE OR REPLACE VIEW monthly_plant_losses AS
SELECT
    O.heiti AS power_plant_source,
    EXTRACT(YEAR FROM M.timi) AS year,
    EXTRACT(MONTH FROM M.timi) AS month,
    SUM(CASE WHEN T.tegund = 'Framleiðsla' THEN M.gildi_kwh ELSE 0 END) AS total_production,
    SUM(CASE WHEN T.tegund = 'Innmötun' THEN M.gildi_kwh ELSE 0 END) AS total_substation_input,
    SUM(CASE WHEN T.tegund = 'Úttekt' THEN M.gildi_kwh ELSE 0 END) AS total_withdrawal
FROM mælingar M
JOIN orku_einingar O ON M.orku_eining_id = O.id
JOIN tegund_mælingar T ON M.tegund_mælingar_id = T.id

GROUP BY
    O.heiti,
    year,
    month;
SELECT --frá Enok breitti bara FROM?
    power_plant_source,
    AVG((total_production - total_substation_input)::FLOAT / NULLIF(total_production, 0)) AS plant_to_substation_loss_ratio,
    AVG((total_production - total_withdrawal)::FLOAT / NULLIF(total_production, 0)) AS total_system_loss_ratio
FROM monthly_plant_losses
WHERE year = 2025
GROUP BY power_plant_source
ORDER BY power_plant_source;
