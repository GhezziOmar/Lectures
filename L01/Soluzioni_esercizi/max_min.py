# Nessun import necessario

def main():
    lista = [14, 3, 27, 8, 42, 5, 19, 33, 1, 11]

    minimo = lista[0]
    massimo = minimo

    for elemento in lista:
        if elemento < minimo:
            minimo = elemento
        if elemento > massimo:
            massimo = elemento

    differenza = massimo - minimo

    print(f"Valore massimo: {massimo}")
    print(f"Valore minimo: {minimo}")
    print(f"Differenza: {differenza}")

if __name__ == "__main__":
    main()