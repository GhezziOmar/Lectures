# import numpy as np

def main():
    n = int(input("Inserisci n: "))

    somma_divisori = 0

    for i in range(1, n):
        if n%i == 0:
            somma_divisori += i

    if n == 0:
        print(f"{n} non è un numero perfetto")
    elif somma_divisori == n:
        print(f"{n} è un numero perfetto")
    else:
        print(f"{n} non è un numero perfetto")

if __name__ == "__main__":
    main()