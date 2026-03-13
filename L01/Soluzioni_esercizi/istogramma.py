# Nessun import necessario

def main():
    voti = [6, 8, 7, 9, 6, 7, 8, 6, 10, 7, 9, 8, 7, 6, 8]

    freq = {}
    for v in voti:
        if v in freq:
            freq[v] += 1
        else:
            freq[v] = 1
    
    lista = []
    for key, value in freq.items():
        lista.append((key, value))
    
    n = len(lista)
    
    for i in range(n):
        for j in range(n - 1 - i):
            if lista[j][0] > lista[j + 1][0]:
                lista[j], lista[j + 1] = lista[j + 1], lista[j]
    
    for i in range(n):
        barra = "*" * lista[i][1]
        print(f"{lista[i][0]}: {barra}")
            

if __name__ == "__main__":
    main()