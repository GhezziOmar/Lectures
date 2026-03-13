# Nessun import necessario

def main():
    base = float(input("Inserisci la base: "))
    altezza = float(input("Inserisci l'altezza: "))

    area = base * altezza
    perimetro = 2 * (base + altezza)
    print(f"L'area del rettangolo è: {area}, il perimetro è: {perimetro}") 

if __name__ == '__main__':
    main()