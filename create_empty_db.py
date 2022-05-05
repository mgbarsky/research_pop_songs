import sqlite3


def create_songs_db():
    sql = open('songs.sql', 'r').read()
    conn = sqlite3.connect('songs.db')

    sqlCommands = sql.split(';')

    for command in sqlCommands:
        c = conn.cursor()
        c.execute(command)
    conn.commit()
    conn.close()


if __name__ == '__main__':
    create_songs_db()