from general_db import *
from lda_utils import *
import pandas as pd

def read_database(con):
    uuid_country_dict = {}
    sql = 'SELECT country_name, uuid FROM countries C, ratings R WHERE R.country_id=C.country_id GROUP BY country_name, uuid ORDER BY country_name'
    rows = db_query(con, sql)
    prev = ''
    for row in rows:
        if row[0] != prev:
            count = 0
        if row[1] not in uuid_country_dict:
            uuid_country_dict[row[1]] = [row[0] + str(count)]
        else:
            uuid_country_dict[row[1]].append(row[0] + str(count))
        count += 1
        prev = row[0]
    return uuid_country_dict


if __name__ == '__main__':
    con = db_connect()
    uuid_country_dict = read_database(con)
    renamed_list = []
    raw_data = pd.read_csv('song_keywords_fortopicmodeling.csv')
    reindexed_data = raw_data['words']
    reindexed_data.index = raw_data['UUID']
    doc_term_2D_array = get_document_term_matrix_asarray (reindexed_data, reindexed_data.index)
    renamed_list.append(doc_term_2D_array[0])
    for i in range(1, len(doc_term_2D_array)):
        uuid = doc_term_2D_array[i][0]
        for j in range(len(uuid_country_dict[uuid])):
            print(uuid_country_dict[uuid][j])
            newlist = doc_term_2D_array[i].copy()
            newlist[0] = uuid_country_dict[uuid][j]
            renamed_list.append(newlist)

    with open('renamed_tfidf.tsv', 'w') as output:
        for i in range(len(renamed_list)):
            row = ''
            for item in renamed_list[i]:
                row = row + str(item) + '\t'
            row.rstrip('\t')
            output.write(row + '\n')
