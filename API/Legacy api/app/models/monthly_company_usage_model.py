from pydantic import BaseModel, ConfigDict


class MonthlyCompanyUsageModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    power_plant_source: str
    customer_name: str
    year: int
    month: int
    total_kwh: float
