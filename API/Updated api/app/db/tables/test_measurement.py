from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class TestMeasurement(Base):
    __tablename__ = "test_measurement"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    timi: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    value: Mapped[Decimal | None] = mapped_column(Numeric)
