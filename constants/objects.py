"""
This module contains the types used in the project.
"""

import json
from typing import Optional, Any, Dict


class ExtractedEntryEncoder(json.JSONEncoder):
    """
    JSON encoder for the ExtractedEntry class.
    """

    def default(self, o: Any) -> Any:
        if isinstance(o, ExtractedEntry):
            return o.to_dict()
        return super().default(o)


class ExtractedEntry:
    """
    ExtractedEntry represents a single entry extracted from the website.
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        location: str,
        square_footage: float,
        price: float,
        link: str,
        origin_url: str,
        built_year: Optional[int] = None,
        price_per_m2: Optional[int] = None,
    ):
        self.location: str = location
        self.square_footage: float = square_footage
        self.price: float = price
        self.link: str = link
        self.built_year: Optional[int] = built_year
        self.origin_url: str = origin_url
        self.price_per_m2: int = (
            int(round(price / (square_footage * 0.95), 0))
            if price_per_m2 is None
            else price_per_m2
        )

    def __str__(self) -> str:
        return (
            f"ExtractedEntry{{link: {self.link}, Location: {self.location},"
            f"Square Footage: {self.square_footage}, Price: {self.price}}},"
            f"Built Year: {self.built_year}, Price per m2: {self.price_per_m2}"
        )

    def __repr__(self) -> str:
        return self.__str__()

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the ExtractedEntry to a dictionary.
        """
        return {
            "location": self.location,
            "square_footage": self.square_footage,
            "price": self.price,
            "link": self.link,
            "built_year": self.built_year,
            "origin_url": self.origin_url,
            "price_per_m2": self.price_per_m2,
        }

    def __hash__(self) -> int:
        return hash(
            (
                self.link,
                self.location,
                self.square_footage,
                self.price,
                self.built_year,
                self.origin_url,
            )
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ExtractedEntry):
            return False
        return (
            self.link == other.link
            and self.location == other.location
            and self.square_footage == other.square_footage
            and self.price == other.price
            and self.built_year == other.built_year
            and self.origin_url == other.origin_url
        )
