import nltk
import itertools
from pprint import pprint
nltk.download('stopwords')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
stop_words = set(stopwords.words("english"))
stemmer = PorterStemmer()



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

  
  
  
  
