from general_db import *


def get_distinct_word_persong(con):
    song_distinct_word = {}
    sql = 'SELECT wc.songUUID as uuid, name, artist_name as artist, word ' \
          'FROM word_count wc, songs s, artists a ' \
          'WHERE wc.songUUID = s.uuid ' \
          'AND s.artist_id = a.artist_id'
    rows = db_query(con, sql)

    for row in rows:
        title = str(row["name"])
        m = map(lambda x: x.lower() if x.isalpha() or x.isdigit() else ' ', title)
        # convert from list of letters to string
        title = "".join(list(m))
        artist = str(row["artist"])
        m = map(lambda x: x.lower() if x.isalpha() else ' ', artist)
        # convert from list of letters to string
        artist = "".join(list(m))
        song_name = title +',' + artist
        if song_name not in song_distinct_word:
            song_distinct_word[song_name] = row["word"]
        else:
            song_distinct_word[song_name] = str(song_distinct_word[song_name]) \
                                            + ' ' + str(row["word"])

    return song_distinct_word


def get_distinct_word_per_country(con):
    country_distinct_word = {}
    sql = 'SELECT wc.word as word, c.country_name as country ' \
          'FROM word_count wc, countries c, ratings r ' \
          'WHERE wc.songUUID = r.uuid ' \
          'AND r.country_id = c.country_id '
    rows = db_query(con, sql)

    for row in rows:
        country = str(row["country"])

        if country not in country_distinct_word:
            country_distinct_word[country] = row["word"]
        else:
            country_distinct_word[country] = str(country_distinct_word[country]) \
                                            + ' ' + str(row["word"])

    return country_distinct_word


if __name__ == "__main__":
    con = db_connect()
    song_distinct_word = get_distinct_word_persong(con)
    with open('song_keywords_dataset.csv', 'w') as csv_file:
        row = 'song,artist,words\n'
        csv_file.write(row)
        for key,words in song_distinct_word.items():
            row = str(key)+','+str(words)+'\n'
            csv_file.write(row)

    country_distinct_word = get_distinct_word_per_country(con)
    with open('country_keywords_dataset.csv', 'w') as csv_file:
        row = 'country,words\n'
        csv_file.write(row)
        for key, words in country_distinct_word.items():
            row = str(key) + ',' + str(words) + '\n'
            csv_file.write(row)