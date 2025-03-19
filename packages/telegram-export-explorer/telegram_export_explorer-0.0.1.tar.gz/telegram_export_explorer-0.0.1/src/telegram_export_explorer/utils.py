import re
from datetime import UTC, datetime, timedelta, timezone, tzinfo
from typing import Callable
from zoneinfo import ZoneInfo


def parse_date_str(date_str: str) -> str:
    """Parse a timestamp from the export's format to ISO8601

    Example inputs:
      - "12.02.2025 08:37:48 EST"
      - "12.02.2025 08:37:48 UTC-08:00"
    """

    matcher = r"^(?P<day>\d{2})\.(?P<month>\d{2})\.(?P<year>\d{4}) (?P<hour>\d{2}):(?P<minute>\d{2}):(?P<second>\d{2}) (?P<tz>.+)$"

    match = re.match(matcher, date_str)
    if not match:
        raise Exception(f"Failed to extract timestamp from {date_str}")

    year = int(match.group("year"))
    month = int(match.group("month"))
    day = int(match.group("day"))
    hour = int(match.group("hour"))
    minute = int(match.group("minute"))
    second = int(match.group("second"))

    tz: tzinfo
    tz_match = re.match(r"^UTC([+-]\d{2}):\d{2}", match.group("tz"))
    if tz_match:
        hours_offset = int(tz_match.group(1))
        tz = timezone(timedelta(hours=hours_offset))
    else:
        tz = ZoneInfo(match.group("tz"))

    local_datetime = datetime(year, month, day, hour, minute, second, tzinfo=tz)
    utc_datetime = local_datetime.astimezone(UTC)

    return utc_datetime.isoformat()[:18] + "Z"


def text_matches(ptn: str, text: str) -> bool:
    return True if re.compile(ptn).search(text) else False
