import folium
import pandas as pd
from .database import init_db


def generate_map(db_path='ore_osint.db', output_html='osint_map.html'):
    conn = init_db(db_path)
    df = pd.read_sql_query('SELECT * FROM intel', conn)
    m = folium.Map(location=[36.27, 43.38], zoom_start=8)
    for _, row in df.iterrows():
        if row['latitude'] and row['longitude']:
            folium.Marker(
                [row['latitude'], row['longitude']],
                popup=f"{row['title']} ({row['source']})"
            ).add_to(m)
    m.save(output_html)
