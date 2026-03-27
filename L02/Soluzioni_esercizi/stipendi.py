import pandas as pd

def main():
    df = pd.DataFrame({
        "Nome":     ["Alice", "Bruno", "Carla", "Davide", "Elena", "Franco", "Giulia"],
        "Reparto":  ["IT", "HR", "IT", "Vendite", "HR", "Vendite", "IT"],
        "Stipendio": [3200, 2800, 3500, 2600, 2900, 3100, 3300]
    })

    stats = ["mean", "max", "min", "sum"]

    df_reparto = df.groupby("Reparto")["Stipendio"].agg(stats).reset_index()
    idx = df_reparto["sum"].idxmax()
    reparto_top = df_reparto.loc[idx, "Reparto"]
    totale_reparto_top = df_reparto.loc[idx, "sum"]

    print("Stipendi dipendenti per reparto: ")
    print(df.to_string() + "\n")

    print("Statistiche per reparto: ")
    print(df_reparto.to_string() + "\n")

    print(f"Reparto con somma stipendi più alta: {reparto_top} ({totale_reparto_top})")

if __name__ == "__main__":
    main()