#  Data analysis pipeline

### 1. Create input for lda topic modeling

Run list_word_per_song.py to create for each song a tuple of
song UUID and a string of distinct words separated with space.
Written into a file song_keywords_fortopicmodeling.csv,
this is the input for lds and lsa topic modeling

Run list_word_per_country.py to create for each country a tuple
of country name and a string of distinct words separated with space.
Written into a file country_keywords_fortopicmodeling.csv,
this can also be used as input for lds and lsa topic modeling

Run:
python list_word_per_song.py
Or
python list_word_per_country.py


### 2. Run lda topic modeling

Script lda_topic_extraction.py takes document data
from song_keywords_fortopicmodeling.csv or country_keywords_fortopicmodeling.csv, extracts specified number of topics
from tf-idf term vectors, and produces topic-document matrix,
which specifies topic distribution for each document.

The separation can be tested by plotting the document clusters in 2D,
using a dimensionality-reduction technique called  t-SNE
(https://www.kaggle.com/rcushen/topic-modelling-with-lsa-and-lda).

Next, it assigns the topic to each document by taking max of
topic score, and writes the results into document_topics11.csv,
where 11 is the selected number of topics.


Note that the resulting number of topics
can be less than what we wanted.



### 3. Name lyrics properly
In order to be able to look at actual songs and understand
differences in songs classified as different topics, run
script name_lyrics_files.py, specify input folder,
where the songs are named by uuid, and output folder to store
the same lyrics files titled with song name and author.



### 4. Topic distribution per country

Run script topics_per_country.py, which will
summarize the number of songs per each topic category for
each country. The result is in country_topics.csv.
This can be visualized with Excel, as for example in
country_topics_charts.xlsx.



### 5. Clustering countries by lyrics

Run script clustering_inputs.py, which creates two .tsv files: count_cluster_input.tsv, which entries are the counts of each words appears in each country and tfidf_cluster_input.tsv, which entries are the tf-idf scores of each word in each country inside the directory 'clustering'. 
Then in the directory 'clustering', hcluster.py performs hierarchical clustering and takes a .tsv file as input parameter, and kmcluster.py performs k-mean clustering and takes a .tsv file and a integer that represents the number of clusters wanted as input parameters. 

Run:
python clustering_inputs.py
python hcluster.py  count_cluster_input.tsv or
python hcluster.py  tfidf_cluster_input.tsv or
python kmcluster.py count_cluster_input.tsv 3 or
python kmcluster.py tfidf_cluster_input.tsv 3



### 6. Create js data file for heat map visualization 
Run script top_k_words.py with an integer that specifies k as input parameter. This creates js data files for creating the heat map: data_tfidf.js, words_tfidf.js, data_count.js, words_count.js
Run: python top_k_words.py 10

