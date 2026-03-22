# Nessun import necessario

def main():
    n = int(input("Inserisci n: "))

    setaccio = list(range(2, n +1))
    primi = []

    while setaccio: # finché ci sono numeri da esaminare nel setaccio
        primo = setaccio[0]
        primi.append(primo)

        nuovo_setaccio = []
        for numero in setaccio:
            if numero % primo != 0:
                nuovo_setaccio.append(numero)
        setaccio = nuovo_setaccio
    
    print(f"Numeri primi fino a {n}: {primi}")


if __name__ == "__main__":
    main()