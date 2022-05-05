from lda_utils import *
import pandas as pd
import numpy as np


def create_tfidf_input_for_clustering():
    raw_data = pd.read_csv('country_keywords_fortopicmodeling.csv')
    reindexed_data = raw_data['words']
    reindexed_data.index = raw_data['country']
    doc_term_2D_array = get_document_term_matrix_asarray (reindexed_data, reindexed_data.index)
    return doc_term_2D_array


def create_tfidf_input_for_website(k):
    array2D = create_tfidf_input_for_clustering()
    with open('countries_expected.txt', 'r') as input:
        expected = []
        line = input.readline()
        while line != '':
            expected.append(line.rstrip('\n'))
            line = input.readline()
    indices = []
    country_top_words = {}
    for i in range(1, len(array2D)):
        country = array2D[i][0]
        country_top_words[country] = []
        a = np.array(array2D[i][1:])
        ind = np.argpartition(a, -int(k))[-int(k):]
        ind = sorted(ind.tolist())
        for item in ind:
            country_top_words[country].append(array2D[0][item])
            if item not in indices:
                indices.append(item)
    words = []
    newarray = []
    countries = []
    ordered = []
    for c in range(1, len(array2D)):
        temp = []
        temp.append(expected[c-1])
        for i in indices:
            temp.append(array2D[c][i])
            if array2D[0][i] not in words:
                words.append(array2D[0][i])
        countries.append(array2D[c][0])
        newarray.append(temp)

    for item in expected:
        ordered.append(newarray[countries.index(item)])

    return (words, ordered, country_top_words)
