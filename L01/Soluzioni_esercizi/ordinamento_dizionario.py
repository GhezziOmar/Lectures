# Nessun import necessario

def main():
    studenti = {
        "Mario": 9, "Bruno": 6, "Carla": 8,
        "Davide": 5, "Elena": 7, "Franco": 9, "Giulia": 6
    }

    lista = []
    for nome, voto in studenti.items():     # coincide con lista = list(studenti.items())
        lista.append((nome, voto))

    n = len(lista)
    
    # Bubble sort
    for i in range(n):  # ripeto il processo di bubbling n volte
        for j in range(n - 1 - i):  # confronto solo la parte ancora non ordinata
            if lista[j][1] < lista[j + 1][1]:   # confronto i voti
                lista[j], lista[j + 1] = lista[j + 1], lista[j]  # scambio le tuple
            elif lista[j][1] == lista[j + 1][1]: #gestione dell'ordinamento lessicografico in caso il voto sia lo stesso
                if lista[j][0] > lista[j + 1][0]:
                    lista[j], lista[j + 1] = lista[j + 1], lista[j]
    
    
    print(f"Dizionario originale: {studenti}")
    print(f"Lista ordinata: {lista}")
    

if __name__ == "__main__":
    main()