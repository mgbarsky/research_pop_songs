from general_db import *
import math

def get_tf_idf(count_list, distinct_words):
    idf_perword = {}
    for word in distinct_words:
        idf_perword[word] = 0

    # count of documents where each word appears
    total_docs = 0
    for item in count_list:
        w = item["word"]
        idf_perword[w] += 1
        total_docs += 1

    # compute inverse frequency - idf
    for word, count in idf_perword.items():
        idf = math.log(total_docs / count)
        idf_perword[word] = idf

    # total number of words in each document
    total_words_perdoc = {}
    for item in count_list:
        s = item["song_id"]
        prev_count = total_words_perdoc.get(s, 0)
        total_words_perdoc[s] = prev_count + 1

    tf_idf_dictionary = {}
    for item in count_list:
        s = item["song_id"]
        w = item["word"]
        doc_dictionary = tf_idf_dictionary.get(s, {})
        doc_dictionary[w] = 1 / total_words_perdoc[s] * idf_perword[w]
        tf_idf_dictionary[s] = doc_dictionary

    return tf_idf_dictionary


def main():
    con = db_connect()
    if not con:
        print ("No db connection")
        return
    sql = "SELECT * FROM word_count"
    rows = db_query(con, sql)

    count_list = []
    for row in rows:
        p = {}
        p["song_id"] = row["songUUID"]
        p["word"] = row["word"]
        p["frequency"] = row["frequency"]
        count_list.append(p)


    sql = "SELECT DISTINCT word FROM word_count"
    rows = db_query(con, sql)
    distinct_words = []

    for row in rows:
        distinct_words.append(row["word"])

    tfidf_dictionary = get_tf_idf(count_list, distinct_words)

    print(tfidf_dictionary)



if __name__ == "__main__":
    main()
