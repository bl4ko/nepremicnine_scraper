"""
Module for building the URL for the scraper
"""

# mypy: ignore-errors

from typing import List, Tuple
from constants.constants import (
    ALLOWED_BROKERAGE,
    ALLOWED_REGIONS,
    ALLOWED_PROPERTY_TYPES,
    ALLOWED_SUBREGIONS,
)


# pylint: disable=too-many-instance-attributes, too-many-arguments, too-few-public-methods
class URL:
    """
    URL class for building the URL for the scraper
    """

    def __init__(
        self,
        type_of_offer: str,
        region: str,
        type_of_property: str,
        sub_regions: List[str] | None = None,
        size_from: int | None = None,
        size_to: int | None = None,
        year_from: int | None = None,
        year_to: int | None = None,
        price_from: int | None = None,
        price_to: int | None = None,
        price_from_m2: int | None = None,
        price_to_m2: int | None = None,
    ):
        # ------ Required parameters validation -------------------
        self.type_of_offer = self._validate_option(
            type_of_offer, ALLOWED_BROKERAGE, "type_of_offer"
        )
        self.region = self._validate_option(region, ALLOWED_REGIONS, "region")
        self.type_of_property = self._validate_option(
            type_of_property, ALLOWED_PROPERTY_TYPES, "type_of_property"
        )

        # ------ Optional parameters validation -------------------
        if sub_regions is not None:
            for sub_region in sub_regions:
                self.sub_regions = self._validate_option(
                    sub_region, ALLOWED_SUBREGIONS[self.region], "sub_regions"
                )

        self._validate_range(size_from, size_to, "velikost_od", "velikost_do")
        self._validate_range(price_from, price_to, "cena_od", "cena_do")
        self._validate_range(price_from_m2, price_to_m2, "cena_od_m2", "cena_do_m2")
        self._validate_range(year_from, year_to, "letnik_od", "letnik_do")
        self._validate_price_conflicts(price_from, price_from_m2, price_to, price_to_m2)

        self.sub_regions = sub_regions
        self.price_from = price_from
        self.price_to = price_to
        self.size_from = size_from
        self.size_to = size_to
        self.price_from_m2 = price_from_m2
        self.price_to_m2 = price_to_m2
        self.year_from = year_from
        self.year_to = year_to

    def _validate_option(self, value, allowed_values, field_name):
        if value not in allowed_values:
            raise ValueError(
                f"Invalid value for {field_name}. Allowed values are: {allowed_values}"
            )
        return value

    def _validate_range(self, min_value, max_value, min_field_name, max_field_name):
        if min_value is not None and max_value is not None and min_value > max_value:
            raise ValueError(
                f"{min_field_name} must be less than or equal to {max_field_name}"
            )
        if min_value is not None and min_value < 0:
            raise ValueError(f"{min_field_name} must be a positive integer")

    def _validate_price_conflicts(self, cena_od, cena_od_m2, cena_do, cena_do_m2):
        if (cena_od is not None and cena_od_m2 is not None) or (
            cena_do is not None and cena_do_m2 is not None
        ):
            raise ValueError(
                "cena_od and cena_od_m2 (or cena_do and cena_do_m2) cannot be used at the same time"
            )

    def _build_base_url(self):
        if self.sub_regions is not None:
            sub_regions_str = ",".join(self.sub_regions)
            return (
                f"https://www.nepremicnine.net/oglasi-{self.type_of_offer}/{self.region}/"
                f"{sub_regions_str}/{self.type_of_property}"
            )

        return (
            f"https://www.nepremicnine.net/oglasi-{self.type_of_offer}"
            f"/{self.region}/{self.type_of_property}"
        )

    # pylint: disable=too-many-return-statements
    def _add_price_to_url(self, base_url) -> Tuple[str, bool]:
        """
        Add price range to the URL.
        """
        if self.price_from is not None and self.price_to is not None:
            return f"{base_url}/cena-od-{self.price_from}-do-{self.price_to}-eur", True
        if self.price_from is not None:
            return f"{base_url}/cena-od-{self.price_from}-eur", True
        if self.price_to is not None:
            return f"{base_url}/cena-do-{self.price_to}-eur", True
        if self.price_from_m2 is not None and self.price_to_m2 is not None:
            return (
                f"{base_url}/cena-od-{self.price_from_m2}-do-{self.price_to_m2}-eur-na-m2",
                True,
            )
        if self.price_from_m2 is not None:
            return f"{base_url}/cena-od-{self.price_from_m2}-eur-na-m2", True
        if self.price_to_m2 is not None:
            return f"{base_url}/cena-do-{self.price_to_m2}-eur-na-m2", True
        return base_url, False

    def _add_size_to_url(self, base_url, separator) -> Tuple[str, bool]:
        """
        Add size range to the URL.
        """
        if self.size_from is not None and self.size_to is not None:
            return (
                f"{base_url}{separator}velikost-od-{self.size_from}-do-{self.size_to}-m2",
                True,
            )
        if self.size_from is not None:
            return f"{base_url}{separator}velikost-od-{self.size_from}-m2", True
        if self.size_to is not None:
            return f"{base_url}{separator}velikost-do-{self.size_to}-m2", True
        return base_url, False

    def _add_year_to_url(self, base_url, separator) -> Tuple[str, bool]:
        if self.year_from is not None and self.year_to is not None:
            return (
                f"{base_url}{separator}letnik-od-{self.year_from}-do-{self.year_to}",
                True,
            )
        if self.year_from is not None:
            return f"{base_url}{separator}letnik-od-{self.year_from}", True
        if self.year_to is not None:
            return f"{base_url}{separator}letnik-do-{self.year_to}", True
        return base_url, False

    def __str__(self):
        base_url = self._build_base_url()

        base_url, cena_set = self._add_price_to_url(base_url)

        separator = "," if cena_set else "/"
        base_url, size_set = self._add_size_to_url(base_url, separator)

        separator = "," if cena_set or size_set else "/"
        base_url, _ = self._add_year_to_url(base_url, separator)

        return f"{base_url}/"
