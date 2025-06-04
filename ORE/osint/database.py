import sqlite3
from typing import List, Tuple, Optional
import csv
import pandas as pd
from fpdf import FPDF

DB_FILE = 'ore_osint.db'

CREATE_TABLE_SQL = '''
CREATE TABLE IF NOT EXISTS intel (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source TEXT,
    title TEXT,
    content TEXT,
    url TEXT,
    timestamp TEXT,
    latitude REAL,
    longitude REAL
);
'''

def init_db(db_file: str = DB_FILE) -> sqlite3.Connection:
    conn = sqlite3.connect(db_file)
    with conn:
        conn.execute(CREATE_TABLE_SQL)
    return conn

def add_intel(conn: sqlite3.Connection, source: str, title: str, content: str,
              url: str, timestamp: str, latitude: Optional[float] = None,
              longitude: Optional[float] = None) -> int:
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO intel (source, title, content, url, timestamp, latitude, longitude) '\
        'VALUES (?, ?, ?, ?, ?, ?, ?)',
        (source, title, content, url, timestamp, latitude, longitude)
    )
    conn.commit()
    return cur.lastrowid

def search_intel(conn: sqlite3.Connection, keyword: str) -> List[Tuple]:
    cur = conn.cursor()
    cur.execute(
        'SELECT * FROM intel WHERE title LIKE ? OR content LIKE ?',
        (f'%{keyword}%', f'%{keyword}%')
    )
    return cur.fetchall()

def export_csv(conn: sqlite3.Connection, csv_file: str):
    df = pd.read_sql_query('SELECT * FROM intel', conn)
    df.to_csv(csv_file, index=False)

def export_pdf(conn: sqlite3.Connection, pdf_file: str):
    df = pd.read_sql_query('SELECT * FROM intel', conn)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(40, 10, 'ORE OSINT Report')
    pdf.ln(20)
    pdf.set_font('Arial', '', 10)
    for _, row in df.iterrows():
        text = f"{row['timestamp']} [{row['source']}] {row['title']} - {row['url']}"
        pdf.multi_cell(0, 10, text)
        pdf.ln(1)
    pdf.output(pdf_file)
