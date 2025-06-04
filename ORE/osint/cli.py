import argparse
from . import (
    feeds,
    social_media,
    satellites,
    database,
    map,
    weather,
    geocoding,
    messaging,
)


def main():
    parser = argparse.ArgumentParser(description='ORE OSINT Toolkit')
    sub = parser.add_subparsers(dest='cmd')

    sub.add_parser('fetch-news')

    tw = sub.add_parser('scrape-twitter')
    tw.add_argument('query')
    tw.add_argument('--limit', type=int, default=50)

    tw_api = sub.add_parser('twitter-api')
    tw_api.add_argument('query')
    tw_api.add_argument('token')

    sat = sub.add_parser('fetch-satellite')
    sat.add_argument('area')

    nasa = sub.add_parser('fetch-nasa')
    nasa.add_argument('lat', type=float)
    nasa.add_argument('lon', type=float)
    nasa.add_argument('api_key')

    oam = sub.add_parser('fetch-oam')
    oam.add_argument('bbox')

    weather_open = sub.add_parser('weather-open')
    weather_open.add_argument('lat', type=float)
    weather_open.add_argument('lon', type=float)

    weather_noaa = sub.add_parser('weather-noaa')
    weather_noaa.add_argument('grid_id')
    weather_noaa.add_argument('grid_x', type=int)
    weather_noaa.add_argument('grid_y', type=int)

    weather_vc = sub.add_parser('weather-vc')
    weather_vc.add_argument('location')
    weather_vc.add_argument('api_key')

    geo = sub.add_parser('geocode')
    geo.add_argument('query')

    rev = sub.add_parser('reverse-geocode')
    rev.add_argument('lat', type=float)
    rev.add_argument('lon', type=float)

    msg_matrix = sub.add_parser('send-matrix')
    msg_matrix.add_argument('homeserver')
    msg_matrix.add_argument('room_id')
    msg_matrix.add_argument('token')
    msg_matrix.add_argument('message')

    msg_signal = sub.add_parser('send-signal')
    msg_signal.add_argument('number')
    msg_signal.add_argument('recipient')
    msg_signal.add_argument('message')

    search = sub.add_parser('search')
    search.add_argument('keyword')

    sub.add_parser('export-csv')
    sub.add_parser('export-pdf')
    sub.add_parser('generate-map')

    args = parser.parse_args()
    if args.cmd == 'fetch-news':
        feeds.fetch_news()
    elif args.cmd == 'scrape-twitter':
        social_media.scrape_twitter(args.query, args.limit)
    elif args.cmd == 'twitter-api':
        social_media.twitter_api_search(args.query, args.token)
    elif args.cmd == 'fetch-satellite':
        satellites.fetch_satellite_metadata(args.area)
    elif args.cmd == 'fetch-nasa':
        satellites.fetch_nasa_imagery(args.lat, args.lon, args.api_key)
    elif args.cmd == 'fetch-oam':
        satellites.fetch_open_aerial(args.bbox)
    elif args.cmd == 'weather-open':
        weather.fetch_open_meteo(args.lat, args.lon)
    elif args.cmd == 'weather-noaa':
        weather.fetch_noaa(args.grid_id, args.grid_x, args.grid_y)
    elif args.cmd == 'weather-vc':
        weather.fetch_visual_crossing(args.location, args.api_key)
    elif args.cmd == 'geocode':
        geocoding.nominatim_geocode(args.query)
    elif args.cmd == 'reverse-geocode':
        geocoding.nominatim_reverse(args.lat, args.lon)
    elif args.cmd == 'send-matrix':
        messaging.matrix_send(args.homeserver, args.room_id, args.token, args.message)
    elif args.cmd == 'send-signal':
        messaging.signal_send(args.number, args.recipient, args.message)
    elif args.cmd == 'search':
        conn = database.init_db()
        rows = database.search_intel(conn, args.keyword)
        for r in rows:
            print(r)
    elif args.cmd == 'export-csv':
        conn = database.init_db()
        database.export_csv(conn, 'intel_export.csv')
    elif args.cmd == 'export-pdf':
        conn = database.init_db()
        database.export_pdf(conn, 'intel_export.pdf')
    elif args.cmd == 'generate-map':
        map.generate_map()
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
