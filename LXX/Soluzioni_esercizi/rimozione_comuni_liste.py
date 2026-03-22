# Nessun import necessario

def main():
    lista1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    lista2 = [2, 4, 6, 8]

    lista1_rimossi = []

    for elemento in lista1:
        if elemento not in lista2:
            lista1_rimossi.append(elemento)

    print(f"lista 1: {lista1}")
    print(f"lista 2: {lista2}")
    print(f"Risultato: {lista1_rimossi}")

if __name__ == "__main__":
    main()