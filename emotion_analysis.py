from general_db import *

def get_prop(con, positive, negative):
    sql = 'SELECT DISTINCT word FROM word_count'
    rows = db_query(con, sql)
    success = 0
    count = 0
    for row in rows:
        if row[0] in positive or row[0] in negative:
            success += 1
        count += 1
    print (success/count)


if __name__ == '__main__':
    with open('positive-words.txt', 'r', encoding='utf-8') as input:
        positive = input.read().split()

    with open('negative-words.txt', 'r', encoding='ISO-8859-1') as input:
        negative = input.read().split()

    con = db_connect()
    get_prop(con, positive, negative)
