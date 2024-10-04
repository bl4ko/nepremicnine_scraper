"""
Module for sending emails with the results of the scraping.
"""

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import ssl
from typing import List

from constants.objects import ExtractedEntry


def create_email_body(entries: List[ExtractedEntry]) -> MIMEMultipart:
    """
    Creates the email body with the given parameters.
    """
    body = MIMEMultipart("alternative")
    html_body = """<html>
    <head>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 20px;
                color: #333;
            }
            h1 {
                color: #0073e6;
            }
            h2 {
                color: #333;
                margin-top: 20px;
                border-bottom: 2px solid #0073e6;
                padding-bottom: 10px;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
            }
            th, td {
                border: 1px solid #ddd;
                padding: 12px;
                text-align: left;
            }
            th {
                background-color: #f4f4f4;
                color: #333;
            }
            tr:nth-child(even) {
                background-color: #f9f9f9;
            }
            tr:hover {
                background-color: #f1f1f1;
            }
            a {
                color: #0073e6;
                text-decoration: none;
            }
            a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <h1>Za vašo poizvedbo je prišlo do sprememb!</h1>"""

    html_body += """
        <h2>Najdene nepremičnine:</h2>
        <table>
            <tr>
                <th>Link</th>
                <th>Lokacija</th>
                <th>Leto izgradnje</th>
                <th>Velikost</th>
                <th>Cena</th>
                <th>Cena/m2 (*0.95)</th>
                <th>Avtor</th>
            </tr>"""

    for entry in entries:
        price_formatted = f"{int(round(entry.price, 0)):,}".replace(",", ".")
        price_per_m2_formatted = f"{entry.price_per_m2:,}".replace(",", ".")

        html_body += f"""
            <tr>
                <td><a href="{entry.link}">{entry.link}</a></td>
                <td>{entry.location}</td>
                <td>{entry.built_year}</td>
                <td>{entry.square_footage} m2</td>
                <td>{price_formatted} €</td>
                <td>{price_per_m2_formatted} €/m2</td>
                <td>{entry.author}</td>
            </tr>
        """

    html_body += """
        </table>
    </body>
    </html>"""

    body.attach(MIMEText(html_body, "html"))
    return body


# pylint: disable=too-many-arguments
def send_email(
    mail_from: str,
    mail_from_password: str,
    mail_to: List[str],  # Updated to accept a list of strings
    smtp_server: str,
    smtp_port: int,
    body: MIMEMultipart,
) -> None:
    """
    Sends an email with the given parameters.
    """
    message = MIMEMultipart("related")
    message["Subject"] = "Najdene nepremičnine"
    message["From"] = mail_from
    message["To"] = ", ".join(mail_to)  # Join list into a comma-separated string

    message.attach(body)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
        server.login(mail_from, mail_from_password)
        server.sendmail(
            mail_from, mail_to, message.as_string()
        )  # Pass the list directly
