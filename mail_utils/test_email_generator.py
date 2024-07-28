# """
# This script is used to test the email_generator module.
# """

# import os
# from dotenv import load_dotenv

# from email_generator import create_email_body, send_email
# from scraper import ExtractedEntry
# from url.url import URL

# load_dotenv()


# url = URL(
#     type_of_offer="prodaja",
#     region="ljubljana-mesto",
#     type_of_property="stanovanje",
#     size_from=50,
#     size_to=100,
#     price_from=100000,
#     price_to=200000,
# )
# entries = [
#     ExtractedEntry(
#         link="https://www.nepremicnine.net/oglasi-prodaja/",
#         origin_url="https://www.nepremicnine.net/oglasi-prodaja/",
#         built_year=2020,
#         location="LJ. BEŽIGRAD, MUCHEJEVA",
#         square_footage=61,
#         price=185000,
#     ),
#     ExtractedEntry(
#         link="https://www.nepremicnine.net/oglasi-prodaja/",
#         location="LJ. BEŽIGRAD, FUŽINE",
#         square_footage=62,
#         price=195000,
#         built_year=2021,
#         origin_url="https://www.nepremicnine.net/oglasi-prodaja/",
#     ),
#     ExtractedEntry(
#         link="https://www.nepremicnine.net/oglasi-prodaja/",
#         location="LJ. BEŽIGRAD, NOVE STOŽICE",
#         square_footage=65,
#         price=199999,
#         built_year=2019,
#         origin_url="https://www.nepremicnine.net/oglasi-prodaja/",
#     ),
# ]

# print(f"Found {len(entries)} entries: {entries}")

# if entries:
#     email_body = create_email_body(entries)
#     send_email(
#         os.environ["MAIL_FROM"],
#         os.environ["MAIL_FROM_PASSWORD"],
#         [os.environ["MAIL_TO"]],
#         os.environ["SMTP_SERVER"],
#         int(os.environ["SMTP_PORT"]),
#         email_body,
#     )
