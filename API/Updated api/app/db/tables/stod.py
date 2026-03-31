from datetime import date
from typing import Optional

from sqlalchemy import (
    DOUBLE_PRECISION,
    Date,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.schema import CheckConstraint

import app.db.tables.eigandi as eigandi
import app.db.tables.maelingar as maelingar
from app.db.base import Base


class Stod(Base):
    __tablename__ = "stod"
    __table_args__ = (CheckConstraint("ID <> tengd_stod_ID", name="check_unique_ids"),)

    ID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    heiti: Mapped[str] = mapped_column(String(100), nullable=False)
    tegund_stod: Mapped[str] = mapped_column(String(100), nullable=False)
    eigandi_ID: Mapped[int] = mapped_column(ForeignKey("eigandi.ID"), nullable=False)
    uppsetning: Mapped[date] = mapped_column(Date, nullable=False)

    x_hnit: Mapped[float] = mapped_column(DOUBLE_PRECISION, nullable=False)
    y_hnit: Mapped[float] = mapped_column(DOUBLE_PRECISION, nullable=False)

    tengd_stod_ID: Mapped[int | None] = mapped_column(ForeignKey("stod.ID"))

    __mapper_args__ = {
        "polymorphic_identity": "stod",
        "polymorphic_on": tegund_stod,
    }

    eigandi: Mapped["eigandi.Eigandi"] = relationship(back_populates="stodvar")
    tengd_stod: Mapped[Optional["Stod"]] = relationship(remote_side=[ID])


class PowerPlant(Stod):
    __tablename__ = "power_plant"

    ID: Mapped[int] = mapped_column(ForeignKey("stod.ID"), primary_key=True)

    maelingar: Mapped[list["maelingar.Maelingar"]] = relationship(
        back_populates="power_plant"
    )

    __mapper_args__ = {
        "polymorphic_identity": "power_plant",
    }


class Substation(Stod):
    __tablename__ = "substation"

    ID: Mapped[int] = mapped_column(ForeignKey("stod.ID"), primary_key=True)

    __mapper_args__ = {
        "polymorphic_identity": "substation",
    }
