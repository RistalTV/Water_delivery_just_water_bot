from datetime import datetime
from typing import Optional


def validate_count(text: str, min: int) -> Optional[int]:
    try:
        count = int(text)
    except (TypeError, ValueError):
        return None

    # if count <= min:
    #     return None
    return count


def validate_date(text: str, ) -> Optional[str]:
    try:
        data = datetime.strptime(text, "%d.%m.%Y")
    except (TypeError, ValueError):
        return None
    return text
