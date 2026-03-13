# Nessun import necessario

def main():
    n = int(input("Inserisci un numero: "))

    if n % 2 == 0:
        print(f"{n} è pari")
    else:
        print(f"{n} è dispari")

if __name__ == "__main__":
    main()