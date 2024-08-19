# Nepremicnine.net scraper

Simple scraper for [nepremicnine.net](https://www.nepremicnine.net/).

## Usage

Clone the repository

```bash
git clone https://github.com/bl4ko/nepremicnine_scraper.git
```

Create an `.env` file in the root of the project

```bash
cp .sample.env .env
vim .env # edit the .env file
```

Create a config file

```bash
cp config.sample.yaml config.yaml
vim config.yaml # edit the config file
```

Run the scraper

```terminal
python -m venv ./venv
source ./venv/bin/activate
pip install -r requirements.txt
playwright install
python scraper.py
```

Set it up as a cron job to run periodically

```bash
crontab -e

# e.g. Add the following line to the crontab file
0 8,14,20 * * * /path/to/venv/bin/python /path/to/scraper.py
```
