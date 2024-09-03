"""
Scraper is responsible for scraping the website and extracting the relevant information.
"""

#!/usr/bin/python

import os
import re
import random
import json
from typing import List, Optional, Set

from dotenv import load_dotenv
from playwright.sync_api import sync_playwright, Page

from constants.objects import ExtractedEntry, ExtractedEntryEncoder
from logger.logger import setup_logger
from config.parser import ConfigParser
from mail_utils.email_generator import create_email_body, send_email

# Load .env file
load_dotenv()

# Set up logging
logger = setup_logger("scraper")
# pylint: disable=W1203


# pylint: disable=too-few-public-methods
class Scraper:
    """
    Scraper class for extracting information from a website.
    """

    def __init__(self, start_url: str):
        self.start_url = start_url

    def _setup_browser(self) -> tuple:
        """
        Sets up and returns a Playwright browser instance.
        """
        playwright = sync_playwright().start()
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        user_agent = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )
        page.set_extra_http_headers({"User-Agent": user_agent})
        return playwright, browser, context, page

    def _accept_cookies(self, page: Page) -> None:
        """
        Accepts cookies if the modal is present.
        """
        try:
            accept_button_selector = "button#CybotCookiebotDialogBodyButtonAccept"
            page.wait_for_selector(accept_button_selector, timeout=5000)
            self._wait_for_timeout(page, 500, 1000)
            page.click(accept_button_selector)
            logger.debug("Accepted cookies.")
        except Exception:  # pylint: disable=broad-except
            logger.debug("No cookies modal found.")

    def _wait_for_timeout(
        self, page: Page, seconds_min: int = 2000, seconds_max: int = 5000
    ) -> None:
        """
        Waits for a random amount of time between `seconds_min` and `seconds_max`.
        """
        seconds = random.randint(seconds_min, seconds_max)
        logger.debug(f"Waiting for {seconds / 1000} seconds before moving on...")
        page.wait_for_timeout(seconds)

    def _fetch_links(self, url: str) -> Set[str]:
        """
        Fetches the page content and extracts all relevant links.
        """
        playwright, browser, _, page = self._setup_browser()
        logger.info(f"Going to page at {url}...")
        page.goto(url, wait_until="networkidle")

        self._accept_cookies(page)
        self._wait_for_timeout(page, 2500, 4500)

        logger.debug("Getting the page content...")
        content = page.content()
        browser.close()
        playwright.stop()

        logger.debug("Extracting entry links from page...")
        links = re.findall(
            r'href="(https://www\.nepremicnine\.net/oglasi-[^/]+/[^/]+-[^/]+_[0-9]+/?)"',
            content,
        )
        return set(links)

    def _fetch_entries(self, links: Set[str]) -> List[ExtractedEntry]:
        """
        Fetches entries from the list of links.
        """
        entries = []
        for link in links:
            playwright, browser, _, page = self._setup_browser()
            logger.info(f"Going to page at [{link}]...")
            page.goto(link, wait_until="networkidle")

            self._accept_cookies(page)
            self._wait_for_timeout(page, 2000, 4000)

            price = self._get_price(page)
            location = self._get_element_text(page, "#opis .kratek strong")
            square_footage = self._get_square_footage(page)
            built_year = self._get_built_year(page)

            page.close()
            browser.close()
            playwright.stop()

            entries.append(
                ExtractedEntry(
                    link=link,
                    price=price,
                    square_footage=square_footage,
                    built_year=built_year,
                    location=location,
                    origin_url=self.start_url,
                )
            )
        return entries

    def _get_element_text(self, page: Page, selector: str) -> str:
        """
        Returns the text content of an element or 'N/A' if not found.
        """
        element = page.query_selector(selector)
        return element.inner_text() if element else "N/A"

    def _get_price(self, page: Page) -> float:
        price_element = page.query_selector(".cena span")

        if not price_element:
            raise ValueError("Price element not found on the page")

        # Get the text content of the first text node (the primary price)
        price_str = price_element.evaluate("el => el.childNodes[0].nodeValue").strip()

        # Clean up the price string
        price_str = price_str.replace("€", "").strip()
        price_str = price_str.replace(".", "").replace(",", ".")

        # Convert to float and round
        price_float = round(float(price_str), 0)
        return price_float

    def _get_square_footage(self, page: Page) -> float:
        """
        Extracts square footage from the page.
        """
        # First attempt: Try to get square footage from the attribute list
        attributes_element = page.query_selector("#atributi")
        if attributes_element:
            for element in attributes_element.query_selector_all("li"):
                if "Velikost" in element.inner_text():
                    square_footage = element.inner_text().split(":")[1].strip()
                    return float(
                        square_footage.replace("m\n2", "")
                        .replace("m2", "")
                        .strip()
                        .replace(",", ".")
                    )

        # Fallback approach: Try to extract square footage from the description
        description_element = page.query_selector("#opis .kratek")
        if description_element:
            description = description_element.inner_text()
            square_footage_match = re.search(r"([0-9]+,[0-9]+) m2", description)
            if square_footage_match:
                # Extract the numeric value before "m2" and return it
                return float(square_footage_match.group(1).replace(",", "."))

        return -1.0

    def _get_built_year(self, page: Page) -> Optional[int]:
        """
        Extracts the built year from the page.
        """
        description_element = page.query_selector("#opis .kratek")
        if description_element:
            description = description_element.inner_text()
            # Update the regex to match "zgrajeno l. <year>"
            built_year_match = re.search(r"zgrajeno l\. (\d{4})", description)
            if built_year_match:
                return int(built_year_match.group(1))
        return None

    def run(self) -> List[ExtractedEntry]:
        """
        Runs the scraper and returns the extracted entries.
        """
        unique_links = self._fetch_links(self.start_url)
        logger.info(f"Found {len(unique_links)} unique links: {unique_links}")
        entries = self._fetch_entries(unique_links)
        return entries


def load_entries_from_file(file_path: str) -> Set[ExtractedEntry]:
    """
    Helper function to load entries from a file.
    """
    with open(file_path, "r", encoding="UTF8") as file:
        entries_data = json.load(file)
        return {ExtractedEntry(**entry) for entry in entries_data}


def main() -> None:
    """
    Main function executed when the script is run.
    """

    # Check if the MAIL_FROM_PASSWORD environment variable is set
    logger.info("Checking if the MAIL_FROM_PASSWORD environment variable is set...")
    mail_from_password = os.getenv("MAIL_FROM_PASSWORD")
    if not mail_from_password:
        logger.error("Please set the MAIL_FROM_PASSWORD environment variable.")
        return

    script_dir = os.path.dirname(os.path.abspath(__file__))
    query_results_path = os.path.join(script_dir, "query_results.json")

    # Read query_results.json if it exists
    logger.info("Reading existing entries from query_results.json if it exists...")
    existing_entries: Set[ExtractedEntry] = set()  # Added type annotation
    if os.path.exists(query_results_path):
        existing_entries = load_entries_from_file(query_results_path)

    # Parse the config file
    logger.info("Parsing the config file...")
    parser = ConfigParser(os.path.join(script_dir, "config.yaml"))
    parsed_config = parser.parse_config()

    # Run the scraper for each query in the config file
    logger.info("Running the scraper for each query in the config file...")
    collected_entries: Set[ExtractedEntry] = set()  # Added type annotation
    for query_name, url in parsed_config.items():
        logger.info("Running scraper for query [%s] on url [%s]", query_name, url)
        scraper = Scraper(str(url))
        entries = scraper.run()
        logger.info(f"Found {len(entries)} entries: ")
        for entry in entries:
            logger.info(entry)
            collected_entries.add(entry)

    # Compare the collected entries with the existing ones
    new_entries = collected_entries - existing_entries
    logger.info(f"Found {len(new_entries)} new entries.")

    # Send an email if there are new entries found
    if new_entries:
        logger.info("Sending mail to %s...", parser.config["nastavitev"]["mail_to"])
        email_body = create_email_body(entries=list(new_entries))
        send_email(
            mail_from=parser.config["nastavitev"]["mail_from"],
            mail_from_password=mail_from_password,
            mail_to=parser.config["nastavitev"]["mail_to"],
            smtp_server=parser.config["nastavitev"]["smtp_server"],
            smtp_port=parser.config["nastavitev"]["smtp_port"],
            body=email_body,
        )

        # Update the query_results.json file with the new entries
        with open(query_results_path, "w", encoding="UTF8") as file:
            json.dump(
                list(collected_entries),
                file,
                cls=ExtractedEntryEncoder,
                indent=4,
                ensure_ascii=False,
            )

    logger.info("My job is finished, exiting now...")


if __name__ == "__main__":
    main()
