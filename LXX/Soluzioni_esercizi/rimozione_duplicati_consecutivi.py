# Nessun import necessario

def main():
    lista = [1, 1, 2, 3, 3, 3, 4, 4, 5, 1, 1, 6, 6]

    elementi_unici_consecutivi = []

    for i in range(len(lista)-1):
        if lista[i] != lista[i+1]:
             elementi_unici_consecutivi.append(lista[i])
    
    #if lista[-1] != elementi_unici_consecutivi[-1]:
    #    elementi_unici_consecutivi.append(lista[-1])
    elementi_unici_consecutivi.append(lista[-1])

    print(f"Lista originale: {lista}")
    print(f"Lista senza duplicati consecutivi: {elementi_unici_consecutivi}")

if __name__ == "__main__":
    main()