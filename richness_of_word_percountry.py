from general_db import *
import operator

def get_distinct_num_percountry(con):
    distinct_percountry = {}
    sql = '''
            SELECT country_name, count(*) as word
            FROM (SELECT country_name, word FROM countries C, word_count W, ratings R
            WHERE W.songUUID=R.uuid AND R.country_id=C.country_id GROUP BY R.country_id, word ORDER BY country_name)
            GROUP BY country_name
            '''
    rows = db_query(con, sql)
    for row in rows:
        distinct_percountry[row[0]] = row[1]

    return distinct_percountry

def get_all_num_percountry(con):
    all_percountry = {}
    sql = '''
            SELECT country_name, sum(sumfre)
            FROM (SELECT country_name, word, sum(frequency) as sumfre FROM countries C, word_count W, ratings R
            WHERE W.songUUID=R.uuid AND R.country_id=C.country_id GROUP BY R.country_id, word ORDER BY country_name)
            GROUP BY country_name
            '''
    rows = db_query(con, sql)
    for row in rows:
        all_percountry[row[0]] = row[1]

    return all_percountry

if __name__ == '__main__':
    con = db_connect()
    distinct_percountry = get_distinct_num_percountry(con)
    all_percountry = get_all_num_percountry(con)
    country_prop = {}
    for key in distinct_percountry.keys():
        prop = distinct_percountry[key]/all_percountry[key]
        country_prop[key] = prop
    sorted_country_prop = sorted(country_prop.items(), key=operator.itemgetter(1))
    print (sorted_country_prop)
