# Nessun import necessario

def main():
    parola_1 = input("Inserisci la prima parola: ")
    parola_2 = input("Inserisci la seconda parola: ")

    freq_p1 = {}
    for c in parola_1.lower():
        if c in freq_p1:
            freq_p1[c]+=1
        else:
            freq_p1[c]=1
    
    freq_p2 = {}
    for c in parola_2.lower():
        if c in freq_p2:
            freq_p2[c]+=1
        else:
            freq_p2[c]=1
    
    if freq_p1 == freq_p2:
        print(f"\"{parola_1}\" e \"{parola_2}\" sono anagrammi")
    else:
        print(f"\"{parola_1}\" e \"{parola_2}\" non sono anagrammi")

if __name__ == "__main__":
    main()