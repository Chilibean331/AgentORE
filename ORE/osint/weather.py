import requests
from datetime import datetime
from .database import add_intel, init_db

OPEN_METEO_URL = 'https://api.open-meteo.com/v1/forecast'
NOAA_URL = 'https://api.weather.gov/gridpoints'
VISUAL_CROSSING_URL = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline'


def fetch_open_meteo(lat: float, lon: float, db_path='ore_osint.db'):
    conn = init_db(db_path)
    params = {
        'latitude': lat,
        'longitude': lon,
        'hourly': 'temperature_2m',
    }
    try:
        r = requests.get(OPEN_METEO_URL, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
        temps = data.get('hourly', {}).get('temperature_2m', [])
        timestamp = datetime.utcnow().isoformat()
        add_intel(conn, 'weather', f'Open-Meteo {lat},{lon}', str(temps[:24]), '', timestamp)
    except Exception as e:
        print('Open-Meteo error:', e)


def fetch_noaa(grid_id: str, grid_x: int, grid_y: int, db_path='ore_osint.db'):
    conn = init_db(db_path)
    url = f'{NOAA_URL}/{grid_id}/{grid_x},{grid_y}/forecast'
    headers = {'User-Agent': 'ORE-OSINT'}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        data = r.json()
        periods = data.get('properties', {}).get('periods', [])
        timestamp = datetime.utcnow().isoformat()
        add_intel(conn, 'weather', f'NOAA {grid_id}', str(periods[:5]), '', timestamp)
    except Exception as e:
        print('NOAA error:', e)


def fetch_visual_crossing(location: str, api_key: str, db_path='ore_osint.db'):
    conn = init_db(db_path)
    url = f'{VISUAL_CROSSING_URL}/{location}'
    params = {'key': api_key, 'unitGroup': 'metric', 'include': 'days'}
    try:
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
        days = data.get('days', [])
        timestamp = datetime.utcnow().isoformat()
        add_intel(conn, 'weather', f'Visual Crossing {location}', str(days[:3]), '', timestamp)
    except Exception as e:
        print('Visual Crossing error:', e)
