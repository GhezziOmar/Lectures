# Guida operativa: dal computer vuoto al primo programma Python

### 1: Cos'è la shell
La shell è un'interfaccia testuale che permette di comunicare direttamente con il sistema operativo tramite comandi. È lo strumento fondamentale per qualsiasi sviluppatore.
* **Linux/macOS**: shell di default è `bash` o `zsh`, si apre con il terminale
* **Windows**: si può usare `PowerShell` oppure `Command Prompt (cmd)`

### 2: Navigare nel filesystem
I comandi fondamentali per muoversi tra le cartelle e creare/rimuovere file o directory:

| Operazione | Linux/macOS | Windows |
|---|---|---|
| Vedere dove sei | `pwd` | `cd` |
| Listare i file | `ls` | `dir` |
| Entrare in una cartella | `cd nomecartella` | `cd nomecartella` |
| Tornare indietro | `cd ..` | `cd ..` |
| Andare al desktop | `cd ~/Desktop` | `cd %USERPROFILE%\Desktop` |
| Creare una cartella | `mkdir nomecartella` | `mkdir nomecartella` |
| Creare un file vuoto | `touch nomefile.py` | `type nul > nomefile.py` |
| Cancellare un file | `rm nomefile.py` | `del nomefile.py` |
| Cancellare una cartella | `rm -r nomecartella` | `rmdir /s nomecartella` |

Comandi utili aggiuntivi
* `clear` (Linux/macOS) / `cls` (Windows) — pulisce il terminale
* `history` — mostra i comandi eseguiti in precedenza
* freccia `↑` — richiama l'ultimo comando digitato
* `Tab` — autocompleta il nome di file e cartelle

### 3: Installazione degli strumenti

1. **VS Code** — editor di codice standard
   * Scaricare da: https://code.visualstudio.com
   * Installare l'estensione **Python** (Microsoft) dall'interno di VS Code

2. **Python**
   * Scaricare da: https://www.python.org/downloads
   * Su Windows: spuntare **"Add Python to PATH"** durante l'installazione
   * Verificare l'installazione: `python --version`

3. **Git**
   * Scaricare da: https://git-scm.com/downloads
   * Verificare l'installazione: `git --version`
   * Configurazione minima obbligatoria:
```bash
git config --global user.name "Nome Cognome"
git config --global user.email "email@esempio.com"
```

4. **uv** — gestore di ambienti virtuali e dipendenze Python
   * Linux/macOS:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
   * Windows (PowerShell):
```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```
   * Verificare l'installazione: `uv --version`


### 4: Primo programma Python in VS Code (1) — Setup

Aprire il terminale su Linux/macOS o il prompt dei comandi su Windows, succesivamente:
```bash
# 1. Spostarsi sul Desktop
cd ~/Desktop                        # Linux/macOS
cd %USERPROFILE%\Desktop            # Windows

# 2. Clonare la repository da GitHub
git clone https://github.com/GhezziOmar/Lectures.git

# 3. Entrare nella cartella clonata
cd Lectures

# 4. Aprire VS Code nella cartella corrente
code .
```

Una volta aperto VS Code, aprire il terminale integrato (menu a tendina: Terminale -> Nuovo Terminale) e:
```bash
# Spostarsi nella sottocartella della lezione corrente (es. L00)
cd L00

# Spostarsi nella (o creare la) sottocartella 'Vostri_esercizi'
cd Vostri_esercizi

# Creare e aprire direttamente il file el primo programma python
code rettangolo.py
```

### 5: Primo programma Python in VS Code (2) — Lo scheletro base

Ogni programma Python che scriveremo seguirà questa struttura base:
```python
# import numpy as np

def main():
    pass

if __name__ == "__main__":
    main()
```

Cosa fa ogni parte:

**`# import numpy as np`**
Riga commentata che ricorda dove importare i package esterni quando servono.
Decommentarla significa rendere disponibile numpy nel programma con l'alias `np`.

**`def main():`**
Definisce la funzione principale del programma, che conterrà tutta la logica.
Raccogliere il codice in una funzione `main` è una buona pratica che rende il codice
più leggibile e organizzato.

**`pass`**
Segnaposto temporaneo: dice a Python "questa funzione per ora non fa nulla".
Va sostituito con il codice effettivo dell'esercizio.

**`if __name__ == "__main__":`**
Blocco che viene eseguito solo quando il file viene lanciato direttamente
(es. `python rettangolo.py` oppure `uv run rettangolo.py`).
Se il file venisse invece importato come modulo da un altro file, questo blocco
verrebbe ignorato.

**`main()`**
Chiama la funzione `main` e avvia l'esecuzione del programma.


### 6: Eseguire un programma python
Assumendo di aver finito di scrivere il codice di `rettangolo.py` nel corpo della funzione main, eseguire (posizionandosi nella cartella che contiene il file) una delle seguenti istruzioni:
Eseguire il file con python base
```bash
python rettangolo.py
```

Eseguire il file con uv
```bash
uv run rettangolo.py
```

### 7: Aggiornare la repository mantenendo le modifiche locali

Se il repository viene aggiornato, è necessario scaricare gli aggiornamenti senza perdere i file creati localmente. La procedura è la seguente:
```bash

# 0. Entrare nella cartella di lavoro da aggiornare (supponendo di trovarci nel Desktop)
cd Lectures

# 1. Mettere da parte le modifiche locali temporaneamente
git stash

# 2. Scaricare gli aggiornamenti dalla repository remota
git pull

# 3. Riapplicare le modifiche locali
git stash pop
```

`git stash` salva temporaneamente tutte le modifiche locali in uno spazio separato, `git pull` scarica i nuovi materiali dal repository remoto, e `git stash pop` riapplica le modifiche salvate sopra ai nuovi file scaricati.

