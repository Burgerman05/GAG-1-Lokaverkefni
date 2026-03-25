from datetime import datetime

from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.orm import Session

from app.db.session import get_orkuflaedi_session
from app.models.monthly_company_usage_model import MonthlyCompanyUsageModel
from app.models.monthly_energy_flow_model import MonthlyPlantEnergyFlowModel
from app.models.monthly_plant_loss_ratios import MonthlyPlantLossRatiosModel
from app.services.service import (
    get_monthly_company_usage_data,
    get_monthly_energy_flow_data,
    get_monthly_plant_loss_ratios_data,
    get_notendur_skraning_data,
    get_orku_einingar_data,
    get_orku_maelingar_data,
    insert_test_measurement_data,
)
from app.utils.validate_date_range import validate_date_range_helper

router = APIRouter()
db_name = "OrkuFlaediIsland"

"""
Endpoints already in place
"""


@router.get("/orku_einingar")
def get_orku_einingar(db: Session = Depends(get_orkuflaedi_session)):
    print(f"Calling [GET] /{db_name}/orku_einingar")
    results = get_orku_einingar_data(db)
    return results


@router.get("/skradir_notendur")
def get_notendur_skraning(db: Session = Depends(get_orkuflaedi_session)):
    print(f"Calling [GET] /{db_name}/skradir_notendur")
    results = get_notendur_skraning_data(db)
    return results


@router.get("/maelingar")
def get_orku_maelingar(
    from_date: datetime | None = None,
    to_date: datetime | None = None,
    eining: str | None = None,
    tegund: str | None = None,
    limit: int = 1000,
    offset: int = 0,
    db: Session = Depends(get_orkuflaedi_session),
):
    print(f"Calling [GET] /{db_name}/maelingar")

    from_date, to_date = validate_date_range_helper(
        from_date, to_date, datetime(2025, 1, 1, 0, 0), datetime(2025, 1, 2, 0, 0)
    )

    results = get_orku_maelingar_data(
        from_date, to_date, limit, offset, db, eining, tegund
    )
    return results


@router.post("/test-measurement-data")
async def insert_test_measurement(
    mode: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_orkuflaedi_session),
):
    print(f"Calling [POST] /{db_name}/test-measurement-data")

    result = await insert_test_measurement_data(file, db, mode)
    return result


# Task B2

"""
Endpoint 1: get_monthly_energy_flow()
"""


@router.get("/monthly_energy_flow", response_model=list[MonthlyPlantEnergyFlowModel])
def get_monthly_energy_flow(
    from_date: datetime | None = None,
    to_date: datetime | None = None,
    db: Session = Depends(get_orkuflaedi_session),
):
    print(f"Calling [GET] /{db_name}/monthly_energy_flow")
    from_date, to_date = validate_date_range_helper(
        from_date, to_date, datetime(2025, 1, 1, 0, 0), datetime(2026, 1, 1, 0, 0)
    )

    results = get_monthly_energy_flow_data(from_date, to_date, db)
    return results


"""
Endpoint 2: get_monthly_company_usage()
"""


@router.get("/monthly_company_usage", response_model=list[MonthlyCompanyUsageModel])
def get_monthly_company_usage(
    from_date: datetime | None = None,
    to_date: datetime | None = None,
    db: Session = Depends(get_orkuflaedi_session),
):
    print(f"Calling [GET] /{db_name}/monthly_company_usage")
    from_date, to_date = validate_date_range_helper(
        from_date, to_date, datetime(2025, 1, 1, 0, 0), datetime(2026, 1, 1, 0, 0)
    )

    results = get_monthly_company_usage_data(from_date, to_date, db)
    return results


"""
Endpoint 3: get_monthly_plant_loss_ratios()
"""
