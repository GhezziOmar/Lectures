import numpy as np

def main():
    v = np.array([1, 2, 3, 4])
    w = np.array([5, 6, 7, 8])

    ps = 0
    for i in range(len(v)):
        ps += v[i] * w[i]
    
    print(v)
    print(w)
    print(f"Prodotto scalare: {ps}")


if __name__ == '__main__':
    main()