"""
Module for parsing and validating the configuration file.
"""

from typing import Any, Dict, Optional, List, get_args, get_origin

import yaml
from constants.constants import ALLOWED_BROKERAGE, ALLOWED_REGIONS, ALLOWED_SUBREGIONS
from url.url import URL


class ConfigValidationError(Exception):
    """Custom exception for configuration validation errors."""


class ConfigParser:
    """
    Class for parsing and validating the configuration file.
    """

    ALLOWED_ATTRIBUTES: Dict[str, Dict[str, Any]] = {
        "nastavitev": {
            "mail_from": str,
            "smtp_server": str,
            "smtp_port": int,
            "mail_to": List[str],
        },
        "poizvedbe": {
            "ime": str,
            "posredovanje": ALLOWED_BROKERAGE,
            "regija": ALLOWED_REGIONS,
            "pod_regija": Optional[str],
            "velikost_od": Optional[int],
            "velikost_do": Optional[int],
            "leto_od": Optional[int],
            "leto_do": Optional[int],
            "m2_od": Optional[int],
            "m2_do": Optional[int],
            "cena_m2_od": Optional[int],
            "cena_m2_do": Optional[int],
        },
    }

    def __init__(self, config_path: str):
        self.config_path = config_path
        self.config: Dict[str, Any] = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        with open(self.config_path, "r", encoding="UTF8") as file:
            return yaml.safe_load(file)

    def _validate_attribute(
        self, section: str, key: str, value: Any, parent_key: Optional[str] = None
    ) -> None:
        if section not in self.ALLOWED_ATTRIBUTES:
            raise ConfigValidationError(f"Unknown configuration section: {section}")

        if key not in self.ALLOWED_ATTRIBUTES[section]:
            raise ConfigValidationError(
                f"Unknown attribute '{key}' in section '{section}'"
            )

        expected_type_or_values = self.ALLOWED_ATTRIBUTES[section][key]

        if get_origin(expected_type_or_values) is list:
            if not all(
                isinstance(v, get_args(expected_type_or_values)[0]) for v in value
            ):
                raise ConfigValidationError(
                    f"Invalid type for '{key}' in section '{section}'. "
                    f"All items must be strings."
                )
        elif isinstance(expected_type_or_values, set):
            if not isinstance(value, str) or value not in expected_type_or_values:
                raise ConfigValidationError(
                    f"Invalid value for '{key}' in section '{section}'. "
                    f"Allowed values are: {expected_type_or_values}"
                )
        elif not isinstance(value, expected_type_or_values):
            raise ConfigValidationError(
                f"Invalid type for '{key}' in section '{section}'. "
                f"Expected type: {expected_type_or_values.__name__}, but got {type(value).__name__}"
            )

        # Special validation for pod_regija based on the selected regija
        if key == "pod_regija" and parent_key:
            allowed_subregions = ALLOWED_SUBREGIONS.get(parent_key, [])
            if value not in allowed_subregions:
                raise ConfigValidationError(
                    f"Invalid value for 'pod_regija' in section '{section}'. "
                    f"Allowed values for regija '{parent_key}' are: {allowed_subregions}"
                )

    def validate(self) -> None:
        """
        Validates the configuration file.
        """
        for section, attributes in self.config.items():
            if section == "poizvedbe":
                if not isinstance(attributes, list):
                    raise ConfigValidationError(
                        f"Expected list for section 'poizvedbe', got {type(attributes).__name__}"
                    )
                for query in attributes:  # attributes is a list here
                    if not isinstance(query, dict):
                        raise ConfigValidationError(
                            f"Expected dictionary for query, got {type(query).__name__}"
                        )
                    regija = query.get("regija")
                    for query_key, query_value in query.items():
                        self._validate_attribute(
                            section,
                            query_key,
                            query_value,
                            regija if query_key == "pod_regija" else None,
                        )
            else:
                if not isinstance(attributes, dict):
                    raise ConfigValidationError(
                        f"Expected dictionary for section '{section}',"
                        f"got {type(attributes).__name__}"
                    )
                for key, value in attributes.items():
                    self._validate_attribute(section, key, value)

    def parse_config(self) -> Dict[str, URL]:
        """
        Parses the configuration file and returns a dictionary of queries.
        """
        self.validate()

        queries: Dict[str, URL] = {}
        poizvedbe = self.config.get("poizvedbe", [])
        if not isinstance(poizvedbe, list):
            raise ConfigValidationError(
                f"Expected list for 'poizvedbe', got {type(poizvedbe).__name__}"
            )

        for query in poizvedbe:
            if not isinstance(query, dict):
                raise ConfigValidationError(
                    f"Expected dictionary for query, got {type(query).__name__}"
                )

            url_instance = URL(
                type_of_offer=query["posredovanje"],
                region=query["regija"],
                type_of_property="stanovanje",
                sub_regions=[query["pod_regija"]] if query.get("pod_regija") else None,
                size_from=query.get("m2_od"),
                size_to=query.get("m2_do"),
                year_from=query.get("leto_od"),
                year_to=query.get("leto_do"),
                price_from_m2=query.get("cena_m2_od"),
                price_to_m2=query.get("cena_m2_do"),
            )
            queries[query["ime"]] = url_instance

        return queries
