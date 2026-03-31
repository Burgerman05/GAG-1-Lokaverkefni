from sqlalchemy import DOUBLE_PRECISION, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

import app.db.tables.eigandi as eigandi
from app.db.base import Base


class NotendurSkraning(Base):
    __tablename__ = "notendur_skraning"

    ID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    heiti: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    kennitala: Mapped[str] = mapped_column(String(10), nullable=False, unique=True)
    eigandi_ID: Mapped[int] = mapped_column(ForeignKey("eigandi.ID"), nullable=False)
    ar_stofnad: Mapped[int] = mapped_column(Integer, nullable=False)

    x_hnit: Mapped[float] = mapped_column(DOUBLE_PRECISION, nullable=False)
    y_hnit: Mapped[float] = mapped_column(DOUBLE_PRECISION, nullable=False)

    eigandi: Mapped[eigandi.Eigandi] = relationship(back_populates="notendur")
