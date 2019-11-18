import os
import sqlite3

DB_PATH = '/tmp/pong.db'

# conn.execute requires an Iterable to be passed to params. This is for convenience.
NO_DATA = []


def create_db():
    should_create = False
    if os.path.exists(DB_PATH):
        confirm = input(f'{DB_PATH} already exists. Do you want to recreate it? (Y/y/Yes/yes) ')
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

    if should_create:
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
    conn.commit()


def select_players(*ids):
    conn = sqlite3.connect(DB_PATH)
    data = NO_DATA
    query = "SELECT * FROM player"
    if ids:
        data = ','.join([str(i) for i in ids])
        query += " WHERE id IN (?)"
    res = conn.execute(query, data)
    print(list(res))


if __name__ == "__main__":
    create_db()
