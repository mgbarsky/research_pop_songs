from general_db import *

def get_song_name_author_byid(conn, uuid):
    sql = "SELECT name,artist_name " \
          "FROM songs NATURAL JOIN artists " \
          "WHERE uuid = '"+uuid+"'"

    rows = db_query(conn, sql)
    name = rows[0]["name"]
    artist = rows[0]["artist_name"]
    name = name.replace(',', ' ')
    artist = artist.replace(',', ' ')
    return (name,artist)
