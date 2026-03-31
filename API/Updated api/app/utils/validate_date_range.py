from datetime import datetime

from fastapi import HTTPException


def validate_date_range_helper(
    from_date: datetime | None,
    to_date: datetime | None,
    from_date_fallback: datetime,
    to_date_fallback: datetime,
) -> tuple[datetime, datetime]:
    if from_date is None:
        from_date = from_date_fallback

    if to_date is None:
        to_date = to_date_fallback

    if from_date > to_date:
        raise HTTPException(status_code=400, detail="from_date must be before to_date")

    return from_date, to_date
