import os
import sqlite3

DB_PATH = '/tmp/pong.db'


def create_db():
    if os.path.exists(DB_PATH):
        confirm = input(f'{DB_PATH} already exists. Do you want to recreate it? (Y/y/Yes/yes) ')
        try:
            confirm = confirm.lower()
        except Exception:
            print('Could not understand user input: {}. Exiting.'.format(confirm))
            exit(1)
        if confirm == 'y' or confirm == 'yes':
            os.remove(DB_PATH)
        else:
            print('Did not recreate database. Exiting.')
            exit(0)

    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """
        CREATE TABLE player (id integer primary key, name text, rating int)
        """
    )
    conn.close()
    print(f'Successfully created db at {DB_PATH}')


if __name__ == "__main__":
    create_db()
