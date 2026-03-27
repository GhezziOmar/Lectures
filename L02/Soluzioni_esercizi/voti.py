import pandas as pd

def main():

    df = pd.DataFrame({
        "Studente": ["Alice", "Bruno", "Carla", "Davide", "Elena"],
        "Matematica": [8, 6, 9, 5, 7],
        "Fisica":     [7, 5, 8, 6, 9],
        "Informatica":[9, 7, 6, 8, 8]
    })

    materie = ["Matematica", "Fisica", "Informatica"]

    df["Media studente"] = df[materie].mean(axis=1).round(2)
    media_materie = df[materie].mean(axis=0)

    voto_max = df[materie].max().max()
    voto_min = df[materie].min().min()

    print("DataFrame con media per studente:")
    print(df.to_string() + "\n")

    print("Media per materia:")
    print(media_materie.to_string() + "\n")

    print(f"Voto massimo: {voto_max}")
    print(f"Voto minimo: {voto_min}")

if __name__ == "__main__":
    main()