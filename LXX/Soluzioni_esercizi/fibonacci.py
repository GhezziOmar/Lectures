# import numpy as np

def main():
    n = int(input("Inserisci n: "))

    serie = []
    for i in range(n):
        if i == 0 or i == 1:
            serie.append(i)
        else:
            serie.append(serie[-1] + serie[-2])

    print(f"Serie di Fibonacci fino al termine {n}: {serie}")

if __name__ == "__main__":
    main()