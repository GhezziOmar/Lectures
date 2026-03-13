# Nessun import necessario

def main():
    n = int(input("Inserisci un numero: "))

    for i in range(10):
        print(f"{i+1} x {n} = {(i+1)*n}")

if __name__ == "__main__":
    main()