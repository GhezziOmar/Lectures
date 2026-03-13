import numpy as np

def norma(v):
    norma = np.sqrt(np.sum(v**2))
    if norma == 0:
        raise ValueError("Vettore di norma nulla!")
    return norma

def main():
    v = np.array([3.0, 4.0, 0.0, 0.0])
    n = norma(v)
    v_normalizzato = v / n

    print(f"Vettore originale: {v}")
    print(f"Norma: {n}")
    print(f"Vettore originale: {v_normalizzato}")

if __name__ == "__main__":
    main()