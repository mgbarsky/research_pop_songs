import matplotlib.mlab as mlab
import seaborn as sb
import ast

import matplotlib.pyplot as plt

import pandas as pd
from IPython.display import display
from jedi.refactoring import inline
from tqdm import tqdm


from sklearn.decomposition import TruncatedSVD
from sklearn.decomposition import LatentDirichletAllocation

from bokeh.plotting import figure, output_file, show
from bokeh.models import Label
from sklearn.manifold import TSNE
from lda_utils import *
from db_utils import *

def plot_top_words(reindexed_data):
    count_vectorizer = TfidfVectorizer()
    words, word_values = get_top_n_words1(n_top_words=10, count_vectorizer=count_vectorizer, text_data=reindexed_data)

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(range(len(words)), word_values)
    ax.set_xticks(range(len(words)))
    ax.set_xticklabels(words)
    ax.set_title('Top Words')

    plt.show()


def extract_lsa_model (document_term_matrix, n_topics, count_vectorizer, show_plot = False, show_cluster = False):
    lsa_model = TruncatedSVD(n_components=n_topics)
    lsa_topic_matrix = lsa_model.fit_transform(document_term_matrix)

    lsa_keys = get_keys(lsa_topic_matrix)
    lsa_categories, lsa_counts = keys_to_counts(lsa_keys)

    top_n_words_lsa = get_top_n_words(10, lsa_keys, document_term_matrix, count_vectorizer, n_topics)

    print("\nLSA topic words sorted by word")

    for i in range(len(top_n_words_lsa)):
        topic_word_list = top_n_words_lsa[i].split()
        topic_word_list = sorted(topic_word_list)
        print(topic_word_list)

    if show_plot:
        top_3_words = get_top_n_words(2, lsa_keys, document_term_matrix, count_vectorizer, n_topics)
        labels = ['Topic {}: \n'.format(i) + top_3_words[i] for i in range(len(lsa_categories))]

        fig, ax = plt.subplots(figsize=(8, 7))
        ax.bar(lsa_categories, lsa_counts)
        ax.set_xticks(lsa_categories)
        ax.set_xticklabels(labels)
        ax.set_title('LSA Topic Category Counts')

        plt.show()
    elif show_cluster:
        tsne_lsa_model = TSNE(n_components=2, perplexity=50, learning_rate=100,
                              n_iter=2000, verbose=1, random_state=0, angle=0.75)
        tsne_lsa_vectors = tsne_lsa_model.fit_transform(lsa_topic_matrix)

        colormap = np.array([
            "#1f77b4", "#aec7e8", "#ff7f0e", "#ffbb78", "#2ca02c",
            "#98df8a", "#d62728", "#ff9896", "#9467bd", "#c5b0d5",
            "#8c564b", "#c49c94", "#e377c2", "#f7b6d2", "#7f7f7f",
            "#c7c7c7", "#bcbd22", "#dbdb8d", "#17becf", "#9edae5"])
        colormap = colormap[:n_topics]

        top_3_words_lsa = get_top_n_words(3, lsa_keys, document_term_matrix, count_vectorizer, n_topics)
        lsa_mean_topic_vectors = get_mean_topic_vectors(lsa_keys, tsne_lsa_vectors, n_topics)

        plot = figure(title="t-SNE Clustering of {} LSA Topics".format(n_topics), plot_width=700, plot_height=700)
        plot.scatter(x=tsne_lsa_vectors[:, 0], y=tsne_lsa_vectors[:, 1], color=colormap[lsa_keys])

        for t in range(n_topics):
            label = Label(x=lsa_mean_topic_vectors[t][0], y=lsa_mean_topic_vectors[t][1],
                          text=top_3_words_lsa[t], text_color=colormap[t])
            plot.add_layout(label)

        show(plot)
    else:
        print(lsa_categories)
        print(lsa_counts)


def get_topics_distribution(topic_matrix):
    return topic_matrix.tolist()


def get_best_topic_perdoc(topic_matrix):
    t = get_topics_distribution(topic_matrix)
    for i in range(len (t)):
        lst = t[i]
        indx = 0
        max_val = 0
        for j in range(len(lst)):
            if lst[j] > max_val:
                max_val = lst[j]
                indx = j
        t[i] = indx

    return t


def extract_lda_model(document_term_matrix, n_topics,
                      count_vectorizer,
                      show_plot = False, show_cluster = False):
    lda_model = LatentDirichletAllocation(n_components=n_topics, learning_method='online',
                                          random_state=0, verbose=0)
    lda_topic_matrix = lda_model.fit_transform(document_term_matrix)

    lda_keys = get_keys(lda_topic_matrix)

    lda_categories, lda_counts = keys_to_counts(lda_keys)
    print(lda_categories)
    print(lda_counts)

    top_n_words_lda = get_top_n_words(20, lda_keys, document_term_matrix, count_vectorizer, n_topics)

    print("\nLDA topic words")
    for i in range(len(top_n_words_lda)):
        topic_word_list = top_n_words_lda[i].split()

        print(topic_word_list)

    if show_plot:
        top_3_words = get_top_n_words(3, lda_keys, document_term_matrix, count_vectorizer, n_topics)

        labels = [top_3_words[i] for i in range(len(lda_categories))]

        fig, ax = plt.subplots(figsize=(8, 4))
        ax.bar(lda_categories, lda_counts)
        ax.set_xticks(lda_categories)
        ax.set_xticklabels(labels)
        ax.set_title('LDA Topic Category Counts')
        plt.show()
    if show_cluster:
        colormap = np.array([
            "#1f77b4", "#aec7e8", "#ff7f0e", "#ffbb78", "#2ca02c",
            "#98df8a", "#d62728", "#ff9896", "#9467bd", "#c5b0d5",
            "#8c564b", "#c49c94", "#e377c2", "#f7b6d2", "#7f7f7f",
            "#c7c7c7", "#bcbd22", "#dbdb8d", "#17becf", "#9edae5"])
        colormap = colormap[:n_topics]
        tsne_lda_model = TSNE(n_components=2, perplexity=50, learning_rate=100,
                          n_iter=2000, verbose=1, random_state=0, angle=0.75)
        tsne_lda_vectors = tsne_lda_model.fit_transform(lda_topic_matrix)

        top_3_words_lda = get_top_n_words(3, lda_keys, document_term_matrix, count_vectorizer, n_topics)
        lda_mean_topic_vectors = get_mean_topic_vectors(lda_keys, tsne_lda_vectors, len(tsne_lda_vectors))

        plot = figure(title="t-SNE Clustering of {} LDA Topics".format(n_topics), plot_width=700, plot_height=700)
        plot.scatter(x=tsne_lda_vectors[:, 0], y=tsne_lda_vectors[:, 1], color=colormap[lda_keys])

        for t in range(len(lda_mean_topic_vectors)):
            label = Label(x=lda_mean_topic_vectors[t][0], y=lda_mean_topic_vectors[t][1],
                          text=top_3_words_lda[t], text_color=colormap[t])
            plot.add_layout(label)

        show(plot)

    print(lda_categories)
    print(lda_counts)
    return lda_topic_matrix


def main():
    # best results n_topics 2,(3),6-PRODUCES 5 WITH MAIN 2,
    # 9 - PRODUCES 8 WITH MAIN 2 min_df = 5
    #11 PRODUCES 8 WITH MAIN 3
    n_topics = 11
    # datafile = 'song_keywords_fortopicmodeling.csv'
    datafile = 'country_keywords_fortopicmodeling.csv'
    raw_data = pd.read_csv(datafile)

    reindexed_data = raw_data['words']
    reindexed_data.index = raw_data['UUID']

    # count_vectorizer = TfidfVectorizer(max_df=0.5, min_df=3, binary=True)
    count_vectorizer = TfidfVectorizer(stop_words='english',
                                       min_df=5,binary=True,max_features=1000)
    # test = get_document_term_matrix_asarray(reindexed_data, reindexed_data.index)
    document_term_matrix = get_document_term_matrix(reindexed_data, count_vectorizer)

    # lsa_model(document_term_matrix, n_topics, count_vectorizer )
    lda_topic_matrix = extract_lda_model(document_term_matrix, n_topics,
                                         count_vectorizer, False,False)
    document_topics = get_best_topic_perdoc(lda_topic_matrix)
    doc_id_list = raw_data['UUID'].tolist()

    output_file_name = 'document_topics'+str(n_topics)+'.csv'
    f = open(output_file_name, 'w')
    conn =db_connect()
    if not conn:
        return
    for i in range(len(doc_id_list)):
        doc_id = doc_id_list[i]
        title,author = get_song_name_author_byid(conn,doc_id)

        topic_id = document_topics[i]
        f.write(doc_id+","+title+","+author+","+ str(topic_id)+"\n")

    f.close()





if __name__ == '__main__':
    main()
