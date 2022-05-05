from general_db import *


def get_distinct_word_percountry(con):
    country_distinct_word = {}
    sql = '''
            SELECT country_name, word
            FROM countries C, word_count W, ratings R
            WHERE W.songUUID=R.uuid AND R.country_id=C.country_id
            GROUP BY R.country_id, word ORDER BY country_name
            '''
    rows = db_query(con, sql)
    for item in rows:
        if item[0] not in country_distinct_word:
            country_distinct_word[item[0]] = item[1]
        else:
            country_distinct_word[item[0]] = str(country_distinct_word[item[0]]) + ' ' + str(item[1])

    return country_distinct_word


if __name__ == "__main__":
    con = db_connect()
    country_distinct_word = get_distinct_word_percountry(con)
    with open('country_keywords_fortopicmodeling.csv', 'w') as csv_file:
        row = 'country,words\n'
        csv_file.write(row)
        for item in country_distinct_word.items():
            row = str(item[0])+','+str(item[1])+'\n'
            csv_file.write(row)
