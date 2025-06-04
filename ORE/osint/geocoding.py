import requests
from datetime import datetime
from .database import add_intel, init_db

NOMINATIM_URL = 'https://nominatim.openstreetmap.org/search'
NOMINATIM_REVERSE_URL = 'https://nominatim.openstreetmap.org/reverse'
MAPQUEST_URL = 'https://open.mapquestapi.com/geocoding/v1/address'
MAPQUEST_REVERSE_URL = 'https://open.mapquestapi.com/geocoding/v1/reverse'


def nominatim_geocode(query: str, db_path='ore_osint.db'):
    conn = init_db(db_path)
    params = {'q': query, 'format': 'json', 'limit': 1}
    try:
        r = requests.get(NOMINATIM_URL, params=params, timeout=10, headers={'User-Agent': 'ORE-OSINT'})
        r.raise_for_status()
        data = r.json()[0]
        lat = float(data['lat'])
        lon = float(data['lon'])
        add_intel(conn, 'geocode', query, '', '', datetime.utcnow().isoformat(), lat, lon)
        return lat, lon
    except Exception as e:
        print('Nominatim error:', e)
        return None


def nominatim_reverse(lat: float, lon: float, db_path='ore_osint.db'):
    conn = init_db(db_path)
    params = {'lat': lat, 'lon': lon, 'format': 'json'}
    try:
        r = requests.get(NOMINATIM_REVERSE_URL, params=params, timeout=10, headers={'User-Agent': 'ORE-OSINT'})
        r.raise_for_status()
        data = r.json()
        display = data.get('display_name', '')
        add_intel(conn, 'reverse_geocode', display, '', '', datetime.utcnow().isoformat(), lat, lon)
        return display
    except Exception as e:
        print('Nominatim reverse error:', e)
        return None


def mapquest_geocode(query: str, api_key: str, db_path='ore_osint.db'):
    conn = init_db(db_path)
    params = {'key': api_key, 'location': query, 'maxResults': 1}
    try:
        r = requests.get(MAPQUEST_URL, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()['results'][0]['locations'][0]['latLng']
        lat = data['lat']
        lon = data['lng']
        add_intel(conn, 'geocode', query, '', '', datetime.utcnow().isoformat(), lat, lon)
        return lat, lon
    except Exception as e:
        print('MapQuest error:', e)
        return None


def mapquest_reverse(lat: float, lon: float, api_key: str, db_path='ore_osint.db'):
    conn = init_db(db_path)
    params = {
        'key': api_key,
        'location': f'{lat},{lon}',
        'includeRoadMetadata': 'false',
        'includeNearestIntersection': 'false'
    }
    try:
        r = requests.get(MAPQUEST_REVERSE_URL, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()['results'][0]['locations'][0]['street']
        add_intel(conn, 'reverse_geocode', data, '', '', datetime.utcnow().isoformat(), lat, lon)
        return data
    except Exception as e:
        print('MapQuest reverse error:', e)
        return None
