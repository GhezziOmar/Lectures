import numpy as np

def main():
    matrice = np.array([
        [1, 2, 3],
        [4, 5, 6]
    ])

    n, m = matrice.shape

    matrice_t = np.zeros([m, n], dtype=int)

    for i in range(n):
        for j in range(m):
            matrice_t[j, i] = matrice[i, j]
    
    print(f"Matrice originale ({n}x{m}):")
    print(matrice)
    print(f"Matrica trasposta ({matrice_t.shape[0]}x{matrice_t.shape[1]})")
    print(matrice_t)

if __name__ == "__main__":
    main()