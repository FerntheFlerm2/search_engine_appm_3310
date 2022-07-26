import numpy as np

# load the original, pre-rank-reduced matrix from SVD.
D = np.loadtxt('D-full-big.txt')

# set the maximum possible rank
rank = len(D)
# set the perfect ratio
ratio = 0

# perform the algorithm rom section 4.4.3.
# minimum rank of one and max ratio of .4
while rank > 1 and ratio < .4:
    rank -= 1 # reduce rank by one
    denom = 0
    # sum squares of singular values up to rank
    for i in range(rank):
        denom += (D[i][i])^2
    # take square root
    denom = np.sqrt(denom)

    num = 0
    # sum squares of singular values after rank
    for i in range (rank, len(D)):
        num += (D[i][i])^2
    # take square root
    num = np.sqrt(num)

    # calculate ratio
    ratio = num/denom

# return the correct rank.
print(str(ratio) + " at rank "+ str(rank))

