# Nessun import necessario

def main():
    lista = [4, 12, 7, 3, 19, 8, 25, 1, 14, 6, 11, 17, 2, 9, 22]

    a = int(input("Inserisci il valore minimo dell'intervallo: "))
    b = int(input("Inserisci il valore massimo dell'intervallo: "))

    count = 0
    for elemento in lista:
        if elemento >= a and elemento <= b:
            count += 1

    print(f"Elementi compresi tra {a} e {b}: {count}")


if __name__ == "__main__":
    main()