import numpy as np

def main():
    matrice = np.array([[3, 7], [2, 5]])

    determinante = matrice[0,0] * matrice[1,1] - (matrice[0,1]*matrice[1,0])

    print(f"Il determinante della matrice è: {determinante}")

if __name__ == '__main__':
    main()