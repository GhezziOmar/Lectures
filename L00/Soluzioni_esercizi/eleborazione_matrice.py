# Nessun import necessario

def main():
    matrice = [
        [3,  10,  2,  4],
        [4,  8,  1,  8],
        [9,  6, 22, 12],
        [12, 21, 1, 7]
    ]

    prima_riga = matrice[0]

    prima_colonna = []
    for i in range(len(matrice)):
        prima_colonna.append(matrice[i][0])
    
    diagonale_principale = []
    for i in range(len(matrice)):
        diagonale_principale.append(matrice[i][i])
    
    print(f"Prima riga: {prima_riga}")
    print(f"Prima colonna: {prima_colonna}")
    print(f"Diagonale Principale: {diagonale_principale}")


if __name__ == "__main__":
    main()