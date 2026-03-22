import numpy as np

def main():

    matrice = []
    
    while True:
        riga_stringa = input("Inserisci una riga (oppure . per terminare): ")
        if riga_stringa == '.':
            break
        riga_interi = [int(i) for i in riga_stringa.split()]
        matrice.append(riga_interi)
    
    try:
        matrice_np = np.array(matrice)
        print("Matrice inserita: ")
        print(matrice_np)
    except ValueError:
        print("Errore: le righe hanno lunghezze diverse, impossibile creare la matrice.")

if __name__ == "__main__":
    main()