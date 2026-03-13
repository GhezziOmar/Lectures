import numpy as np

def main():
    lista = [3, 7, 2, 9, 1, 5, 8, 4, 6, 0, 11, 13, 15, 12, 10, 14]

    matrice = np.zeros([4, 4], dtype=int)

    for i in range(4):
        for j in range(4):
            matrice[i,j] = lista[i*4+j]
    
    print(matrice)

if __name__ == "__main__":
    main()