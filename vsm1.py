# -*- coding: utf-8 -*-
"""IR_Test.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1OUsc0lr9C-dHSjQWU3olgAJCgtHz0fcZ
"""

# general concepts
tf
tf vector -> norm. tf - (220, 190, 10)
idf_t = log(N/ df_t)
tf-idf :  wt_term_doc = (1 + log tf_td) * log(N/ df_t)
term - doc incidence
text preprocess - tokenize, normalize, stemming, stop words removal

# set retrival
1. using grep - not efficient  
2. boolean model - answer a boolean query 
3. inverted index 
    steps : doc -> tokenize (token, doc id) -> stemming -> sort tokens ->  form { token : {freq, [postings sorted by doc id]} }
    query processing : and- merge, or, not (Process terms in increasing document frequency)

eval  :
P = P(relevant | retrieved)
R =  P(retrieved | relevant)
F1 = 2PR / P+R


# ranked retrieval
eval : 

# bag of words model

# vector space models
cos. similarity
Simple Matching
Dice’s Coefficient
Jaccard’s Coefficient
euclid. distance
length norm.

import nltk
import itertools
from pprint import pprint
nltk.download('stopwords')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
stop_words = set(stopwords.words("english"))
stemmer = PorterStemmer()

doc = """
Muad'Dib learned rapidly because his first training was in how to learn.
And the first lesson of all was the basic trust that he could learn.
It's shocking to find how many people do not believe they can learn,
and how many more believe learning to be difficult."""

def tokenize(doc):
  return word_tokenize(doc)

def remove_stop_words(l):
  filtered_list = []
  for word in l:
    if word.casefold() not in stop_words:
      filtered_list.append(word)
  return filtered_list

def stem(l):
  return [stemmer.stem(word) for word in l]

def tf(document, term):
  return document.count(term)

def cosineSimilarity(pt1, pt2):
  temp1 = 0
  pt = list(zip(pt1, pt2))
  
  for i in range(len(pt)):
    temp1 += (pt[i][0] * pt[i][1])

  temp2 = 0
  for i in range(len(pt1)):
    temp2 += (pt1[i]**2)
  temp3 = 0
  for i in range(len(pt2)):
    temp3 += (pt2[i]**2)  
  #print(temp3)

  return round( (temp1/((temp2**(0.5))*(temp3**(0.5)))),2)

def euclideanDistance(pt1, pt2):
  pt = list(zip(pt1,pt2))
  temp=0
  
  for i in range(len(pt)):
    temp += (abs(pt[i][0] - pt[i][1]))**2
  return round(((temp) ** (1/2)),2)

def manhattan(pt1, pt2):
  pt = list(zip(pt1,pt2))
  temp=0
  
  for i in range(len(pt)):
    temp += (abs(pt[i][0] - pt[i][1]))
  return temp

def diceSimilarity(pt1, pt2):
  temp1 = 0
  pt = list(zip(pt1, pt2))
  
  for i in range(len(pt)):
    temp1 += (pt[i][0] * pt[i][1])

  temp2 = 0
  for i in range(len(pt1)):
    temp2 += (pt1[i]**2)
  temp3 = 0
  for i in range(len(pt2)):
    temp3 += (pt2[i]**2)  
  #print(temp3)

  return round( ((2*temp1)/((temp2)+(temp3))),2)

def jaccardSimilarity(pt1, pt2):
  temp1 = 0
  pt = list(zip(pt1, pt2))
  
  for i in range(len(pt)):
    temp1 += (pt[i][0] * pt[i][1])

  temp2 = 0
  for i in range(len(pt1)):
    temp2 += (pt1[i]**2)
  temp3 = 0
  for i in range(len(pt2)):
    temp3 += (pt2[i]**2)  
  #print(temp3)

  return round( ((temp1)/(temp2+temp3-temp1)),2)

tokenized_doc = tokenize(doc)
print(tokenized_doc)
filtered_doc = remove_stop_words(tokenized_doc)
stemmed_doc = stem(filtered_doc)
for i in range(len(stemmed_doc)):
  print(filtered_doc[i], "-->", stemmed_doc[i])

data="This is the first word.\nThis is the second text, Hello! How are you?\nThis is the third, this is it now.\nthe ibm dsd technical information center - a total systems approach\ncombining traditional library features\nand mechanized computer processing\ncurrent trends in information science education\nappear inadequate for the important need of the nation's\npracticing professional personnel for training in becoming\ninformation specialists or more proficient users of"

tf(data, 'this')

#f = open("file.txt", "r")
#data = f.read()
#print(data)


data=data.lower()

#remove punctuations
punc = '''!()-[]{};:'"\, <>./?@#$%^&*_~'''
for ele in data:
	if ele in punc:
		data = data.replace(ele, " ")


docs = data.split("\n")

#tokenize and stemming
terms = []
ps = PorterStemmer()
for i in range(len(docs)):
    temp = word_tokenize(docs[i])
    #temp = [ps.stem(i) for i in temp]
    
    docs[i] = [i for i in temp if i not in stop_words]
    terms += docs[i]
terms = list(set(sorted(terms)))
#print(docs)
#print(terms)

docs = [["hello", "hello", "hai","bye"],["bye", "welcome", "bye"],["welcome", "thanks", "thanks"]]
terms=["hello","hai","bye","welcome","thanks"]
#term doc matrix
#inverted matrix

term_doc = {}
inverted = {}
term_doc_freq = {}
for i in terms:
    term_doc[i] = []
    inverted[i] = []
    term_doc_freq[i] = []
    for j in range(len(docs)):
        if i in docs[j]:
            term_doc[i].append(1)
            inverted[i].append(j+1)
            term_doc_freq[i].append(docs[j].count(i))
        else:
            term_doc[i].append(0)
            term_doc_freq[i].append(0)
    
    
#pprint(term_doc)
#pprint(inverted)
pprint(term_doc_freq)

ntf = {}
for i in term_doc_freq:
  temp = term_doc_freq[i]
  max_freq = max(temp)
  ntf[i] = [round(i/max_freq , 2) for i in temp]

pprint(ntf)

d1=[5,3,9,11,1]
q=[2,3,4,1,2]
cos_sim = cosineSimilarity(d1,q)
euc_dis = euclideanDistance(d1,q)
manhat = manhattan(d1,q)
print(cos_sim)
print(euc_dis)
print(manhat)