from general_db import *

def read_doc_topics():
    n_topics = 11
    input_file_name = "document_topics"+str(n_topics)+".csv"
    try:
        f = open(input_file_name,"r")
    except:
        print("Cannot open file for reading:",input_file_name)
        return None

    doc_topic_list = f.readlines()

    doc_topic_dict = {}
    for pair in doc_topic_list:
        doc,title,author, topic = pair.strip().split(',')
        doc_topic_dict[doc]=int(topic)

    return doc_topic_dict


def get_docs_per_country():
    con = db_connect()
    if not con:
        print("No db connection")
        return None
    sql = "SELECT c.country_name AS country, r.uuid AS doc_id " \
          "FROM ratings r, countries c " \
          "WHERE r.country_id = c.country_id"
    rows = db_query(con, sql)


    country_docs = {}
    for row in rows:
        country = row["country"]
        doc_id = row["doc_id"]

        prev_doc_list = country_docs.get(country,[])
        prev_doc_list.append(doc_id)
        country_docs[country] = prev_doc_list

    return country_docs


def main():
    doc_topic_dict = read_doc_topics()

    if doc_topic_dict is None:
        return

    country_docs = get_docs_per_country()
    if country_docs is None:
        return

    max_topic = 0
    for country,docs in country_docs.items():
        num_per_topic = {}
        for d in docs:
            if d in doc_topic_dict.keys():
                topic_id = int(doc_topic_dict[d])
                if topic_id > max_topic:
                    max_topic = topic_id
                prev_count = num_per_topic.get(topic_id,0)
                num_per_topic[topic_id] = prev_count + 1
        country_docs[country] = num_per_topic

    total_topics = max_topic +1
    f = open('country_topics.csv', 'w')
    country_file = open('countries_expected.txt', 'r')
    country_list = country_file.readlines()

    for item in country_list:
        country = item.strip()
        line = country +','
        total_docs  = 0
        for i in range(total_topics):
            count_per_topic = country_docs[country].get(i, 0)
            line += str(count_per_topic) +','
            total_docs += count_per_topic

        line += str(total_docs) +','

        for i in range(total_topics):
            count_per_topic = country_docs[country].get(i, 0)
            line += str(count_per_topic/total_docs) +','

        f.write(line[:-1]+"\n")

    f.close()








if __name__ == '__main__':
    main()