# Lezione 01: Esercizi Python Base (Parte 2)

## 1. Inversione di una lista
Scrivere un programma che, data la seguente lista, la inverta, senza usare il metodo della classe list `reverse()` o lo slicing `[::-1]`.

**Lista da inserire hard coded nel codice:**
```python
lista = [10, 20, 30, 40, 50, 60, 70]
```

##### Esempio d'esecuzione:
```text
$ python inversione.py (in alternativa: uv run inversione.py)
Lista originale: [10, 20, 30, 40, 50, 60, 70]
Lista invertita: [70, 60, 50, 40, 30, 20, 10]
```

---
## 2. Prodotto scalare tra vettori (NumPy)
Scrivere un programma che, dati i seguenti due vettori `v` e `w`, calcoli e stampi il loro prodotto scalare (senza ricorrere alla funzione `np.dot(v, w)` di numpy o l'operatore `@`).

**Vettori da inserire hard coded nel codice:**
```python
v = np.array([1, 2, 3, 4])
w = np.array([5, 6, 7, 8])
```

**Suggerimento:**
il prodotto scalare (o dot product) tra due vettori di n componenti `v=[v_1, v_1, ..., v_n]` e `w=[w_1, w_2, ..., w_n]` è definito come la somma dei prodotti delle componenti corrispondenti:
```
v · w = v_1 * w_1 + v_2 * w_2 + ... + v_n * w_n
```

##### Esempio d'esecuzione:
```text
$ python prodotto_scalare.py (in alternativa: uv run prodotto_scalare.py)
Prodotto scalare: 70
```

---
## 3. Trasposizione di una matrice (NumPy)
Scrivere un programma che, data la seguente matrice NumPy di dimensioni 2x3:
* stampi la matrice originale con le sue dimensioni;
* calcoli e stampi la sua trasposta con le nuove dimensioni, costruendola manualmente con cicli for.
  
**Matrice da inserire hard coded nel codice:**
```python
matrice = np.array([
    [1, 2, 3],
    [4, 5, 6]
])
```

**Suggerimento:**
la trasposta di una matrice si ottiene scambiando righe e colonne: l'elemento in posizione `(i, j)` nella matrice originale va in posizione `(j, i)` nella trasposta. Di conseguenza, una matrice di dimensioni `m x n` diventa una matrice di dimensioni `n x m`.

##### Esempio d'esecuzione:
```text
$ python matrice_trasposta.py (in alternativa: uv run matrice_trasposta.py)
Matrice originale (2x3):
[[1 2 3]
 [4 5 6]]
Matrice trasposta (3x2):
[[1 4]
 [2 5]
 [3 6]]
```

## 4. Moltiplicazione tra matrici (NumPy)
Scrivere un programma che, date le seguenti due matrici NumPy, calcoli e stampi il loro prodotto matriciale **senza usare** `np.dot` o l'operatore `@`.

**Matrici da inserire hard coded nel codice:**
```python
A = np.array([[1, 2], [3, 4], [5, 6]])
B = np.array([[6, 7, 8], [9, 10, 11]])
```

**Suggerimento:**
il prodotto matriciale tra due matrici `A` (n x p) e `B` (p x m) produce una matrice `C` (n x m), dove ogni elemento `C[i, j]` è la somma dei prodotti degli elementi della riga `i` di `A` per gli elementi della colonna `j` di `B` (ossia, `C[i, j]` è il prodotto scalare del vettore riga i-esimo di `A` e il vettore colonna `j` di `B`):
```
C[i, j] = A[i,0]*B[0,j] + A[i,1]*B[1,j] + ... + A[i,n]*B[n,j]
```

##### Esempio d'esecuzione:
```text
$ python prodotto_matrici.py (in alternativa: uv run prodotto_matrici.py)
A x B =
[[ 24  27  30]
 [ 54  61  68]
 [ 84  95 106]]
```

## 5. Rimozione duplicati da una lista

Scrivere un programma che, data la seguente lista, rimuova i duplicati mantenendo l'ordine di prima apparizione, **senza usare** `set()` o altre funzioni built-in per la deduplicazione.

**Lista da inserire hard coded nel codice:**
```python
lista = [3, 7, 2, 7, 1, 3, 9, 2, 5, 1, 8, 3]
```

##### Esempio d'esecuzione:
```text
$ python rimozione_duplicati.py (in alternativa: uv run rimozione_duplicati.py)
Lista originale: [3, 7, 2, 7, 1, 3, 9, 2, 5, 1, 8, 3]
Lista senza duplicati: [3, 7, 2, 1, 9, 5, 8]
```
---

## 6. Anagrammi

Scrivere un programma che legga da tastiera due parole e verifichi se sono anagrammi l'una dell'altra, cioè se contengono esattamente le stesse lettere con le stesse frequenze. Il confronto deve essere case-insensitive. **Non è consentito** usare `sorted()` o `Counter`.

##### Esempio d'esecuzione:
```text
$ python anagrammi.py (in alternativa: uv run anagrammi.py)
Inserisci la prima parola: Roma
Inserisci la seconda parola: Mora
"Roma" e "Mora" sono anagrammi

$ python anagrammi.py (in alternativa: uv run anagrammi.py)
Inserisci la prima parola: aab
Inserisci la seconda parola: abc
"aab" e "abc" non sono anagrammi
```
---
## 7. Ordinamento di un dizionario

Scrivere un programma che, dato il seguente dizionario contenente i voti di alcuni studenti, restituisca una lista di tuple ordinate per voto decrescente **senza usare** `sorted()`, `sort()` o qualsiasi altra funzione di ordinamento built-in. A parità di voto, i nomi devono essere in ordine alfabetico crescente.

**Dizionario da inserire hard coded nel codice:**
```python
studenti = {
    "Mario": 9, "Bruno": 6, "Carla": 8,
    "Davide": 5, "Elena": 7, "Franco": 9, "Giulia": 6
}
```

**Suggerimento:**
il primo passo è convertire il dizionario in una lista di tuple su cui poter operare (un dizionario è una collezione **non ordinata** di elementi, una lista dispone invece di un ordinamento intrinseco). Si scorrono le coppie chiave-valore con `.items()`:
```python
lista = []
for nome, voto in studenti.items():
    lista.append((nome, voto))
```

##### Esempio d'esecuzione:
```text
$ python bubble_sort.py (in alternativa: uv run bubble_sort.py)
Dizionario originale: {'Mario': 9, 'Bruno': 6, 'Carla': 8, 'Davide': 5, 'Elena': 7, 'Franco': 9, 'Giulia': 6}
Lista ordinata:       [('Franco', 9), ('Mario', 9), ('Carla', 8), ('Elena', 7), ('Bruno', 6), ('Giulia', 6), ('Davide', 5)]
```
---

## 8. Istogramma testuale

Scrivere un programma che, data la seguente lista di voti, stampi un istogramma orizzontale a barre di asterischi che mostri quante volte compare ciascun voto, ordinato per voto crescente. **Non è consentito** usare funzioni built-in come `count()`, `sorted()` e `sort()` .

**Lista da inserire hard coded nel codice:**
```python
voti = [6, 8, 7, 9, 6, 7, 8, 6, 10, 7, 9, 8, 7, 6, 8]
```

##### Esempio d'esecuzione:
```text
$ python istogramma.py (in alternativa: uv run istogramma.py)
6: ****
7: ****
8: ****
9: **
10: *
```
---

## 9. Normalizzazione di un vettore (NumPy)

Scrivere un programma che, dato un vettore NumPy, definisca una funzione `norma(v)` che calcoli e restituisca la norma euclidea del vettore.
Utilizzare poi tale funzione per normalizzare il vettore, ossia ottenere il vettore unitario dividendo il vettore originale per la sua norma. La norma deve essere calcolata manualmente, **senza utilizzare** `np.linalg.norm()`. La funzione deve inoltre sollevare un `ValueError` nel caso in cui il vettore sia nullo.

**Vettore da inserire hard coded nel codice:**
```python
v = np.array([3.0, 4.0, 0.0, 0.0])
```

**Suggerimento:**
la norma euclidea di un vettore è la radice quadrata della somma dei quadrati delle sue componenti. Il vettore normalizzato si ottiene dividendo ogni componente per la norma: `v / norma`. Attenzione a gestire il caso `norma == 0`.

##### Esempio d'esecuzione:
```text
$ python normalizzazione.py (in alternativa: uv run normalizzazione.py)
Vettore originale: [3. 4. 0. 0.]
Norma: 5.0
Vettore normalizzato: [0.6 0.8 0. 0.]
```
---


## 10. Matrice da input utente 

Scrivere un programma che legga da tastiera una matrice inserita riga per riga dall'utente. Ogni riga è una sequenza di numeri interi separati da uno spazio. L'inserimento termina quando l'utente digita `.`. Il programma deve:
* raccogliere le righe inserite e costruire una lista di liste;
* tentare di convertire la lista di liste in un array NumPy;
* stampare la matrice se la conversione ha successo (tutte le righe hanno lo stesso numero di elementi), altrimenti stampare un messaggio di errore.

**Suggerimento:**
Python non ha un costrutto `do-while` nativo come altri linguaggi, ma si può simulare con un ciclo `while True` che esegue sempre almeno una iterazione e si interrompe con `break` quando viene soddisfatta la condizione di uscita:
```python
while True:
    riga = input("...")
    if riga == ".":
        break
    # elabora riga
```
Ogni riga inserita va divisa nei suoi elementi costituenti considerando come separatore lo spazio bianco (gestendo anche spazi multipli consecutivi). Ogni elemento va poi convertito in intero.

La conversione in array NumPy va gestita con un blocco `try/except`: se le righe hanno lunghezze diverse, NumPy non riesce a costruire una matrice rettangolare e solleva un `ValueError`:
```python
try:
    matrice = np.array(lista_righe, dtype=int)
    print(matrice)
except ValueError:
    print("Errore: le righe hanno lunghezze diverse, impossibile creare la matrice.")
```

##### Esempio d'esecuzione (caso corretto):
```text
$ python matrice_input.py (in alternativa: uv run matrice_input.py)
Inserisci una riga (oppure . per terminare): 1 2 3
Inserisci una riga (oppure . per terminare): 4 5 6
Inserisci una riga (oppure . per terminare): 7 8 9
Inserisci una riga (oppure . per terminare): .
Matrice inserita:
[[1 2 3]
 [4 5 6]
 [7 8 9]]
```

##### Esempio d'esecuzione (caso errato):
```text
$ python matrice_input.py (in alternativa: uv run matrice_input.py)
Inserisci una riga (oppure . per terminare): 1 2 3
Inserisci una riga (oppure . per terminare): 4 5
Inserisci una riga (oppure . per terminare): 7 8 9
Inserisci una riga (oppure . per terminare): .
Errore: le righe hanno lunghezze diverse, impossibile creare la matrice.
```


