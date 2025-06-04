import requests
from datetime import datetime
from .database import add_intel, init_db

# Placeholder for pulling Sentinel Hub or other imagery. Requires API credentials.
SENTINEL_API = 'https://api.sentinel-hub.com'

def fetch_satellite_metadata(area: str, db_path='ore_osint.db'):
    conn = init_db(db_path)
    # This is a simplified placeholder request.
    params = {'q': area}
    try:
        r = requests.get(f'{SENTINEL_API}/search', params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
        for item in data.get('results', []):
            title = item.get('title', 'Satellite Image')
            url = item.get('preview', '')
            ts = item.get('timestamp', datetime.utcnow().isoformat())
            add_intel(conn, 'satellite', title, '', url, ts)
    except Exception as e:
        print('Satellite fetch error:', e)

NASA_API = 'https://api.nasa.gov/planetary/earth/assets'
OPEN_AERIAL_MAP = 'https://api.openaerialmap.org'
OSM_TILE_URL = 'https://tile.openstreetmap.org/{z}/{x}/{y}.png'


def fetch_nasa_imagery(lat: float, lon: float, api_key: str, db_path='ore_osint.db'):
    conn = init_db(db_path)
    params = {
        'lon': lon,
        'lat': lat,
        'api_key': api_key,
    }
    try:
        r = requests.get(NASA_API, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
        for result in data.get('results', []):
            url = result.get('url')
            ts = result.get('date', datetime.utcnow().isoformat())
            add_intel(conn, 'satellite', 'NASA imagery', '', url, ts)
    except Exception as e:
        print('NASA imagery error:', e)


def fetch_open_aerial(area: str, db_path='ore_osint.db'):
    conn = init_db(db_path)
    params = {'bbox': area, 'limit': 5}
    try:
        r = requests.get(f'{OPEN_AERIAL_MAP}/images', params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
        for feature in data.get('features', []):
            props = feature.get('properties', {})
            url = props.get('url')
            ts = props.get('acquisition_start', datetime.utcnow().isoformat())
            add_intel(conn, 'satellite', 'OpenAerialMap', '', url, ts)
    except Exception as e:
        print('OpenAerialMap error:', e)


def fetch_osm_tile(z: int, x: int, y: int, db_path='ore_osint.db'):
    conn = init_db(db_path)
    url = OSM_TILE_URL.format(z=z, x=x, y=y)
    ts = datetime.utcnow().isoformat()
    add_intel(conn, 'satellite', f'OSM tile {z}/{x}/{y}', '', url, ts)
    return url
