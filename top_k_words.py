from count_utils import *
from tfidf_utils import *
import json
import sys

if __name__=='__main__':
    word_list, tfidf_score, tfidf_top_words = create_tfidf_input_for_website(sys.argv[1])
    with open('songs_website/word_tfidf/js/data_tfidf.js', 'w') as js_file:
        js_file.write('var data = ')
        json.dump(tfidf_score, js_file)
    with open('songs_website/word_tfidf/js/words_tfidf.js', 'w') as js_file:
        js_file.write('var words = ')
        json.dump(word_list, js_file)
    with open('songs_website/word_tfidf/js/country_top_words.js', 'w') as js_file:
        js_file.write('var top_words = ')
        temp = []
        for key, value in tfidf_top_words.items():
            temp.append([key]+value)
        json.dump(temp, js_file)

    words, country_fre,  country_top_words = create_count_input_for_website(sys.argv[1])
    with open('songs_website/word_counts/js/data_count.js', 'w') as js_file:
        js_file.write('var data = ')
        array2D = []
        for key, value in country_fre.items():
            array2D.append([key]+value)
        json.dump(array2D, js_file)
    with open('songs_website/word_counts/js/words_count.js', 'w') as js_file:
        js_file.write('var words = ')
        json.dump(words, js_file)
    with open('songs_website/word_counts/js/country_top_words.js', 'w') as js_file:
        js_file.write('var top_words = ')
        array2D = []
        for key, value in country_top_words.items():
            array2D.append([key]+value)
        json.dump(array2D, js_file)
