from datetime import date, datetime
from pathlib import Path
from typing import Any

import requests
from tqdm import tqdm


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
    if isinstance(obj, datetime | date):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")


def notabs(text):
    """Remove leading/trailing whitespace on each line."""
    return "\n".join([x.strip() for x in text.split("\n")]).strip()


def download_file(url, path, description="Downloading"):
    """Download file from URL to local path with progress bar."""
    path = str(path)
    response = requests.get(url, stream=True)
    response.raise_for_status()
    total_size = int(response.headers.get("content-length", 0))

    with (
        Path.open(path, "wb") as file,
        tqdm(
            desc=description,
            total=total_size,
            unit="iB",
            unit_scale=True,
            unit_divisor=1024,
        ) as progress,
    ):
        for data in response.iter_content(chunk_size=1024):
            size = file.write(data)
            progress.update(size)
