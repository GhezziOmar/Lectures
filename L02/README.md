# Esercizi Python — Stringhe, Dizionari (e Pandas)

---

## 1. Stringa palindroma

Scrivere un programma che legga da tastiera una stringa e verifichi se è palindroma, cioè se si legge allo stesso modo da sinistra a destra e da destra a sinistra. Il confronto deve essere case-insensitive (ignorare maiuscole e minuscole) e ignorare gli spazi.

**Suggerimento:**
prima si normalizza la stringa rimuovendo gli spazi e convertendo tutto in minuscolo:
```python
s = stringa.replace(" ", "").lower()
```
Poi si confronta la stringa con la sua versione invertita. Se `s == s_invertita` la stringa è palindroma.

##### Esempio d'esecuzione:
```text
$ python palindroma.py (in alternativa: uv run palindroma.py)
Inserisci una stringa: Anna
"Anna" è palindroma

$ python palindroma.py (in alternativa: uv run palindroma.py)
Inserisci una stringa: I topi non avevano nipoti
"I topi non avevano nipoti" è palindroma

$ python palindroma.py (in alternativa: uv run palindroma.py)
Inserisci una stringa: Python
"Python" non è palindroma
```
---

## 2. Conteggio caratteri in una stringa

Scrivere un programma che legga da tastiera una stringa e conti, senza usare funzioni built-in come `count()`:
* il numero di vocali (a, e, i, o, u);
* il numero di consonanti;
* il numero di spazi;
* il numero di caratteri speciali (tutto ciò che non è una lettera né uno spazio).

**Suggerimento:**
si può definire, come variabile globale, una stringa contenente tutte le vocali e usarla per il confronto:
```python
VOCALI = "aeiou"
```

##### Esempio d'esecuzione:
```text
$ python conteggio_caratteri.py (in alternativa: uv run conteggio_caratteri.py)
Inserisci una stringa: Ciao, mondo!
Vocali: 5
Consonanti: 4
Spazi: 1
Caratteri speciali: 2
```
---

## 3. Frequenza delle parole

Scrivere un programma che, data la seguente stringa hard coded, conti la frequenza di ogni parola e stampi le parole ordinate dalla più frequente alla meno frequente.

**Stringa da inserire hard coded nel codice:**
```python
testo = "il gatto è sul tetto il tetto è alto il gatto guarda il cielo il cielo è blu"
```

**Suggerimento:**
si usa un dizionario dove le chiavi sono le parole e i valori sono i conteggi. Si scorre la lista di parole ottenuta con `.split()` e si aggiorna la frequenza, relativa alla parola trovata, nel dizionario.

##### Esempio d'esecuzione:
```text
$ python frequenza_parole.py (in alternativa: uv run frequenza_parole.py)
[('il', 5), ('è', 3), ('gatto', 2), ('tetto', 2), ('cielo', 2), ('sul', 1), ('alto', 1), ('guarda', 1), ('blu', 1)]
```
---

## 4. Statistiche sui voti degli studenti

Scrivere un programma che, dato il seguente DataFrame pandas contenente i voti di alcuni studenti, calcoli e stampi:
* la media dei voti per ogni studente;
* la media dei voti per ogni materia;
* il voto massimo e minimo dell'intero DataFrame.

**Dataset da inserire hard coded nel codice:**
```python
df = pd.DataFrame({
    "Studente": ["Alice", "Bruno", "Carla", "Davide", "Elena"],
    "Matematica": [8, 6, 9, 5, 7],
    "Fisica":     [7, 5, 8, 6, 9],
    "Informatica":[9, 7, 6, 8, 8]
})
```

**Suggerimento:**
per calcolare la media per ogni riga (studente) si usa `.mean()` con `axis=1`, che opera orizzontalmente. Per la media per ogni colonna (materia) si usa `.mean()` con `axis=0` (il default). Il valore massimo e minimo dell'intero DataFrame si ottiene con `.max().max()` e `.min().min()` (il primo `.max()` restituisce il massimo per colonna, il secondo prende il massimo tra quei valori).

##### Esempio d'esecuzione:
```text
$ python voti.py (in alternativa: uv run voti.py)
DataFrame con media per studente:
  Studente  Matematica  Fisica  Informatica  Media studente
0    Alice           8       7            9            8.00
1    Bruno           6       5            7            6.00
2    Carla           9       8            6            7.67
3   Davide           5       6            8            6.33
4    Elena           7       9            8            8.00

Media per materia:
Matematica     7.0
Fisica         7.0
Informatica    7.6

Voto massimo: 9
Voto minimo: 5
```
---

## 5. Analisi delle vendite mensili

Scrivere un programma che, dato il seguente DataFrame contenente le vendite mensili di tre prodotti, calcoli e stampi:
* il totale delle vendite per ogni mese;
* il totale delle vendite per ogni prodotto nell'intero anno;
* il mese con le vendite totali più alte.

**Dataset da inserire hard coded nel codice:**
```python
df = pd.DataFrame({
    "Mese":     ["Gen", "Feb", "Mar", "Apr", "Mag", "Giu"],
    "ProdottoA": [1200, 1500, 1100, 1800, 2000, 1700],
    "ProdottoB": [800,  900,  750,  1100, 1300, 1050],
    "ProdottoC": [500,  450,  600,  700,  800,  750]
})
```

**Suggerimento:**
Per calcolare il totale per riga (totale mensile) si usa `.sum(axis=1)`. Per trovare la riga con il valore massimo si usa `.idxmax()`, che restituisce l'indice della riga con il valore massimo:
```python
idx_max = df["Totale mese"].idxmax()
mese_migliore = df.loc[idx_max, "Mese"]
```

##### Esempio d'esecuzione:
```text
$ python vendite.py (in alternativa: uv run vendite.py)
Vendite con totale mensile:
  Mese  ProdottoA  ProdottoB  ProdottoC  Totale mese
0  Gen       1200        800        500         2500
1  Feb       1500        900        450         2850
2  Mar       1100        750        600         2450
3  Apr       1800       1100        700         3600
4  Mag       2000       1300        800         4100
5  Giu       1700       1050        750         3500

Totale annuo per prodotto:
ProdottoA    9300
ProdottoB    5900
ProdottoC    3800

Mese con vendite più alte: Mag (4100)
```
---
## 6. Stipendi dei dipendenti

Scrivere un programma che, dato il seguente DataFrame contenente gli stipendi dei dipendenti di un'azienda, calcoli e stampi:
* lo stipendio medio, massimo e minimo per ogni reparto;
* il reparto con con somma stipendi più alta.

**Dataset da inserire hard coded nel codice:**
```python
df = pd.DataFrame({
    "Nome":     ["Alice", "Bruno", "Carla", "Davide", "Elena", "Franco", "Giulia"],
    "Reparto":  ["IT", "HR", "IT", "Vendite", "HR", "Vendite", "IT"],
    "Stipendio": [3200, 2800, 3500, 2600, 2900, 3100, 3300]
})
```

**Suggerimento:**
per calcolare statistiche raggruppate per categoria si usa: `.groupby()`, per raggruppare le righe per i valori di una colonna, seguito dalla selezione di una o più colonne specifiche (`"Stipendio"`) e dall'applicazione delle statistiche (`["mean", "max", "min", "sum"]`) tramite `.agg()`. Per ridefinire l'idicizzazione si utilizza `.reset_index()`:
```python
stats = df.groupby("Reparto")["Stipendio"].agg(["mean", "max", "min", "sum"]).reset_index()
```

##### Esempio d'esecuzione:
```text
$ python stipendi.py (in alternativa: uv run stipendi.py)
Stipendi dipendenti per reparto: 
     Nome  Reparto  Stipendio
0   Alice       IT       3200
1   Bruno       HR       2800
2   Carla       IT       3500
3  Davide  Vendite       2600
4   Elena       HR       2900
5  Franco  Vendite       3100
6  Giulia       IT       3300

Statistiche per reparto: 
   Reparto         mean   max   min    sum
0       HR  2850.000000  2900  2800   5700
1       IT  3333.333333  3500  3200  10000
2  Vendite  2850.000000  3100  2600   5700

Reparto con somma stipendi più alta: IT (10000)
```
---