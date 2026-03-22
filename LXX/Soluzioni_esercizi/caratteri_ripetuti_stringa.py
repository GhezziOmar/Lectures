# Nessun import necessario

def main():
    stringa = "thequickbrownfoxjumpsoverthelazydog"

    caratteri_ripetuti = {}
    for c in stringa:
        if c in caratteri_ripetuti:
            caratteri_ripetuti[c] += 1
        else:
            caratteri_ripetuti[c] = 1

    lista_tuple = []
    for key, value in caratteri_ripetuti.items():
        if value > 1:
            lista_tuple.append((key, value))
    
    for i in range(len(lista_tuple)):
        for j in range(len(lista_tuple) - 1 - i):
            if lista_tuple[j][1] < lista_tuple[j+1][1]:
                lista_tuple[j], lista_tuple[j+1] = lista_tuple[j+1], lista_tuple[j]
    
    for i in range(len(lista_tuple)):
        print(f"{lista_tuple[i][0]} {lista_tuple[i][1]}")      

if __name__ == "__main__":
    main()