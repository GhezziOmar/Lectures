# Lezione XX: Altri esercizi di Coding

## 1. Conteggio elementi in intervallo

Scrivere un programma Python che, data la seguente lista di numeri interi, conti quanti elementi sono compresi in un intervallo `[a, b]` letto da tastiera.

**Lista da inserire hard coded nel codice:**
```python
lista = [4, 12, 7, 3, 19, 8, 25, 1, 14, 6, 11, 17, 2, 9, 22]
```

##### Esempio d'esecuzione:
```text
$ python conteggio.py (in alternativa: uv run conteggio.py)
Inserisci il valore minimo dell'intervallo: 5
Inserisci il valore massimo dell'intervallo: 15
Elementi compresi tra 5 e 15: 6
```
---

## 2. Crivello di Eratostene

Scrivere un programma Python che utilizzi il metodo del Crivello di Eratostene per stampare l'elenco dei numeri primi fino a un numero `n` specificato da tastiera.

Il Crivello di Eratostene funziona così: si scrivono tutti i numeri naturali da 2 fino a `n`. In seguito, si cancellano tutti i multipli del primo numero (escluso lui stesso). Poi si prende il primo numero non cancellato e si ripete l'operazione, proseguendo fino alla fine. I numeri rimasti sono i numeri primi.

##### Esempio d'esecuzione:
```text
$ python crivello.py (in alternativa: uv run crivello.py)
Inserisci n: 30
Numeri primi fino a 30: [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
```
---

## 3. Rimozione duplicati consecutivi

Scrivere un programma Python che, data la seguente lista, rimuova gli elementi duplicati consecutivi mantenendo l'ordine degli elementi.

**Lista da inserire hard coded nel codice:**
```python
lista = [1, 1, 2, 3, 3, 3, 4, 4, 5, 1, 1, 6, 6]
```

##### Esempio d'esecuzione:
```text
$ python duplicati.py (in alternativa: uv run duplicati.py)
Lista originale: [1, 1, 2, 3, 3, 3, 4, 4, 5, 1, 1, 6, 6]
Lista senza duplicati consecutivi: [1, 2, 3, 4, 5, 1, 6]
```
---

## 4. Conversione temperature

Scrivere un programma Python che converta una temperatura letta da tastiera da gradi Celsius a Fahrenheit e viceversa, chiedendo all'utente la direzione della conversione.

La formula di conversione è la seguente, dove `C` è la temperatura in gradi Celsius e `F` in gradi Fahrenheit:

```
F = (C × 9/5) + 32
C = (F - 32) × 5/9
```

##### Esempio d'esecuzione:
```text
$ python temperature.py (in alternativa: uv run temperature.py)
Converti da (C)elsius a Fahrenheit o da (F)ahrenheit a Celsius? C
Inserisci la temperatura in Celsius: 60
60°C corrisponde a 140.0°F

$ python temperature.py (in alternativa: uv run temperature.py)
Converti da (C)elsius a Fahrenheit o da (F)ahrenheit a Celsius? F
Inserisci la temperatura in Fahrenheit: 45
45°F corrisponde a 7.22°C
```
---

## 5. Serie di Fibonacci

Scrivere un programma Python che, letto da tastiera un numero intero `n`, stampi la serie di Fibonacci fino all'n-esimo termine.

La sequenza di Fibonacci è: 0, 1, 1, 2, 3, 5, 8, 13, 21, ... Ogni numero si ottiene sommando i due che lo precedono.

##### Esempio d'esecuzione:
```text
$ python fibonacci.py (in alternativa: uv run fibonacci.py)
Inserisci n: 10
Serie di Fibonacci fino al termine 10: [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
```
---

## 6. Numero perfetto

Scrivere un programma Python che, letto da tastiera un numero intero positivo `n`, verifichi se il numero è perfetto.

Un numero perfetto è un intero positivo uguale alla somma dei suoi divisori positivi propri (cioè escluso il numero stesso). Ad esempio: 6 = 1 + 2 + 3, oppure 28 = 1 + 2 + 4 + 7 + 14.

##### Esempio d'esecuzione:
```text
$ python perfetto.py (in alternativa: uv run perfetto.py)
Inserisci un numero: 6
6 è un numero perfetto

$ python perfetto.py (in alternativa: uv run perfetto.py)
Inserisci un numero: 10
10 non è un numero perfetto
```
---

## 7. Caratteri ripetuti in una stringa

Scrivere un programma che, data la seguente stringa hard coded, conti quante volte ogni carattere appare e stampi solo i caratteri che compaiono più di una volta, in ordine decrescente di frequenza.

**Stringa da inserire hard coded nel codice:**
```python
stringa = "thequickbrownfoxjumpsoverthelazydog"
```

##### Esempio d'esecuzione:
```text
$ python caratteri_ripetuti.py (in alternativa: uv run caratteri_ripetuti.py)
o 4
e 3
u 2
h 2
r 2
t 2
```
---

## 8. Rimozione elementi comuni tra due liste

Scrivere un programma che, date le seguenti due liste hard coded, rimuova da `lista1` tutti gli elementi che sono presenti anche in `lista2` e stampi la lista risultante.

**Liste da inserire hard coded nel codice:**
```python
lista1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
lista2 = [2, 4, 6, 8]
```

##### Esempio d'esecuzione:
```text
$ python rimozione_comuni.py (in alternativa: uv run rimozione_comuni.py)
lista1: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
lista2: [2, 4, 6, 8]
Risultato: [1, 3, 5, 7, 9, 10]
```
---

## 9. Prodotto degli elementi di una tupla

Scrivere un programma che, date le seguenti due tuple hard coded, calcoli e stampi il prodotto di tutti i loro elementi.

**Tuple da inserire hard coded nel codice:**
```python
tupla1 = (4, 3, 2, 2, -1, 18)
tupla2 = (2, 4, 8, 8, 3, 2, 9)
```

##### Esempio d'esecuzione:
```text
$ python prodotto_tupla.py (in alternativa: uv run prodotto_tupla.py)
Tupla 1: (4, 3, 2, 2, -1, 18) → Prodotto: -864
Tupla 2: (2, 4, 8, 8, 3, 2, 9) → Prodotto: 27648
```
---

## 10. Frequenza dei valori in un dizionario

Scrivere un programma che, dato il seguente dizionario hard coded, calcoli quante volte ogni **valore** compare nel dizionario e stampi i risultati in ordine decrescente di frequenza.

**Dizionario da inserire hard coded nel codice:**
```python
dizionario = {
    'V': 10, 'VI': 10, 'VII': 40, 'VIII': 20,
    'IX': 70, 'X': 80, 'XI': 40, 'XII': 20, 'XIII': 10
}
```

##### Esempio d'esecuzione:
```text
$ python frequenza_valori.py (in alternativa: uv run frequenza_valori.py)
10: 3
40: 2
20: 2
70: 1
80: 1
```
---

## 11. Stringa più lunga in una lista

Definire la funzione `max_length(L)` che prende come argomento una lista `L` di stringhe e restituisce la stringa con la lunghezza massima. Si assuma che `L` sia non vuota e che tutte le stringhe siano diverse tra loro. La funzione non deve chiamare altre funzioni eccetto `len()`.

##### Esempio d'esecuzione:
```text
$ python max_length.py (in alternativa: uv run max_length.py)
max_length(["cane", "gatto", "rinoceronte", "topo"]) → rinoceronte
max_length(["mela", "banana", "kiwi"]) → banana
```
---

## 12. Somma dei divisori dispari

Definire la funzione `somma_div_dispari(N)` che restituisce la somma di tutti i divisori positivi dispari di `N`. Si assuma che `N` sia un intero maggiore di 1. Sia 1 che `N` stesso sono considerati divisori di `N`.

##### Esempio d'esecuzione:
```text
$ python somma_div_dispari.py (in alternativa: uv run somma_div_dispari.py)
somma_div_dispari(21) → 32   # divisori dispari: 1, 3, 7, 21
somma_div_dispari(18) → 13   # divisori dispari: 1, 3, 9
```
---
