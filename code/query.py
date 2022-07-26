import numpy as np

import nltk.stem as stem

# the library to reduce words to their most basic form
stemmer = stem.PorterStemmer()

# loads the document and word arrays
documents = np.loadtxt('documents.txt', dtype=str, delimiter='\n')
words = np.loadtxt('words.txt', dtype=str, delimiter='\n')

# loads the components of the reduced SVD and the final matrix
U = np.loadtxt('U-appx.txt')
D = np.loadtxt('D-appx.txt')
V_t = np.loadtxt('Vt-appx.txt')
rankAppx = np.loadtxt('rank-appx.txt')

# query function
def query(querytext):

    query = [] # array to hold the vector form of the query

    # splits the query string into an array,
    # reduces the words to their most basic form
    # and saves them in the stemmed list.
    s = querytext.split()
    stemmed = []
    for ss in s:
        stemmed.append(stemmer.stem(ss.lower()))

    # iterates through all the words in the corpus. If the word is in the query,
    # that word's dimension is set to 1 in the query vector. If not, zero.
    for i in range(len(words)):
        if words[i] in stemmed:
            query.append(1)
        else:
            query.append(0)
    
    # converted to a column vector.
    query = np.transpose(query)

    # list to hold the cosine values for each document (in order)
    similarities = []

    # for every document vector
    for col in range(rankAppx.shape[1]):
        # creates vector corresponding to index-matrix column of index-matrix
        # of size dxd where d is the number of documents
        e = np.zeros(rankAppx.shape[1])
        e[col] = 1
        e = np.transpose([e])

        # gets transpose of V_t
        V = np.transpose(V_t)

        # gets transpose of U
        U_t = np.transpose(U)

        # calculates the numerator and denominator in the cosine equation.
        num = np.matmul(np.matmul(np.matmul(np.transpose(e), V), D), np.matmul(U_t, query))
        denom = np.linalg.norm(np.matmul(np.matmul(D, V_t), e), ord=2) * np.linalg.norm(query, ord=2)

        if denom == 0: # avoid divide by zero
            costheta = [-1] # if divide by zero, assign cosine of least relevance
        else:
            costheta = num/denom

        # add the costheta value at the index corresponding to its document.
        similarities.append(costheta[0])

    return similarities # return results

# run query and save cosine values in order (for example query "monkey")
resp = query("monkey")

# array for tuples of cosine value and document URL/title
results = []
i = 0
for res in resp: # iterate through all the cosine values
    if res > -2: # sanity check
        results.append((res, documents[i]))
    i += 1

# sort the results by cosine value
results = sorted(results, key = lambda x: x[0])

# print the results to the terminal
for result in results:
    print(str(result[0]) + " :: " + str(result[1]))

# save the results for later
np.savetxt("results.txt", results, delimiter=", ", fmt="% s")


