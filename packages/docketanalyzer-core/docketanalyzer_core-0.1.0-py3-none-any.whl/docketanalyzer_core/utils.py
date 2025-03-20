from datetime import datetime, date
from typing import Any
from pathlib import Path


BASE_DIR = Path(__file__).parent.parent


def parse_docket_id(docket_id: str) -> tuple[str, str]:
    """Parse a docket ID into a court and docket number."""
    court, docket_number = docket_id.split("__")
    docket_number = docket_number.replace("_", ":")
    return court, docket_number


def construct_docket_id(court: str, docket_number: str) -> str:
    """Construct a docket ID from a court and docket number."""
    formatted_number = docket_number.replace(":", "_")
    return f"{court}__{formatted_number}"


def json_default(obj: Any) -> Any:
    """Default JSON serializer for datetime and date objects."""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")


def notabs(text):
    """Remove leading/trailing whitespace on each line."""
    return "\n".join([x.strip() for x in text.split("\n")]).strip()
