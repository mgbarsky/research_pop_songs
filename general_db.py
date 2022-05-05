import sqlite3 as lite
import sys

SQLITE_DB = 'songs.db'


def db_connect():
    con = None
    try:
        con = lite.connect(SQLITE_DB, check_same_thread=False)

    except lite.Error as e:
        if con:
            con.rollback()
        print("Connection error: {0}".format(e))
        sys.exit(1)

    return con


def db_query(con, sql, params=None):
    if not con:
        print("Not connected to the database")
        return None

    rows = None
    try:
        con.row_factory = lite.Row

        cur = con.cursor()
        if params:
            cur.execute(sql, params)
        else:
            cur.execute(sql)

        rows = cur.fetchall()

    except lite.Error as e:
        print("Connection error: {0}".format(e))

    return rows


def db_update(con, sql, params=None):
    result = None
    try:
        cur = con.cursor()
        result = cur.execute(sql, params)
        con.commit()

    except lite.Error as e:
        if con:
            con.rollback()

        print("Transaction failed: {0}".format(e))

    return result
