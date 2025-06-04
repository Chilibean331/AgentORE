# ORE OSINT Toolkit

This module collects open-source intelligence (OSINT) for the Nineveh Plains and wider Iraq region.

## Features

- **News scraping** via RSS feeds
- **Social media scraping** using [snscrape](https://github.com/JustAnotherArchivist/snscrape)
- **Satellite imagery metadata** retrieval (Sentinel Hub placeholder)
- **Storage** in a local SQLite database
- **Search and export** of collected intel to CSV or PDF
- **Interactive map** generation using Leaflet (via `folium`)

## Usage

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the command line interface:

```bash
python -m ORE.osint.cli fetch-news
python -m ORE.osint.cli scrape-twitter "Nineveh" --limit 20
python -m ORE.osint.cli fetch-satellite "Nineveh Plains"
python -m ORE.osint.cli generate-map
```

Exports:

```bash
python -m ORE.osint.cli export-csv
python -m ORE.osint.cli export-pdf
```

Field photos and reports can be inserted into the database using custom scripts that call `add_intel()` with latitude and longitude values.
