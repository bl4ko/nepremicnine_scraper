# Nepremicnine.net scraper

Simple scraper for [nepremicnine.net](https://www.nepremicnine.net/).

## Usage

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
python scraper.py
```
