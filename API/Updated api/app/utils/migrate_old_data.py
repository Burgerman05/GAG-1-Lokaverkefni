from typing import Iterator

from sqlalchemy import insert, select
from sqlalchemy.orm import Session

from app.db.tables.eigandi import Eigandi
from app.db.tables.maelingar import Framleidsla, Innmotun, Maelingar, Uttekt
from app.db.tables.stod import Stod
from app.models.parsed_data.old_measurement_data import OldMeasurementData


def insert_single_row(new_data: OldMeasurementData, db: Session) -> bool:
    power_plant_id = db.scalars(
        select(Stod.id).where(Stod.heiti == new_data.eining_heiti)
    ).first()

    if power_plant_id is None:
        return False

    result = db.execute(
        insert(Maelingar)
        .values(
            power_plant_id=power_plant_id,
            timi=new_data.timi,
            gildi_kwh=new_data.gildi_kwh,
            maeling_type=new_data.tegund_maelingar,
        )
        .returning(Maelingar.id)
    ).fetchone()

    if result is None:
        db.rollback()
        return False

    maeling_id = result.tuple()[0]

    match new_data.tegund_maelingar:
        case "Úttekt":
            if new_data.notandi_heiti is None:
                return False

            notandi_id = db.scalars(
                select(Eigandi.id).where(Eigandi.heiti == new_data.notandi_heiti)
            ).first()

            if notandi_id is None:
                return False

            sendandi_id = db.scalars(
                select(Stod.id).where(Stod.heiti == new_data.sendandi_maelingar)
            ).first()

            if sendandi_id is None:
                return False

            db.execute(
                insert(Uttekt).values(
                    id=maeling_id,
                    sendandi_maelingar=sendandi_id,
                    notandi_id=notandi_id,
                )
            )
        case "Innmötun":
            sendandi_id = db.scalars(
                select(Stod.id).where(Stod.heiti == new_data.sendandi_maelingar)
            ).first()

            if sendandi_id is None:
                return False

            db.execute(
                insert(Innmotun).values(id=maeling_id, sendandi_maelingar=sendandi_id)
            )
        case "Framleiðsla":
            sendandi_id = db.scalars(
                select(Eigandi.id).where(Eigandi.heiti == new_data.sendandi_maelingar)
            ).first()
            if sendandi_id is None:
                return False

            db.execute(
                insert(Framleidsla).values(
                    id=maeling_id, sendandi_maelingar=sendandi_id
                )
            )
        case _:
            return False

    return True


def insert_rows(data: Iterator[OldMeasurementData], db: Session) -> int:
    processed = 0
    for row in data:
        try:
            insert_single_row(row, db)
            processed += 1
        except Exception:
            db.rollback()
            continue

    return processed
