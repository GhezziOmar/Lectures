# Nessun import necessario

def main():
    lista = [3, 7, 2, 7, 1, 3, 9, 2, 5, 1, 8, 3]

    elementi_unici = []
    for elemento in lista:
        if elemento not in elementi_unici:
            elementi_unici.append(elemento)
    
    print(f"Lista originale: {lista}")
    print(f"Lista senza duplicati: {elementi_unici}")

if __name__ == "__main__":
    main()