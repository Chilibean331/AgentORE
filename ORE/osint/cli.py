import argparse
from . import feeds, social_media, satellites, database, map


def main():
    parser = argparse.ArgumentParser(description='ORE OSINT Toolkit')
    sub = parser.add_subparsers(dest='cmd')

    sub.add_parser('fetch-news')

    tw = sub.add_parser('scrape-twitter')
    tw.add_argument('query')
    tw.add_argument('--limit', type=int, default=50)

    sat = sub.add_parser('fetch-satellite')
    sat.add_argument('area')

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
    elif args.cmd == 'fetch-satellite':
        satellites.fetch_satellite_metadata(args.area)
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
