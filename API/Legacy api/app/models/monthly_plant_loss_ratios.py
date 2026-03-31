from pydantic import BaseModel, ConfigDict


class MonthlyPlantLossRatiosModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    power_plant_source: str
    plant_to_substation_loss_ratio: float
    total_system_loss_ratio: float
