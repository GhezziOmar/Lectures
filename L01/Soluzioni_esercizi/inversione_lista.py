# Nessun import necessario

def main():
    lista = [10, 20, 30, 40, 50, 60, 70]

    lista_inv = []
    for i in range(len(lista)-1 , -1, -1):
        lista_inv.append(lista[i])
    
    print(f"Lista originale: {lista}")
    print(f"Lista invertita: {lista_inv}")


if __name__ == '__main__':
    main()