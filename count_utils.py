import operator
from general_db import *

def create_count_input_for_clustering():
    con = db_connect()
    index_all = 0
    temp_all = {}
    country_fre_all = {}
    word_index_all = {}
    with open('countries_expected.txt', 'r') as file:
        for line in file:
            country_fre_all[line.replace('\n', '')] = []
    for ckey in country_fre_all.keys():
        with con:
            cur = con.cursor()
            cur.execute('SELECT word, sum(frequency) FROM word_count W, ratings R, countries C WHERE W.songUUID=R.uuid AND R.country_id=C.country_id AND C.country_name=? GROUP BY word ORDER BY sum(frequency) DESC', (ckey,))
            con.commit()
            rows_all = cur.fetchall()
            for item in rows_all:
                if item[0] not in word_index_all:
                    word_index_all[item[0]] = index_all
                    index_all += 1
            temp_all[ckey] = rows_all
    word_index_all['words/countries'] = -1
    sorted_word_dict = dict(sorted(word_index_all.items(), key=operator.itemgetter(1)))
    for key in country_fre_all.keys():
        country_fre_all[key] = [0 for i in range(len(word_index_all))]
        for item in temp_all[key]:
            country_fre_all[key][word_index_all[item[0]]] = item[1]

    return (sorted_word_dict, country_fre_all)


def create_count_input_for_website(k):
    con = db_connect()
    index = 0
    temp = {}
    country_fre = {}
    word_index = {}
    with open('countries_expected.txt', 'r') as file:
        for line in file:
            country_fre[line.replace('\n', '')] = []
    country_top_words = {}
    for ckey in country_fre.keys():
        country_top_words[ckey] = []
        with con:
            cur = con.cursor()
            cur.execute('SELECT word, sum(frequency) FROM word_count W, ratings R, countries C WHERE W.songUUID=R.uuid AND R.country_id=C.country_id AND C.country_name=? GROUP BY word ORDER BY sum(frequency) DESC LIMIT ?', (ckey,k))
            con.commit()
            rows = cur.fetchall()
            for item in rows:
                country_top_words[ckey].append(item[0])
                if item[0] not in word_index:
                    word_index[item[0]] = index
                    index += 1
            temp[ckey] = rows
    sorted_index = sorted(word_index.items(), key=operator.itemgetter(1))
    words = []
    for item in sorted_index:
        words.append(item[0])
    for key in country_fre.keys():
        country_fre[key] = [0 for i in range(len(word_index))]
        for item in temp[key]:
            country_fre[key][word_index[item[0]]] = item[1]
        for i in range(len(country_fre[key])):
            if country_fre[key][i] == 0:
                with con:
                    cur = con.cursor()
                    cur.execute('SELECT sum(frequency) FROM word_count W, ratings R, countries C WHERE W.songUUID=R.uuid AND R.country_id=C.country_id AND C.country_name=? AND W.word=?', (key,sorted_index[i][0]))
                    con.commit()
                    count = cur.fetchall()
                    if count[0][0] != None:
                        country_fre[key][i] = count[0][0]
    return(words, country_fre, country_top_words)
