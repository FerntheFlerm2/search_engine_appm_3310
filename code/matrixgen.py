from __future__ import print_function
import json
import numpy as np

#nltk imports
import nltk
nltk.data.path.append("/home/gigabyte/Desktop/matrixMethods/project/Info-Retireval-3310/nltk")
nltk.data.path.append("/home/becketth/3310/Info-Retireval-3310/nltk")
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import nltk.stem as stem

from collections import Counter

# filename gets adjusted depending on where the dataset is saved.
filename = "search_spider/demo-data.json"

# the set of words to ignore
stopWords = set(stopwords.words('english'))

# the library to reduce words to their most basic form
stemmer = stem.PorterStemmer()

documents = [] # holds list of document urls, index corresponds to doc's col
words = [] # holds list of words, index corresponds to word's row

matrixArray = []

with open(filename, "r") as file:
    file_data = json.load(file) # extracts JSON data from the file
    for document in file_data["data"]:
        documents.append(document["url"])
        # saves page url in index which corresponds to its column

        doc_words = {}

        doc_raw = word_tokenize(" ".join(document["texts"]).lower())
        # compiles the whole document into one lowercase array of terms.
        for w in doc_raw:
            w = stemmer.stem(w) # reduces the term to its simplest form
            if w not in stopWords: # if not an ignored word
                if w not in doc_words: # if the word has not already been encountered
                    if w.isalpha()==True: # ignore punctuation
                        doc_words[w] = 1 # add the term w/ a count of 1 to this doc's dictionary.
                else: # if it has been encountered
                    doc_words[w] += 1 # increment the count by 1

        column = [] # list for the vector components to be inserted into

        for i in range(len(words)): # iterates over all found words
            if words[i] in doc_words: # if the word is in the doc
                column.append(doc_words[words[i]]) # add its frequency as that word's component
                doc_words.pop(words[i]) # remove the word from the doc's dictionary
            else: # if the word isn't in the doc
                column.append(0) # set that word's component to zero.
            i += 1

        for uncaughtkey in doc_words: # for all novel words in the doc
            words.append(uncaughtkey) # add the word to the list of all words
            column.append(doc_words[uncaughtkey]) # add the frequency as that word's component
        
        norm = np.linalg.norm(column, ord=2) # get the length of the vector
        normed_col = []
        for c in column: # normalize all vector components
            if norm == 0:
                normed_col.append(0) # in case the document was empty (zero vector).
            else:
                normed_col.append(c/norm)

        
        matrixArray.append(normed_col) # add the normalized column to the matrix.
# print(matrixArray)

np.savetxt("documents.txt", documents, delimiter =", ", fmt ="% s") # save documents to text file for later
np.savetxt("words.txt", words, delimiter=", ", fmt="% s") # save words to text file for later

for doc in matrixArray: # the matrix right now is jagged. Ensure that each vector has
                        # as many dimensions as there are words, filling missing
                        # dims with zeros.
    d = (len(words) - len(doc))
    if (d > 0):
        for i in range(d):
            doc.append(0)

# print(matrixArray)

print("+++++++++==")
M = np.transpose(np.array(matrixArray)) # cols are actually rows, fix by transposing.

print(M)

np.savetxt('pre-svd.txt', M) # save matrix for future use.
    
    
