# Nepremicnine.net scraper

Simple scraper for [nepremicnine.net](https://www.nepremicnine.net/).

## Usage

* Clone the repository

```bash
git clone https://github.com/bl4ko/nepremicnine_scraper.git
```

* Create an `.env` file in the root of the project

```bash
cp .sample.env .env
vim .env # edit the .env file
```

* Create a config file (see [config section](#configyaml))

```bash
cp config.sample.yaml config.yaml
vim config.yaml # edit the config file
```

* Run the scraper

```terminal
python -m venv ./venv
source ./venv/bin/activate
pip install -r requirements.txt
playwright install
python scraper.py
```

* Optionally: Set it up as a cron job to run periodically

```bash
crontab -e

# e.g. Add the following line to the crontab file
0 6,13,20 * * * /path/to/venv/bin/python /path/to/scraper.py
```

## Config.yaml

Example config can be found at [`config.sample.yaml`](./config.sample.yaml).

| Key                      | Description                                                                                                                                                              | Required |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------- |
| nastavitev.mail_from     | Email address from which the email will be sent                                                                                                                          | true     |
| nastavitev.smtp_server   | SMTP server for sending the email                                                                                                                                        | true     |
| nastavitev.smtp_port     | SMTP port for sending the email                                                                                                                                          | true     |
| nastavitev.mail_to       | List of email addresses to send the email to                                                                                                                             | true     |
| poizvedbe                | List of search queries                                                                                                                                                   | true     |
| poizvedbe[].ime          | Name of the search query                                                                                                                                                 | true     |
| poizvedbe[].posredovanje | Type of the property (prodaja, oddaja, nakup, najem)                                                                                                                     | true     |
| poizvedbe[].regija       | Region of the property (ljubljana-mesto, ljubljana-okolica, juzna-primorska, severna-primorska, notranjska, savinska, gorenjska, koroska, podravska, posavska, pomurska) | true     |
| poizvedbe[].pod_regija   | Subregion of the property (e.g. "ljubljana-bezigrad" for ljubljana-mesto)                                                                                                | false    |
| poizvedbe[].m2_od        | Minimum size of the property in m^2                                                                                                                                      | false    |
| poizvedbe[].m2_do        | Maximum size of the property in m^2                                                                                                                                      | false    |
| poizvedbe[].leto_od      | Minimum year of construction                                                                                                                                             | false    |
| poizvedbe[].leto_do      | Maximum year of construction                                                                                                                                             | false    |
| poizvedbe[].cena_od      | Minimum price of the property                                                                                                                                            | false    |
| poizvedbe[].cena_do      | Maximum price of the property                                                                                                                                            | false    |
| poizvedbe[].cena_od_m2   | Minimum price per m^2                                                                                                                                                    | false    |
| poizvedbe[].cena_do_m2   | Maximum price per m^2                                                                                                                                                    | false    |
