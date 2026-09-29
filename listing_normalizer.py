"""
Public portfolio version of the listing normalization layer
for the Batumi apartment radar.

The goal is to convert apartment listings from different sources
into one common structure before filtering, deduplication,
owner detection, and Telegram delivery.
"""

from dataclasses import dataclass
from typing import Optional
import re


@dataclass
class NormalizedListing:
    source: str
    title: str
    description: str
    price_usd: Optional[float]
    rooms: Optional[int]
    area_m2: Optional[float]
    district: Optional[str]
    url: str


def clean_text(value: str) -> str:
    if not value:
        return ""

    value = value.strip()
    value = re.sub(r"\s+", " ", value)

    return value


def normalize_price(
    raw_price: str,
) -> Optional[float]:

    if not raw_price:
        return None

    cleaned = (
        raw_price
        .replace(",", "")
        .replace(" ", "")
    )

    match = re.search(
        r"(\d+(?:\.\d+)?)",
        cleaned,
    )

    if not match:
        return None

    return float(match.group(1))


def normalize_rooms(
    raw_rooms: str,
) -> Optional[int]:

    if not raw_rooms:
        return None

    match = re.search(
        r"\d+",
        raw_rooms,
    )

    if not match:
        return None

    return int(match.group())


def normalize_area(
    raw_area: str,
) -> Optional[float]:

    if not raw_area:
        return None

    cleaned = raw_area.replace(",", ".")

    match = re.search(
        r"\d+(?:\.\d+)?",
        cleaned,
    )

    if not match:
        return None

    return float(match.group())


def normalize_listing(
    source: str,
    title: str,
    description: str,
    price: str,
    rooms: str,
    area: str,
    district: str,
    url: str,
) -> NormalizedListing:

    return NormalizedListing(
        source=clean_text(source),
        title=clean_text(title),
        description=clean_text(description),
        price_usd=normalize_price(price),
        rooms=normalize_rooms(rooms),
        area_m2=normalize_area(area),
        district=(
            clean_text(district)
            if district
            else None
        ),
        url=clean_text(url),
    )


if __name__ == "__main__":

    example = normalize_listing(
        source="Example Source",
        title="Apartment near Metro City",
        description=(
            "Modern apartment in Batumi. "
            "Owner listing."
        ),
        price="$650",
        rooms="2 rooms",
        area="55 m²",
        district="Airport District",
        url="https://example.com/listing/123",
    )

    print(example)
