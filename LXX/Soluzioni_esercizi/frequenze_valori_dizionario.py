# nessun import necessario

def main():
    dizionario = {
        'V': 10, 'VI': 10, 'VII': 40, 'VIII': 20,
        'IX': 70, 'X': 80, 'XI': 40, 'XII': 20, 'XIII': 10
    }

    freq_valori = {}
    for key, value in dizionario.items():
        if value in freq_valori:
            freq_valori[value] += 1
        else:
            freq_valori[value] = 1
    
    lista_tuple = []
    for key, value in freq_valori.items():
        lista_tuple.append((key, value))
    
    for i in range(len(lista_tuple)):
        for j in range(len(lista_tuple) - 1 - i):
            if lista_tuple[j][1] < lista_tuple[j+1][1]:
                lista_tuple[j], lista_tuple[j+1] = lista_tuple[j+1], lista_tuple[j]
    
    for i in range(len(lista_tuple)):
        print(f"{lista_tuple[i][0]} {lista_tuple[i][1]}")   

if __name__ == "__main__":
    main()