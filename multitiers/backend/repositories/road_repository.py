from contextlib import closing
import json
import sqlite3
from pathlib import Path

class RoadRepository:
    def __init__(self, path):
        self.path = str(path)
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with closing(sqlite3.connect(self.path)) as db, db:
            db.execute('CREATE TABLE IF NOT EXISTS readings (id INTEGER PRIMARY KEY, payload TEXT NOT NULL)')

    def save_and_load(self, roads):
        with closing(sqlite3.connect(self.path)) as db, db:
            db.execute('DELETE FROM readings')
            db.executemany('INSERT INTO readings VALUES (?, ?)', [(r['id'], json.dumps(r)) for r in roads])
            return [json.loads(row[0]) for row in db.execute('SELECT payload FROM readings ORDER BY id')]
