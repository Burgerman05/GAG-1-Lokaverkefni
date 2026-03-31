# Task C5
from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import app.services.service as service
from app.db.session import get_orkuflaedi_session
from app.models.monthly_company_usage_model import MonthlyCompanyUsageModel
from app.models.monthly_energy_flow_model import MonthlyPlantEnergyFlowModel
from app.models.monthly_plant_loss_ratios import MonthlyPlantLossRatiosModel
from app.utils.validate_date_range import validate_date_range_helper

router = APIRouter()
db_name = "UpdatedOrkuFlaediIsland"

"""
Endpoint 1: get_monthly_energy_flow()
"""


@router.get("/monthly_energy_flow", response_model=list[MonthlyPlantEnergyFlowModel])
def get_monthly_energy_flow(
    from_date: datetime | None = None,
    to_date: datetime | None = None,
    db: Session = Depends(get_orkuflaedi_session),
) -> list[MonthlyPlantEnergyFlowModel]:
    print(f"Calling [GET] /{db_name}/monthly_energy_flow")
    from_date, to_date = validate_date_range_helper(
        from_date, to_date, datetime(2025, 1, 1, 0, 0), datetime(2026, 1, 1, 0, 0)
    )
    results = service.get_monthly_energy_flow_data(from_date, to_date, db)
    return results


"""
Endpoint 2: get_monthly_company_usage()
"""


@router.get("/monthly_company_usage", response_model=list[MonthlyCompanyUsageModel])
def get_monthly_company_usage(
    from_date: datetime | None = None,
    to_date: datetime | None = None,
    db: Session = Depends(get_orkuflaedi_session),
) -> list[MonthlyCompanyUsageModel]:
    print(f"Calling [GET] /{db_name}/monthly_company_usage")
    from_date, to_date = validate_date_range_helper(
        from_date, to_date, datetime(2025, 1, 1, 0, 0), datetime(2026, 1, 1, 0, 0)
    )
    results = service.get_monthly_company_usage_data(from_date, to_date, db)
    return results


"""
Endpoint 3: get_monthly_plant_loss_ratios()
"""


@router.get(
    "/monthly_plant_loss_ratios", response_model=list[MonthlyPlantLossRatiosModel]
)
def get_monthly_plant_loss_ratios(
    from_date: datetime | None = None,
    to_date: datetime | None = None,
    db: Session = Depends(get_orkuflaedi_session),
) -> list[MonthlyPlantLossRatiosModel]:
    print(f"Calling [GET] /{db_name}/monthly_plant_loss_ratios")
    from_date, to_date = validate_date_range_helper(
        from_date, to_date, datetime(2025, 1, 1, 0, 0), datetime(2026, 1, 1, 0, 0)
    )
    results = service.get_monthly_plant_loss_ratios_data(from_date, to_date, db)
    return results


# Task E1

"""
Endpoint 4: insert_measurements()
"""

# Task F1
"""
Endpoint 5: get_substations_gridflow()
"""
