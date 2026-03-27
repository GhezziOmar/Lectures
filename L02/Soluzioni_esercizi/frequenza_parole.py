# import numpy as np

def main():
    testo = "il gatto è sul tetto il tetto è alto il gatto guarda il cielo il cielo è blu"

    freq = {}
    for parola in testo.split():
        if parola in freq:
            freq[parola] +=1
        else:
            freq[parola] = 1
    
    lista = []
    for key, value in freq.items():
        lista.append((key, value))
    
    n = len(lista)

    for i in range(n):
        for j in range(n-1-i):
            if lista[j][1] < lista[j+1][1]:
                lista[j], lista[j+1] = lista[j+1], lista[j]

    print(lista)
        

if __name__ == "__main__":
    main()