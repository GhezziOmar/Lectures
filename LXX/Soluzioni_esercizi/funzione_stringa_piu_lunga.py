# Nessun import necessario

def max_length(lista):
    
    out = lista[0]
    for s in lista:
        if len(s) > len(out):
            out = s
    return out

if __name__ == "__main__":
    print(max_length(["cane", "gatto", "rinoceronte", "topo"]))
    print(max_length(["mela", "banana", "kiwi"]))