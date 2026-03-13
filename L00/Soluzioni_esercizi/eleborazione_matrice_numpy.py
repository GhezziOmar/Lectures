import numpy as np

def main():
    matrice = np.array([
        [3,  10,  2,  4],
        [4,  8,  1,  8],
        [9,  6, 22, 12],
        [12, 21, 1, 7]
    ])

    prima_riga = matrice[0, :]
    prima_colonna = matrice[:, 0]
    diagonale_principale = np.diag(matrice)

    print(f"Prima riga: {prima_riga}")
    print(f"Prima colonna: {prima_colonna}")
    print(f"Diagonale Principale: {diagonale_principale}")

if __name__ == "__main__":
    main()