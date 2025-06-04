# ORE OSINT Toolkit

This module collects open-source intelligence (OSINT) for the Nineveh Plains and wider Iraq region.

## Features

- **News scraping** via RSS feeds and free OSINT APIs (GDELT, NewsAPI, OSINT Combine)
- **Social media scraping** using [snscrape](https://github.com/JustAnotherArchivist/snscrape) or Twitter public API
- **Satellite imagery metadata** from Sentinel, NASA, OpenAerialMap, and OpenStreetMap tiles
- **Weather data** via Open-Meteo, NOAA and Visual Crossing
- **Geocoding** using Nominatim and MapQuest Open
- **Secure messaging** helpers for Matrix and Signal (via signal-cli)
- **Storage** in a local SQLite database
- **Search and export** of collected intel to CSV or PDF
- **Interactive map** generation using Leaflet (via `folium`)
- **PGP encryption utilities** for securing sensitive notes and files

## Usage

Install dependencies:

```bash
pip install -r requirements.txt
```

Example commands:

```bash
# News and social media
python -m ORE.osint.cli fetch-news
python -m ORE.osint.cli scrape-twitter "Nineveh" --limit 20
python -m ORE.osint.cli twitter-api "Nineveh" YOUR_TOKEN

# Satellite imagery
python -m ORE.osint.cli fetch-satellite "Nineveh Plains"
python -m ORE.osint.cli fetch-nasa 36.27 43.38 DEMO_KEY
python -m ORE.osint.cli fetch-oam "43.0,36.0,44.0,37.0"

# Weather data
python -m ORE.osint.cli weather-open 36.27 43.38
python -m ORE.osint.cli weather-noaa OTX 72 120
python -m ORE.osint.cli weather-vc "Iraq" YOUR_KEY

# Geocoding
python -m ORE.osint.cli geocode "Mosul"
python -m ORE.osint.cli reverse-geocode 36.34 43.13

# Messaging
python -m ORE.osint.cli send-matrix https://matrix.org "!room:id" TOKEN "Hello"
python -m ORE.osint.cli send-signal "+10000000000" "+19999999999" "Secure message"

# Generate outputs
python -m ORE.osint.cli generate-map
python -m ORE.osint.cli export-csv
python -m ORE.osint.cli export-pdf

# PGP Encryption Helpers
Generate a key and encrypt or decrypt text:

```bash
python -m ORE.osint.crypto gen-key "Alice" alice@example.com mypass
python -m ORE.osint.crypto encrypt RECIPIENT_FP "secret message"
python -m ORE.osint.crypto decrypt mypass "-----BEGIN PGP MESSAGE-----..."
```
```

Field photos and reports can be inserted into the database using custom scripts that call `add_intel()` with latitude and longitude values.
