import numpy as np



aux = np.asarray([[1, 1, 1, 1, 1],
                   [1, 1, 1, 0, 0],
                   [1, 0, 0, 1, 1],
                   [0, 1, 1, 0, 1],
                   [1, 0, 1, 1, 1]])

print(aux)
print(np.sum(aux,0))
print(aux.shape)