import nltk, re, pprint
import enchant
dict = enchant.Dict("en_US")
# nltk.download('punkt')
nltk.download('wordnet')
from nltk import word_tokenize

f = open('test1.txt', encoding='utf-8')
raw = f.read()

#replace all non-letter characters with spaces
m = map(lambda x: x.lower() if x.isalpha() else ' ', raw)
#convert from list of letters to string
clean_str = "".join(list(m))

# only work with words which are in the dictionary
tokens = list(
    filter(
            lambda x: True if len(x) > 2 and dict.check(x) else False,list(set(clean_str.split()))
    ))

print(len(tokens))

print(tokens)

porter = nltk.PorterStemmer()
lancaster = nltk.LancasterStemmer()
print([porter.stem(t) for t in tokens])

print([lancaster.stem(t) for t in tokens])

wnl = nltk.WordNetLemmatizer()
print([wnl.lemmatize(t) for t in tokens])