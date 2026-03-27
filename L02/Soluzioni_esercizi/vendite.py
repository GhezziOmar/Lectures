import pandas as pd

def main():
    df = pd.DataFrame({
        "Mese":     ["Gen", "Feb", "Mar", "Apr", "Mag", "Giu"],
        "ProdottoA": [1200, 1500, 1100, 1800, 2000, 1700],
        "ProdottoB": [800,  900,  750,  1100, 1300, 1050],
        "ProdottoC": [500,  450,  600,  700,  800,  750]
    })

    prodotti = ["ProdottoA", "ProdottoB", "ProdottoC"]

    df["Totale mese"] = df[prodotti].sum(axis=1)
    Totale_prodotto = df[prodotti].sum()

    idx_max = df["Totale mese"].idxmax()
    mese_migliore = df.loc[idx_max, "Mese"]
    totale_mese_migliore = df.loc[idx_max, "Totale mese"]

    print("Vendite con totale mensile:")
    print(df.to_string() + "\n")

    print("Totale annuo per prodotto:")
    print(Totale_prodotto.to_string() + "\n")

    print(f"Mese con vendite più alte: {mese_migliore} ({totale_mese_migliore})")


if __name__ == "__main__":
    main()