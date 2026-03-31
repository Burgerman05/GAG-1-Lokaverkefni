from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

import app.db.tables.notendur_skraning as notendur_skraning
import app.db.tables.stod as stod
from app.db.base import Base


class Eigandi(Base):
    __tablename__ = "eigandi"

    ID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    heiti: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    stodvar: Mapped[list[stod.Stod]] = relationship(back_populates="eigandi")
    notendur: Mapped[list[notendur_skraning.NotendurSkraning]] = relationship(
        back_populates="eigandi"
    )
