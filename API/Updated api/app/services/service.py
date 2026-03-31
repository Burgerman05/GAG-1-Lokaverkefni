# Task C5

from datetime import datetime

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.models.monthly_company_usage_model import MonthlyCompanyUsageModel
from app.models.monthly_energy_flow_model import MonthlyPlantEnergyFlowModel
from app.models.monthly_plant_loss_ratios import MonthlyPlantLossRatiosModel

"""
Service 1: get_monthly_energy_flow_data()
"""


def get_monthly_energy_flow_data(
    from_date: datetime, to_date: datetime, db: Session
) -> list[MonthlyPlantEnergyFlowModel]:
    sql = text("""
SELECT
    AM.heiti as power_plant_source,
    EXTRACT(YEAR FROM AM.timi) as year,
    EXTRACT(MONTH FROM AM.timi) as month,
    AM.maeling_type as measurement_type,
    SUM(AM.gildi_kwh) as total_kwh
FROM raforka_updated.allar_maelingar AM
WHERE
    AM.timi BETWEEN :from_date AND :to_date
GROUP BY
    AM.heiti,
    year,
    month,
    AM.maeling_type
ORDER BY
    AM.heiti ASC,
    month ASC,
    total_kwh DESC;
""")

    results = (
        db.execute(sql, {"from_date": from_date, "to_date": to_date}).mappings().all()
    )
    return [MonthlyPlantEnergyFlowModel.model_validate(row) for row in results]


"""
Service 2: get_monthly_company_usage_data()
"""


def get_monthly_company_usage_data(
    from_date: datetime, to_date: datetime, db: Session
) -> list[MonthlyCompanyUsageModel]:
    sql = text("""
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
    M.timi BETWEEN :from_date AND :to_date
GROUP BY
    power_plant_source,
    year,
    month,
    customer_name
ORDER BY
    power_plant_source ASC,
    month ASC,
    customer_name ASC;
""")

    results = (
        db.execute(sql, {"from_date": from_date, "to_date": to_date}).mappings().all()
    )
    return [MonthlyCompanyUsageModel.model_validate(row) for row in results]


"""
Service 3: get_monthly_plant_loss_ratios_data()
"""


def get_monthly_plant_loss_ratios_data(
    from_date: datetime, to_date: datetime, db: Session
) -> list[MonthlyPlantLossRatiosModel]:
    sql = text("""
SELECT
    MPL.power_plant_source,
    AVG((MPL.total_production - MPL.total_substation_input)::FLOAT / NULLIF(MPL.total_production, 0)) AS plant_to_substation_loss_ratio,
    AVG((MPL.total_production - MPL.total_withdrawal)::FLOAT / NULLIF(MPL.total_production, 0)) AS total_system_loss_ratio
FROM raforka_updated.monthly_plant_losses MPL
WHERE
    MPL.year BETWEEN EXTRACT(YEAR FROM :from_date) AND EXTRACT(YEAR FROM :to_date)
GROUP BY
    MPL.power_plant_source
ORDER BY
    MPL.power_plant_source;
""")

    results = (
        db.execute(sql, {"from_date": from_date, "to_date": to_date}).mappings().all()
    )
    return [MonthlyPlantLossRatiosModel.model_validate(row) for row in results]


# Task E1

"""
Service 4: insert_measurements_data()
"""

# Task F1

"""
Service 5: get_substations_gridflow_data()
"""
