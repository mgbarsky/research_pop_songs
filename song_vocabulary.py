import sys
import os
import codecs
import nltk, re, pprint
import enchant
en_dict = enchant.Dict("en_US")
# nltk.download('punkt')
# nltk.download('wordnet')
from nltk import word_tokenize

def clean_and_parse(str_data):
    # replace all non-letter characters with spaces
    m = map(lambda x: x.lower() if x.isalpha() else ' ', str_data)
    # convert from list of letters to string
    clean_str = "".join(list(m))

    tokens = clean_str.split()
    # only work with words which are in the dictionary
    tokens = list(
        filter(lambda x: True if en_dict.check(x) else False, tokens)
    )

    # remove min stop words (combined nltk and clustering - selection)
    f = open("songs_stop_words.csv", "r")
    stop_words = set(f.read().splitlines())

    tokens = list(
        filter(
            lambda x: True if x not in stop_words else False, tokens)
    )

    wnl = nltk.WordNetLemmatizer()

    tokens = list(
        filter(
            lambda x: True if x not in stop_words else False, [wnl.lemmatize(t) for t in tokens])
    )

    return tokens


def add_to_vocabulary(vocab, words_list):
    for word in words_list:
        vocab.add(word.strip())


def main():
    if len(sys.argv) < 2:
        print("Please specify directory to process")
        return

    songs_dir = sys.argv[1]

    vocab_set = set()

    try:
        directory = os.fsencode(songs_dir)
    except (FileNotFoundError, IOError):
        print("No such directory", songs_dir)
        return

    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        with codecs.open(file_path, "r", encoding='utf-8', errors='replace') as data:
            raw_text = data.read()
        words_list_all = clean_and_parse(raw_text)
        add_to_vocabulary (vocab_set, words_list_all)
        data.close()

    with codecs.open("research_vocabulary.csv", "w") as fwrite:
        for word in vocab_set:
            fwrite.write(word)
            fwrite.write('\n')

        fwrite.close()


if __name__ == "__main__":
    main()



