import os
import sqlite3

DB_PATH = '/tmp/pong.db'


def create_db():
    should_create = False
    if os.path.exists(DB_PATH):
        confirm = input(f'{DB_PATH} already exists. Do you want to recreate it? (Y/y/N/n) ')
        try:
            confirm = confirm.lower()
        except Exception:
            print('Could not understand user input: {}.'.format(confirm))
            return
        if confirm == 'y' or confirm == 'yes':
            os.remove(DB_PATH)
            should_create = True
        else:
            print('Did not recreate database.')
            return
    else:
        should_create = True

    if not should_create:
        return

    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """
        CREATE TABLE player (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            rating INTEGER
        )
        """
    )
    conn.close()
    print(f'Successfully created db at {DB_PATH}')


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
