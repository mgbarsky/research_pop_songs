import numpy as np

from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer


def get_document_term_matrix_asarray (pd_data, pd_keys=None):
    count_vectorizer = TfidfVectorizer(max_df=0.70, min_df=3, binary=True)
    data_matrix = pd_data.as_matrix()

    # print('Headline before vectorization: ', [55])
    document_term_matrix = count_vectorizer.fit_transform(data_matrix)

    word_to_index = count_vectorizer.vocabulary_

    words_array = ['']*len(word_to_index)

    for w,i in word_to_index.items():
        words_array[i] = w

    words_array.insert (0, "docs")

    doc_term_2D_array = document_term_matrix.toarray().tolist()

    doc_term_2D_array.insert (0, words_array)
    for i in range(1,len(doc_term_2D_array)):
        doc_term_2D_array[i] = [round(f,2) for f in doc_term_2D_array[i]]

    if pd_keys is not None:
        doc_id_list = pd_keys.tolist()
        for i in range (len(doc_id_list)):
            doc_id = doc_id_list[i]
            doc_term_2D_array[i+1].insert(0,doc_id)

    return doc_term_2D_array


def get_document_term_matrix (pd_data, count_vectorizer):
    data_matrix = pd_data.as_matrix()

    # print('Headline before vectorization: ', [55])
    document_term_matrix = count_vectorizer.fit_transform(data_matrix)

    # print(count_vectorizer.vocabulary_)
    return document_term_matrix


def get_mean_topic_vectors(keys, two_dim_vectors, n_topics):
    '''returns a list of centroid vectors from each predicted topic category'''

    mean_topic_vectors = []
    for t in range(n_topics):
        articles_in_that_topic = []
        for i in range(len(keys)):
            if keys[i] == t:
                articles_in_that_topic.append(two_dim_vectors[i])

        if len(articles_in_that_topic)>0:
            articles_in_that_topic = np.vstack(articles_in_that_topic)


            mean_article_in_that_topic = np.mean(articles_in_that_topic, axis=0)
            mean_topic_vectors.append(mean_article_in_that_topic)
    return mean_topic_vectors


def get_top_n_words1(n_top_words, count_vectorizer, text_data):
    '''returns a tuple of the top n words in a sample
    and their accompanying counts, given a CountVectorizer object and text sample'''
    vectorized_headlines = count_vectorizer.fit_transform(text_data.as_matrix())

    vectorized_total = np.sum(vectorized_headlines, axis=0)
    word_indices = np.flip(np.argsort(vectorized_total)[0, :], 1)
    word_values = np.flip(np.sort(vectorized_total)[0, :], 1)

    word_vectors = np.zeros((n_top_words, vectorized_headlines.shape[1]))
    for i in range(n_top_words):
        word_vectors[i, word_indices[0, i]] = 1

    words = [word[0].encode('ascii').decode('utf-8') for word in count_vectorizer.inverse_transform(word_vectors)]

    return (words, word_values[0, :n_top_words].tolist()[0])


def get_top_n_words(n, keys, document_term_matrix, count_vectorizer, n_topics):
    '''returns a list of n_topic strings, where each string contains the n most common
        words in a predicted category, in order'''
    top_word_indices = []
    for topic in range(n_topics):
        temp_vector_sum = None
        for i in range(len(keys)):
            if keys[i] == topic:
                if temp_vector_sum is not None:
                    temp_vector_sum += document_term_matrix[i]
                else:
                    temp_vector_sum = document_term_matrix[i]

        if temp_vector_sum is not None:
            temp_vector_sum = temp_vector_sum.toarray()
            top_n_word_indices = np.flip(np.argsort(temp_vector_sum)[0][-n:],0)
            top_word_indices.append(top_n_word_indices)
    top_words = []
    for topic in top_word_indices:
        topic_words = []
        for index in topic:
            temp_word_vector = np.zeros((1,document_term_matrix.shape[1]))
            temp_word_vector[:,index] = 1
            the_word = count_vectorizer.inverse_transform(temp_word_vector)[0][0]
            topic_words.append(the_word.encode('ascii').decode('utf-8'))
        top_words.append(" ".join(topic_words))

    return top_words


def get_keys(topic_matrix):
    '''returns an integer list of predicted topic categories for a given topic matrix'''
    keys = []
    for i in range(topic_matrix.shape[0]):
        keys.append(topic_matrix[i].argmax())
    return keys


def keys_to_counts(keys):
    '''returns a tuple of topic categories and their accompanying magnitudes for a given list of keys'''
    count_pairs = Counter(keys).items()
    categories = [pair[0] for pair in count_pairs]
    counts = [pair[1] for pair in count_pairs]
    return (categories, counts)
