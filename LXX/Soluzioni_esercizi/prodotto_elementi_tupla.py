# nessun import necessario

def prodotto_elementi(tupla):

    prodotto = 1
    for elemento in tupla:
        prodotto *= elemento

    return prodotto

def main():
    tupla1 = (4, 3, 2, 2, -1, 18)
    tupla2 = (2, 4, 8, 8, 3, 2, 9)

    print(f"Tupla 1: {tupla1} , Prodotto: {prodotto_elementi(tupla1)}")
    print(f"Tupla 2: {tupla2} , Prodotto: {prodotto_elementi(tupla2)}")

if __name__ == "__main__":
    main()