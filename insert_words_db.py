import nltk
# nltk.download('punkt')
# nltk.download('wordnet')
import sys
import operator
import glob
import os
import io
import pickle
import enchant
import pprint
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from song_vocabulary import *
from general_db import *

'''
To run: python insert_words_db.py 20180726/
'''

l = WordNetLemmatizer()
d = enchant.Dict("en_US")

'''
For each lyrics file, tokenize lyrics
check if each word is in vocabulary and
produce triple (file_id, word, frequency)
to insert into db
'''
def process_lyrics_files(db_connection, vocabulary, folder_name, date=None):
    path =''
    if date:
        path = date+'/'
    path = path + folder_name + '/*.txt'
    files = glob.glob(path)
    db_connection.isolation_level = None
    try:
        db_connection.execute("begin")
        c = db_connection.cursor()

    except lite.Error as e:
        print("Transaction failed: {0}".format(e))
        if db_connection:
            db_connection.execute("rollback")
        return

    for file in files:
        fileUUID = file[len(file)-40:len(file)-4]
        with codecs.open(file, "r", encoding='utf-8', errors='replace') as input:
            lyrics = input.read()
        word_list = clean_and_parse(lyrics)
        word_dictionary = {}
        for w in word_list:
            if w in vocabulary:
                if w not in word_dictionary:
                    word_dictionary[w] = 1
                else:
                    word_dictionary[w] += 1
        for word,count in word_dictionary.items():
            sql = "INSERT or REPLACE INTO word_count(songUUID, word, frequency) VALUES(?, ?, ?)"
            params = (fileUUID, word, count)
            try:
                result = c.execute(sql, params)
            except lite.Error as e:
                print("Transaction failed: {0}".format(e))
                if db_connection:
                    db_connection.execute("rollback")
                return
    try:
        db_connection.execute("commit")
    except db_connection.Error:
        print("failed!")
        if db_connection:
            db_connection.execute("rollback")
        return

def main():
    # 'lyricsTranslated20180726/*.txt'
    folder_name = sys.argv[1]
    con = db_connect()
    if not con:
        return
    con.execute('DELETE FROM word_count')
    con.commit()

    vocabulary = set()

    f = open('research_vocabulary.csv', 'r', encoding='utf-8', errors='replace')
    words = f.readlines()
    words = [x.strip() for x in words]
    for w in words:
        vocabulary.add(w)
    process_lyrics_files(con, vocabulary, folder_name)


if __name__ == "__main__":
    main()
