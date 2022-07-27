# Information Retrieval Project for Matrix Methods
We scrape CU Boulder's website and implement a vector space model for intersite queries.

The paper is under `main.pdf`. See the [repo](https://github.com/BeckettHydeCU/Info-Retireval-3310) for the code which we both worked on. 

Project by [FerntheFlerm2](https://github.com/FerntheFlerm2) and [BeckettHydeCU](https://github.com/BeckettHydeCU)


# Overview:
Note this is very high level with implementation details which help
for performance left out, the paper is a better reference.

### Sitemap Generation
First we use sitemap-generator (node.js package) to generate
a sitemap of links to pages on the CU website by crawling four layers deep from the
homepage www.colorado.edu.

### Text Data Gathering
Then we use scrapy to save the links and their corresponding text in a JSON file. 

### Term-Document Matrix Generation
For each document we:

1. Scan the document and record the frequency of every word that appears.
In this process we stem (convert words to their most generic form i.e. "baking" -> "bake"), filter out common words, and lowercase all words using the nltk library in python. 

2. Generate a vector for the document by going through the global dictionary, and if the term is present in the document the frequency of the term is appended to the corresponding component, and if that term is not, a zero is appended.

3. Add any new words in the document which were not in the global dictionary to the global dictionary.

Finally since we have vectors of varying sizes, since for each document with new words, additional components are added to its vector that were not needed for previous vectors.
We append zeroes to make all vectors to make then match the size of the final document vector created.


### Rank Choice Generation
As it would be too computationally intensive to use the entire matrix for querying, we must
use a rank approximation. To do this we need to pick an appropriate rank
to ensure we do not lose too much information. Thus, we compute the ratio of the difference in size between the datbase matrix's singular value decompositon (SVD) and the approximation, using the Frobenius norm, reducing the rank used until the ratio becomes too high. 

### Rank-k Matrix Approximation
Next we generate the approximation using the SVD of the full matrix. 

### Querying
Finally we generate results for a given query. To do this we stem, filter, and lower case the query. Then, we generate a query vector in the manner described above, and calculate the cosine of the angle between the vector and each document. The documents corresponding to the top 10 largest cosines (meaning the most similar vectors) are returned.



