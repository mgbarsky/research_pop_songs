from general_db import *
import pickle
import glob
import os

global songs_info
global country_info
global lyrics_info

# python3 populate_data.py 2018-08-13songs_info_pickle.txt 2018-08-13charts_info_pickle.txt lyrics_results_pickle.txt
# 20180726/

def read_as_dict():
    global songs_info, country_info, lyrics_info
    with open(sys.argv[1], 'rb') as handle:
        songs_info = pickle.loads(handle.read())
    with open(sys.argv[2], 'rb') as handle:
        country_info = pickle.loads(handle.read())
    with open(sys.argv[3], 'rb') as handle:
        lyrics_info = pickle.loads(handle.read())


def insert_country(con):
        sql = "INSERT or IGNORE INTO countries(country_id, country_name) VALUES(?, ?)"
        for key in country_info.keys():
            params = (country_info[key][0], key)
            db_update(con, sql, params)


def insert_artist(con):
    sql = "INSERT or IGNORE INTO artists(artist_id, artist_name) VALUES(?, ?)"
    for key in songs_info.keys():
        params = (songs_info[key][1], key[1])
        db_update(con, sql, params)


def insert_rating(con):
    sql = "INSERT or IGNORE INTO ratings(uuid, country_id, rating, chart_date) VALUES(?, ?, ?, ?)"
    for key in songs_info.keys():
        uuid = str(songs_info[key][0])
        for i in range(1, len(songs_info[key])):
            if i%2 == 0:
                country_id = int(country_info[songs_info[key][i]][0])
                rating = int(songs_info[key][i+1])
                chart_date = country_info[songs_info[key][i]][1]
                chart_date = int(chart_date[6:]+chart_date[3:5]+chart_date[0:2])
                params = (uuid, country_id, rating, chart_date)
                db_update(con, sql, params)


def insert_songs(con):
    sql = "INSERT or IGNORE INTO songs(uuid, name, artist_id, lyrics) VALUES(?, ?, ?, ?)"
    for key in songs_info.keys():
        uuid = str(songs_info[key][0])
        name = key[0]
        artist_id = int(songs_info[key][1])
        lyrics = int(lyrics_info[key][0])
        params = (uuid, name, artist_id, lyrics)
        db_update(con, sql, params)


def insert_word_count(con):
    sql = "INSERT or REPLACE INTO word_count(uuid, word, frequency) VALUES(?, ?, ?)"
    script_dir = os.path.dirname(os.path.abspath(__file__))
    path = script_dir+'/'+sys.argv[4]+'lyricsSearchResults/wordsUUID/*.txt'
    files = glob.glob(path)
    for file in files:
        fileUUID = file[len(file)-40:len(file)-4]
        with open(file, 'rb') as handle:
            temp = pickle.loads(handle.read())
        for key in temp.keys():
            params = (fileUUID, key, temp[key])
            db_update(con, sql, params)


if __name__ == "__main__":
    global songs_info, country_info, lyrics_info
    songs_info = {}
    country_info = {}
    lyrics_info = {}
    con = db_connect()
    read_as_dict()
    insert_country(con)
    insert_artist(con)
    insert_rating(con)
    insert_songs(con)
    # insert_word_count(con)



    # sql1 = "SELECT * FROM artists"
    # cursor = db_query(con, sql1)
    # print (cursor)
