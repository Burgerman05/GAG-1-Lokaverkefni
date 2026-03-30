# Task C5
from datetime import datetime

from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.orm import Session

from app.db.session import get_orkuflaedi_session
from app.models.monthly_company_usage_model import MonthlyCompanyUsageModel
from app.models.monthly_energy_flow_model import MonthlyPlantEnergyFlowModel
from app.models.monthly_plant_loss_ratios import MonthlyPlantLossRatiosModel
from app.services.service import (
    OrkuEiningar,
    Maelingar,
    Notandi,
    Stod,
    TegundMaelingar,
    PowerPlantInjection,
    CustomerWithdrawal,
)
from app.utils.validate_date_range import validate_date_range_helper

router = APIRouter()
db_name = "OrkuFlaediIsland"

'''
Endpoint 1: get_monthly_energy_flow()
'''

'''
Endpoint 2: get_monthly_company_usage()
'''

'''
Endpoint 3: get_monthly_plant_loss_ratios()
'''

# Task E1

'''
Endpoint 4: insert_measurements()
'''

# Task F1
'''
Endpoint 5: get_substations_gridflow()
'''