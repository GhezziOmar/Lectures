# Nessun import necessario

def somma_div_dispari(N):

    sum = 0
    for i in range(1, N+1):
        if N % i == 0 and i % 2 !=0:
            sum += i
    
    return sum


if __name__ == "__main__":
    print(somma_div_dispari(21))
    print(somma_div_dispari(18))