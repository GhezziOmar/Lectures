# Lezione 00: Esercizi Python Base (parte 1)

## 1. Area e perimetro rettangolo

Scrivere un programma che legga da tastiera le misure dell’altezza e della base di un rettangolo e ne calcoli il perimetro e l’area.

##### Esempio d'esecuzione:

```text
$ python rettangolo.py (in alternativa: uv run rettangolo.py)
Inserisci la base: 20.5
Inserisci l'altezza: 10
L'area del rettangolo è: 205.0, il perimetro è: 61.0
```
---

## 2. Area cerchio

Scrivere un programma che legga da tastiera il raggio di un cerchio e ne calcoli circonferenza e area.

*Suggerimento:* l'area del cerchio si calcola facendo `raggio x raggio x pi_greco`, mentre la circonferenza facendo `2 x raggio x pi_greco`. Il valore numerico di `pi_greco` è memorizzato nella costante `pi` del package `numpy`, a cui ci si può riferire con `np.pi`, avendo importato il package numpy come segue: `import numpy as np`.

##### Esempio d'esecuzione:

```text
$ python cerchio.py (in alternativa: uv run cerchio.py)
Raggio = 2.5
L'area del cerchio è: 19.635, la circonferenza è: 15.708
```
---
## 3. Età

Scrivere un programma che legga da tastiera le età di due persone (espresse in anni) e calcoli:

* la somma delle età inserite;
* la media delle età inserite;
* la media delle età inserite arrotondata per difetto all'intero inferiore;
* la media delle età inserite arrotondata per eccesso all'intero superiore;
* la somma e la media delle età che le due persone avranno fra 10 anni.

**Suggerimento:**
la media arrotondata per difetto può essere calcolata usando la funzione `np.floor` del package `numpy` nel seguente modo:
```python
media_arrotondata_difetto = np.floor(media)
```
Similarmente, la media arrotondata per eccesso può essere calcolata usando la funzione `np.ceil` nel seguente modo:
```python
media_arrotondata_eccesso = np.ceil(media)
```

##### Esempio d'esecuzione:

```text
$ python calcoloeta.py (in alternativa: uv run calcoloeta.py) 
Età persona 1 = 15
Età persona 2 = 20
Somma età = 35
Media età = 17.5
Media età arrotondata per difetto all'intero inferiore = 17
Media età arrotondata per eccesso all'intero superiore = 18
Somma età fra 10 anni = 55
Media età fra 10 anni = 27.5
```

---
## 4. Pari o dispari

Scrivere un programma che legge da tastiera un intero `n` e stampa a video se il numero è pari o dispari.

##### Esempio d'esecuzione:
```text
$ python pari_dispari.py (in alternativa: uv run pari_dispari.py)
Inserisci un numero: 10
10 è pari

$ python paridispari.py (in alternativa: uv run pari_dispari.py)
Inserisci un numero: 11
11 è dispari
```
---
## 5. Tabellina

Scrivere un programma che, dopo aver richiesto all'utente di inserire da tastiera un numero intero `n`, stampi a video la corrispondente tabellina (moltiplicando `n` per i numeri naturali da 1 a 10) come mostrato nell'**Esempio d'esecuzione**.

##### Esempio d'esecuzione:
```text
$ python tabelline.py (in alternativa: uv run tabelline.py)
Inserisci un numero: 9
1 x 9 = 9
2 x 9 = 18
3 x 9 = 27
4 x 9 = 36
5 x 9 = 45
6 x 9 = 54
7 x 9 = 63
8 x 9 = 72
9 x 9 = 81
10 x 9 = 90
```
---

## 6. Creazione matrice da lista 

Scrivere un programma che, data la seguente lista di 16 numeri:
* crei una matrice (lista di liste) 4x4 disponendo i numeri sulla prima riga, poi sulla seconda, e così via;
* stampi la matrice riga per riga.

**Lista da inserire hard coded nel codice:**
```python
lista = [3, 7, 2, 9, 1, 5, 8, 4, 6, 0, 11, 13, 15, 12, 10, 14]
```

**Suggerimento:**
una matrice è una struttura dati bidimensionale organizzata in righe e colonne. In Python può essere rappresentata come una **lista di liste**, dove ogni lista interna rappresenta una riga. Per costruire la matrice si usano due cicli `for` annidati: il ciclo esterno scorre le righe, quello interno scorre le colonne.

##### Esempio d'esecuzione:
```text
$ python crea_matrice.py (in alternativa: uv run crea_matrice.py)
[[3, 7, 2, 9], [1, 5, 8, 4], [6, 0, 11, 13], [15, 12, 10, 14]]
```
---

## 7. Creazione matrice da lista (numpy)
Scrivere un programma che, data la seguente lista di 16 numeri:
* crei una matrice numpy 4x4 disponendo i numeri sulla prima riga, poi sulla seconda, e così via;
* stampi la matrice.

**Lista da inserire hard coded nel codice:**
```python
lista = [3, 7, 2, 9, 1, 5, 8, 4, 6, 0, 11, 13, 15, 12, 10, 14]
```
**Suggerimento:**
In NumPy, una matrice viene prima preallocata con tutti zeri usando `np.zeros`, specificando la forma come tupla `(righe, colonne)`:
```python
matrice = np.zeros((4, 4), dtype=int)
```
##### Esempio d'esecuzione:
```text
$ python crea_matrice.py (in alternativa: uv run crea_matrice.py)
[[ 3  7  2  9]
 [ 1  5  8  4]
 [ 6  0 11 13]
 [15 12 10 14]]
```
---

## 8. Elaborazione Matrice
Scrivere un programma che, data la seguente matrice 4x4 definita come lista di liste:
* estragga e stampi la prima riga;
* estragga e stampi la prima colonna;
* estragga e stampi gli elementi sulla diagonale principale.

**Matrice da inserire hard coded nel codice:**
```python
matrice = [
        [3,  10,  2,  4],
        [4,  8,  1,  8],
        [9,  6, 22, 12],
        [12, 21, 1, 7]
    ]
```

##### Esempio d'esecuzione:
```text
$ python matrice.py (in alternativa: uv run matrice.py)
Prima riga: [3,  10,  2,  4]
Prima colonna: [3, 4, 9, 12]
Diagonale principale: [3, 8, 22, 7]
```
---

## 9. Elaborazione Matrice (NumPy)
Scrivere un programma che, data la seguente matrice 4x4 definita come array NumPy:
* estragga e stampi la prima riga;
* estragga e stampi la prima colonna;
* estragga e stampi gli elementi sulla diagonale principale.

**Matrice da inserire hard coded nel codice:**
```python
matrice = np.array([
        [3,  10,  2,  4],
        [4,  8,  1,  8],
        [9,  6, 22, 12],
        [12, 21, 1, 7]
    ])
```

##### Esempio d'esecuzione:
```text
$ python matrice_numpy.py (in alternativa: uv run matrice_numpy.py)
Prima riga: [ 3 10  2  4]
Prima colonna: [ 3  4  9 12]
Diagonale Principale: [ 3  8 22  7]
```

---
## 10. Determinante di una matrice 2x2
Scrivere un programma che, data la seguente matrice 2x2 definita come array NumPy:
* calcoli e stampi il determinante della matrice.

**Matrice da inserire hard coded nel codice:**
```python
matrice = np.array([[3, 7], [2, 5]])
```
**Suggerimento:**
Se `A= [[a, b], [c, d]]` è una matrice 2x2, il suo determinante è definito come:
```text
det(A) = (a × d) - (b × c)
```

##### Esempio d'esecuzione:
```text
$ python determinante.py (in alternativa: uv run determinante.py)
Il determinante della matrice è: 1.0
```
---
