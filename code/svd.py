import numpy as np

A = np.loadtxt('pre-svd.txt', dtype=float) # load the term-document matrix

print("Loaded matrix.")
# print(A)

U, first_D, V_t = np.linalg.svd(A) # perform SVD on the matrix

print("Svd complete.")

# the D matrix is returned as a string
# this converts it to a diagonalized matrix
D = np.zeros((U.shape[1], V_t.shape[0]))
D[:first_D.size, :first_D.size] = np.diag(first_D)

np.savetxt('D-full.txt', D)

print("Reducing rank.")

# the rank to reduce the matrix to.
# 3 for the example dataset
# 400 for the CU website dataset
rank = 3

# perform rank reduction on the matrix components
U = np.delete(U, slice(rank, U.shape[1]), axis=1)
D = np.delete(D, slice(rank, D.shape[1]), axis=1)
D = np.delete(D, slice(rank, D.shape[0]), axis=0)
V_t = np.delete(V_t, slice(rank, V_t.shape[0]), axis=0)

print("Rank appx:")
rankAppx = np.matmul(U, np.matmul(D, V_t)) # finds the A_k matrix.

print(rankAppx)

# saves all useful components for later.
np.savetxt('rank-appx.txt', rankAppx)
np.savetxt('U-appx.txt', U)
np.savetxt('D-appx.txt', D)
np.savetxt('Vt-appx.txt', V_t)





