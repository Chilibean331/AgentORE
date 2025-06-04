import subprocess
import requests
from .database import init_db, add_intel
from datetime import datetime


# Matrix simple send message via Matrix client API

def matrix_send(homeserver: str, room_id: str, token: str, message: str, db_path='ore_osint.db'):
    conn = init_db(db_path)
    url = f'{homeserver}/_matrix/client/v3/rooms/{room_id}/send/m.room.message'
    params = {'access_token': token}
    payload = {'msgtype': 'm.text', 'body': message}
    try:
        r = requests.post(url, params=params, json=payload, timeout=10)
        r.raise_for_status()
        add_intel(conn, 'matrix', message[:80], message, url, datetime.utcnow().isoformat())
    except Exception as e:
        print('Matrix send error:', e)


# Signal bridge using signal-cli (must be installed)

def signal_send(number: str, recipient: str, message: str, db_path='ore_osint.db'):
    conn = init_db(db_path)
    cmd = ['signal-cli', '-u', number, 'send', recipient, '-m', message]
    try:
        subprocess.run(cmd, check=True)
        add_intel(conn, 'signal', message[:80], message, recipient, datetime.utcnow().isoformat())
    except Exception as e:
        print('Signal send error:', e)
