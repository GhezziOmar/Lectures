# import numpy as np

def main():
    stringa = input("Inserisci una stringa: ")
    s = stringa.replace(" ", "").lower()

    s_inv = ""
    for i in range(len(s)-1, -1, -1):
        s_inv +=s[i]
    
    if s == s_inv:
        print(f"{stringa} è palindroma")
    else:
        print(f"{stringa} non è palindroma")

if __name__ == "__main__":
    main()