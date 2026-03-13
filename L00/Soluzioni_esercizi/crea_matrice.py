# Nessun import necessario

def main():
    lista = [3, 7, 2, 9, 1, 5, 8, 4, 6, 0, 11, 13, 15, 12, 10, 14]

    matrice = []
    for i in range(4):
        riga = []
        for j in range(4):
            riga.append(lista[i*4+j])
        matrice.append(riga)
    
    print(matrice)


if __name__ == "__main__":
    main()