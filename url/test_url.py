"""
This module contains tests for the URL class.
"""

import unittest
from .url import URL


class TestURL(unittest.TestCase):
    """
    Test class for the URL class.
    """

    def test_valid_url_creation(self) -> None:
        """
        Test if the URL is created correctly.
        """
        url = URL(
            type_of_offer="prodaja",
            region="ljubljana-mesto",
            type_of_property="stanovanje",
            size_from=50,
            size_to=100,
            price_from=100000,
            price_to=200000,
        )
        expected_url = (
            "https://www.nepremicnine.net/oglasi-prodaja/ljubljana-mesto/stanovanje"
            "/cena-od-100000-do-200000-eur,velikost-od-50-do-100-m2/"
        )
        self.assertEqual(str(url), expected_url)

    def test_valid_url_creation2(self) -> None:
        """
        Test if the URL is created correctly.
        """
        url = URL(
            type_of_offer="prodaja",
            region="ljubljana-mesto",
            sub_regions=["ljubljana-siska"],
            type_of_property="stanovanje",
            year_from=1950,
            year_to=1999,
            size_to=40,
            price_to_m2=3800,
        )

        expected_url = (
            "https://www.nepremicnine.net/oglasi-prodaja/ljubljana-mesto/ljubljana-siska/"
            "stanovanje/cena-do-3800-eur-na-m2,velikost-do-40-m2,letnik-od-1950-do-1999/"
        )

        self.assertEqual(str(url), expected_url)

    def test_valid_url_creation3(self) -> None:
        """
        Test if the URL is created correctly.
        """
        url = URL(
            type_of_offer="prodaja",
            region="ljubljana-mesto",
            sub_regions=["ljubljana-bezigrad"],
            type_of_property="stanovanje",
            year_from=2000,
            size_from=40,
            size_to=70,
            price_to_m2=4300,
        )

        expected_url = (
            "https://www.nepremicnine.net/oglasi-prodaja/ljubljana-mesto/ljubljana-bezigrad/"
            "stanovanje/cena-do-4300-eur-na-m2,velikost-od-40-do-70-m2,letnik-od-2000/"
        )

        self.assertEqual(str(url), expected_url)

    def test_valid_url_creation4(self) -> None:
        """
        Test if the URL is created correctly
        """
        url = URL(
            type_of_offer="prodaja",
            region="ljubljana-mesto",
            sub_regions=["ljubljana-siska"],
            type_of_property="stanovanje",
            year_from=1950,
            year_to=1999,
            size_from=40,
            size_to=70,
            price_to_m2=3600,
        )

        expected_url = (
            "https://www.nepremicnine.net/oglasi-prodaja/ljubljana-mesto/ljubljana-siska/"
            "stanovanje/cena-do-3600-eur-na-m2,velikost-od-40-do-70-m2,letnik-od-1950-do-1999/"
        )

        self.assertEqual(str(url), expected_url)

    def test_invalid_posredovanje(self) -> None:
        """
        Test if an error is raised when an invalid value is
        passed to the type_of_offer parameter.
        """
        with self.assertRaises(ValueError) as context:
            URL(
                type_of_offer="invalid",
                region="ljubljana-mesto",
                type_of_property="stanovanje",
            )
        self.assertTrue("Invalid value for type_of_offer" in str(context.exception))

    def test_invalid_regija(self) -> None:
        """
        Test if an error is raised when an invalid value is
        passed to the region parameter.
        """
        with self.assertRaises(ValueError) as context:
            URL(
                type_of_offer="prodaja", region="invalid", type_of_property="stanovanje"
            )
        self.assertTrue("Invalid value for region" in str(context.exception))

    def test_invalid_property_type(self) -> None:
        """
        Test if an error is raised when an invalid value is
        passed to the type_of_property parameter.
        """
        with self.assertRaises(ValueError) as context:
            URL(
                type_of_offer="prodaja",
                region="ljubljana-mesto",
                type_of_property="invalid",
            )
        self.assertTrue("Invalid value for type_of_property" in str(context.exception))

    def test_velikost_od_greater_than_velikost_do(self) -> None:
        """
        Test if an error is raised when velikost_od is greater than velikost_do.
        """
        with self.assertRaises(ValueError) as context:
            URL(
                type_of_offer="prodaja",
                region="ljubljana-mesto",
                type_of_property="stanovanje",
                size_from=100,
                size_to=50,
            )
        self.assertTrue(
            "velikost_od must be less than or equal to velikost_do"
            in str(context.exception)
        )

    def test_negative_velikost_od(self) -> None:
        """
        Test if an error is raised when velikost_od is negative.
        """
        with self.assertRaises(ValueError) as context:
            URL(
                type_of_offer="prodaja",
                region="ljubljana-mesto",
                type_of_property="stanovanje",
                size_from=-10,
            )
        self.assertTrue(
            "velikost_od must be a positive integer" in str(context.exception)
        )

    def test_cena_od_greater_than_cena_do(self) -> None:
        """
        Test if an error is raised when price_from is greater than
        price_to.
        """
        with self.assertRaises(ValueError) as context:
            URL(
                type_of_offer="prodaja",
                region="ljubljana-mesto",
                type_of_property="stanovanje",
                price_from=200000,
                price_to=100000,
            )
        self.assertTrue(
            "cena_od must be less than or equal to cena_do" in str(context.exception)
        )

    def test_negative_cena_od(self) -> None:
        """
        Test if an error is raised when price_from is negative
        """
        with self.assertRaises(ValueError) as context:
            URL(
                type_of_offer="prodaja",
                region="ljubljana-mesto",
                type_of_property="stanovanje",
                price_from=-100000,
            )
        self.assertTrue("cena_od must be a positive integer" in str(context.exception))

    def test_cena_od_m2_greater_than_cena_do_m2(self) -> None:
        """
        Test if an error is raised when price_from_m2 is greater than
        price_to_m2.
        """
        with self.assertRaises(ValueError) as context:
            URL(
                type_of_offer="prodaja",
                region="ljubljana-mesto",
                type_of_property="stanovanje",
                price_from_m2=2000,
                price_to_m2=1000,
            )
        self.assertTrue(
            "cena_od_m2 must be less than or equal to cena_do_m2"
            in str(context.exception)
        )

    def test_cena_od_and_cena_od_m2_together(self) -> None:
        """
        Test if an error is raised when price_from and price_from_m2.
        """
        with self.assertRaises(ValueError) as context:
            URL(
                type_of_offer="prodaja",
                region="ljubljana-mesto",
                type_of_property="stanovanje",
                price_from=100000,
                price_from_m2=1000,
            )
        self.assertTrue(
            "cena_od and cena_od_m2 (or cena_do and cena_do_m2) cannot be used at the same time"
            in str(context.exception)
        )

    def test_valid_url_with_only_mandatory_parameters(self) -> None:
        """
        Test if the URL is created correctly with only mandatory parameters.
        """
        url = URL(
            type_of_offer="prodaja",
            region="ljubljana-mesto",
            type_of_property="stanovanje",
        )
        expected_url = (
            "https://www.nepremicnine.net/oglasi-prodaja/ljubljana-mesto/stanovanje/"
        )
        self.assertEqual(str(url), expected_url)

    def test_valid_url_with_size_and_price_m2(self) -> None:
        """
        Test if the URL is created correctly with size and price per m2.
        """
        url = URL(
            type_of_offer="prodaja",
            region="ljubljana-mesto",
            type_of_property="stanovanje",
            size_from=50,
            size_to=100,
            price_from_m2=1500,
            price_to_m2=2000,
        )
        expected_url = (
            "https://www.nepremicnine.net/oglasi-prodaja/ljubljana-mesto/"
            "stanovanje/cena-od-1500-do-2000-eur-na-m2,velikost-od-50-do-100-m2/"
        )

        self.assertEqual(str(url), expected_url)

    def test_valid_url_with_single_size(self) -> None:
        """
        Test if the URL is created correctly with only size_from.
        """
        url = URL(
            type_of_offer="prodaja",
            region="ljubljana-mesto",
            type_of_property="stanovanje",
            size_to=100,
        )
        expected_url = (
            "https://www.nepremicnine.net/oglasi-prodaja/"
            "ljubljana-mesto/stanovanje/velikost-do-100-m2/"
        )
        self.assertEqual(str(url), expected_url)

    def test_valid_url_with_single_price(self) -> None:
        """
        Test if the URL is created correctly with only price_from.
        """
        url = URL(
            type_of_offer="prodaja",
            region="ljubljana-mesto",
            type_of_property="stanovanje",
            price_from=100000,
        )
        expected_url = (
            "https://www.nepremicnine.net/oglasi-prodaja/"
            "ljubljana-mesto/stanovanje/cena-od-100000-eur/"
        )
        self.assertEqual(str(url), expected_url)


if __name__ == "__main__":
    unittest.main()
