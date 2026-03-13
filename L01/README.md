# Lezione 01: Esercizi Python Base (Parte 2)
## 1. Massimo e minimo di una lista
Scrivere un programma che, data la seguente lista di numeri, trovi e stampi il valore massimo, il valore minimo e la loro differenza, senza usare le funzioni built-in `max()` e `min()`.

**Lista da inserire hard coded nel codice:**
```python
lista = [14, 3, 27, 8, 42, 5, 19, 33, 1, 11]
```

##### Esempio d'esecuzione:
```text
$ python max_min.py (in alternativa: uv run max_min.py)
Lista: [14, 3, 27, 8, 42, 5, 19, 33, 1, 11]
Valore massimo: 42
Valore minimo: 1
Differenza: 41
```

---
## 2. Inversione di una lista
Scrivere un programma che, data la seguente lista, la inverta, senza usare la funzione built-in `reverse()` o lo slicing `[::-1]`.
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
## 3. Prodotto scalare tra vettori (NumPy)
Scrivere un programma che, dati i seguenti due vettori `v` e `w`, calcoli e stampi il loro prodotto scalare (senza ricorrere alla funzione `np.dot(v, w)` di numpy).

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
v = [1 2 3 4]
w = [5 6 7 8]
Prodotto scalare: 70
```

---
## 4. Trasposizione di una matrice (NumPy)
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

## 5. Moltiplicazione tra matrici (NumPy)
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
A =
[[1 2]
 [3 4]
 [5 6]]
B =
[[ 6  7  8]
 [ 9 10 11]]
A x B =
[[ 24  27  30]
 [ 54  61  68]
 [ 84  95 106]]
```

## 6. Rimozione duplicati da una lista

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

## 7. Anagrammi

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
## 8. Ordinamento di un dizionario

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

## 10. Istogramma testuale

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
