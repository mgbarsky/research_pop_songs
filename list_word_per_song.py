from general_db import *

def get_distinct_word_persong(con):
    song_distinct_word = {}
    sql = 'SELECT songUUID, word FROM word_count'
    with con:
        cur = con.cursor()
        cur.execute(sql)
        con.commit()
        rows = cur.fetchall()
    for item in rows:
        if item[0] not in song_distinct_word:
            song_distinct_word[item[0]] = item[1]
        else:
            song_distinct_word[item[0]] = str(song_distinct_word[item[0]]) + ' ' + str(item[1])

    return song_distinct_word


if __name__ == "__main__":
    con = db_connect()
    song_distinct_word = get_distinct_word_persong(con)
    with open('song_keywords_fortopicmodeling.csv', 'w') as csv_file:
        row = 'UUID,words\n'
        csv_file.write(row)
        for item in song_distinct_word.items():
            row = str(item[0])+','+str(item[1])+'\n'
            csv_file.write(row)
