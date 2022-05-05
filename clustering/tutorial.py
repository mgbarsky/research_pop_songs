from __future__ import print_function
from stopwords import *
import sys

debug=1
def readfile(filename):
  f=open(filename,'r')
  ret=f.read()
  f.close()
  return ret

def printarraytofile( arr2D,filename):

  sys.stdout = open(filename,'w')

  for i in range (0,len(arr2D)-1):
    line=arr2D[i]
    for j in range (0, len(line)-1):
      print (line[j],'\t',)

    print (line[len(line)-1],'\n')


  lastline=arr2D[len(arr2D)-1]
  for j in range (0, len(lastline)-1):
    print (lastline[j],'\t',)

  print (lastline[len(lastline)-1])


  sys.stdout=sys.__stdout__

def getdocumentvectors(filename):
  f=open(filename,'r')
  rdata=f.read()
  f.close()
  lines=rdata.split('\n')

  vectorsdict={}
  for i in range(1,len(lines)):
    items=lines[i].split('\t')
    if(len (items)>1):
      vector=[]
      for j in range (1, len(items)):
        vector.append(int(items[j]))
      vectorsdict[items[0].strip()]=vector

  return vectorsdict


def getwordvectors(filename):
  f=open(filename,'r')
  rdata=f.read()
  f.close()
  lines=rdata.split('\n')

  vectorsdict={}

  words=lines[0].split('\t')
  for i in range (1, len(words)):
    vector=[]
    for j in range (1,len(lines)):
      freqs=lines[j].split('\t')
      if len(freqs)>1:
        vector.append(int (freqs[i].strip()))
    vectorsdict[words[i].strip()]=vector

  return vectorsdict

def parsetitles (txt):
  wordvectors={}
  for line in txt.split('\n'):
    tokens=line.lower().split()
    wordvectors[tokens[0]]=tokens[1:]

  return wordvectors

def getwordfrequencies(dict):
  wordcounts={}
  for doc,words in dict.items():

    for word in words:
      if word not in stopwords:
        if word not in wordcounts:
            wordcounts[word]=1
        else:
            wordcounts[word]+=1
  return wordcounts

def generate_word_doc_matrix (wordsindocs,wordslist):
  retmatrix=[]
  firstline=[]

  firstline.append('items')
  wordpos=1
  wordpositions={}

  for word in wordslist:
    firstline.append(word)
    wordpositions[word]=wordpos
    wordpos+=1

  retmatrix.append(firstline)
  totalitems=wordpos


  for doc, words in  wordsindocs.items():
    line=[]
    line.append(doc)
    for i in range (1,totalitems):
      line.append(0)

    for word in words:
      if word in wordslist:
        line[wordpositions[word]]+=1

    retmatrix.append(line)

  return retmatrix

if __name__=='__main__':
  txt=readfile('titles.txt')

  wordsintitles=parsetitles (txt)
  if debug==1:
    for doc,words in wordsintitles.items():
      print (doc,)
      print (': ',)
      print (words)

  #create dictionary of all words (universe)
  allwords=getwordfrequencies(wordsintitles)

  for word, frequency in allwords.items():
    if debug==1:
      print (word, ': ', frequency)

  #generate list of words with frequency more than 1
  worddimensions=[]
  for word, frequency in allwords.items():
    if frequency > 1:
      worddimensions.append(word)
  if debug==1:
    print (worddimensions)

  wordtitlesmatrix=generate_word_doc_matrix (wordsintitles,worddimensions)
  if debug==1:
    print (wordtitlesmatrix)

  printarraytofile(wordtitlesmatrix,'titlesdata.txt')
