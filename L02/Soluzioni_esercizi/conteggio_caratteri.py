# import numpy as np

VOCALI = "aeiou"

def main():
    stringa = input("Inserisci una stringa: ")

    conteggio = {"Vocali" : 0, "Consonanti": 0, "Spazi" : 0, "Caratteri speciali": 0}

    for c in stringa.lower():
        if c in VOCALI:
            conteggio["Vocali"] += 1
        elif c == " ":
            conteggio["Spazi"] += 1
        elif c.isalpha():
            conteggio["Consonanti"] += 1
        else:
            conteggio["Caratteri speciali"] += 1
    
    for key, value in conteggio.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    main()