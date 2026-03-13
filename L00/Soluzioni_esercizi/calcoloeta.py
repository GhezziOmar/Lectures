import numpy as np

def main():
    eta1 = int(input("Età persona 1: "))
    eta2 = int(input("Età persona 2: "))

    somma = np.sum([eta1, eta2])
    media = np.mean([eta1, eta2])
    media_difetto = np.floor(media)
    media_eccesso = np.ceil(media)

    somma_piu_10_per_persona = somma + 20
    media_piu_10_per_persona = media + (20 // 2)

    print(f"Somma età: {somma}")
    print(f"Media età: {media}")
    print(f"Media arrotondata per difetto: {media_difetto}")
    print(f"Media arrotondata per eccesso: {media_eccesso}")

    print(f"Somma età fra 10 anni: {somma_piu_10_per_persona}")
    print(f"Media età fra 10 anni: {media_piu_10_per_persona}")

if __name__ == '__main__':
    main()