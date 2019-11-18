import sqlite3

DB_PATH = '/tmp/pong.db'

PLAYER_TABLE_CREATE = """
CREATE TABLE IF NOT EXISTS player (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    rating INTEGER
)
"""


def create_tables():
    conn = sqlite3.connect(DB_PATH)
    conn.execute(PLAYER_TABLE_CREATE)
    conn.close()


def insert_players(vals):
    conn = sqlite3.connect(DB_PATH)
    conn.executemany("INSERT INTO player (name, rating) VALUES (?, ?)", vals)
    conn.close()


def select_players(*ids):
    conn = sqlite3.connect(DB_PATH)
    if ids:
        data = ','.join([str(i) for i in ids])
        query = "SELECT * FROM player WHERE id IN (?)"
        res = conn.execute(query, data)
    else:
        res = conn.execute("SELECT * FROM player")
    players = list(res)
    conn.close()
    return players


if __name__ == "__main__":
    pass
