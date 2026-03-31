from io import StringIO
from typing import Iterator

import polars as pl

from app.models.parsed_data.old_measurement_data import OldMeasurementData


def parse_old_measurements(csv_str: str) -> Iterator[OldMeasurementData]:
    df = pl.read_csv(StringIO(csv_str))
    for row in df.iter_rows(named=True):
        try:
            yield OldMeasurementData(**row)
        except Exception:
            continue
