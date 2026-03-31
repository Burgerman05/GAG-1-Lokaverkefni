from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Index, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

import app.db.tables.stod as stod
from app.db.base import Base


class Maelingar(Base):
    __tablename__ = "maelingar"
    __table_args__ = (Index("idx_maelingar", "timi", "power_plant_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    power_plant_id: Mapped[int] = mapped_column(
        ForeignKey("power_plant.id"), nullable=False
    )
    gildi_kwh: Mapped[Decimal] = mapped_column(Numeric, nullable=False)
    timi: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    maeling_type: Mapped[str] = mapped_column(String(50), nullable=False)

    __mapper_args__ = {
        "polymorphic_on": maeling_type,
        "polymorphic_identity": "maelingar",
    }

    power_plant: Mapped["stod.PowerPlant"] = relationship(back_populates="maelingar")


class Uttekt(Maelingar):
    __tablename__ = "uttekt"

    id: Mapped[int] = mapped_column(ForeignKey("maelingar.id"), primary_key=True)
    sendandi_maelingar: Mapped[int] = mapped_column(
        ForeignKey("substation.id"), nullable=False
    )
    notandi_id: Mapped[int] = mapped_column(ForeignKey("eigandi.id"), nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "uttekt",
    }


class Innmotun(Maelingar):
    __tablename__ = "innmotun"

    id: Mapped[int] = mapped_column(ForeignKey("maelingar.id"), primary_key=True)
    sendandi_maelingar: Mapped[int] = mapped_column(
        ForeignKey("substation.id"), nullable=False
    )

    __mapper_args__ = {
        "polymorphic_identity": "innmotun",
    }


class Framleidsla(Maelingar):
    __tablename__ = "framleidsla"

    id: Mapped[int] = mapped_column(ForeignKey("maelingar.id"), primary_key=True)
    sendandi_maelingar: Mapped[int] = mapped_column(
        ForeignKey("eigandi.id"), nullable=False
    )

    __mapper_args__ = {
        "polymorphic_identity": "framleidsla",
    }
