import numpy as np

def main():
    A = np.array([[1, 2], [3, 4], [5, 6]])
    B = np.array([[6, 7, 8], [9, 10, 11]])

    n = A.shape[0]
    m = B.shape[1]

    C = np.zeros([n, m], dtype=int)

    p = A.shape[1] # deve essere uguale a B.shape[0]

    for i in range(n):
        for j in range(m):
            ps = 0
            for k in range(p):
                ps += A[i, k] * B[k, j]   # avrei potuto scrivere direttamente C[i,j] += A[i, k] * B[k, j] (senza usare ps)
            C[i, j] = ps
    
    print("A x B =")
    print(C)


if __name__ == "__main__":
    main()