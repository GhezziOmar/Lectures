import numpy as np

def main():
    raggio = float(input("Inserisci il raggio: "))

    area = (raggio ** 2) * np.pi
    circonferenza = 2 * raggio * np.pi

    print(f"L'area del cerchio è: {area:.3f}, la circonferenza è: {circonferenza:.3f}")

if __name__ == "__main__":
    main()