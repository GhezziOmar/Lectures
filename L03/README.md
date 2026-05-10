## Esercizi

---

### 1. Esercizio_CaliforniaHousing.ipynb

**Dataset**: California Housing (`sklearn.datasets.fetch_california_housing`)  
**Task**: Regressione (target continuo `MedHouseVal`)

#### Obiettivo 

Estendere la pipeline di ML dalla **classificazione binaria** (Lezione 03) alla **regressione**. Si impara a:
- usare metriche di regressione (R² e RMSE) invece di accuracy
- interpretare la curva di complessità con RMSE (ottimale al **minimo**, non al massimo)
- scegliere `scoring='neg_root_mean_squared_error'` e `score_multiplier=-1` per i risultati positivi

#### Consegna passo-passo

1. **Carica il dataset** e verifica shape, tipi, NaN (nessun NaN atteso).
2. **EDA univariata**: esegui `plot_histograms` su tutte le feature + target. Osserva la distribuzione asimmetrica di `MedInc` e il clipping di `MedHouseVal` a 5.0.
3. **EDA bivariata**: calcola la correlazione di Pearson con il target e visualizza le top-4 feature con scatter plots. Identifica `MedInc` come predittore principale.
4. **EDA multivariata**: traccia la heatmap di correlazione. Identifica la collinearità tra `AveRooms` e `AveBedrms`.
5. **Modello base (Ridge)**: costruisci la pipeline `StandardScaler + Ridge`, esegui `nestedKFolfCV` con `scoring='neg_root_mean_squared_error'`. Calcola R² e RMSE dai `best_models`.
6. **Bias-variance (MLP Regressore)**: usa `nested_cv_bias_variance` con `scoring='neg_root_mean_squared_error'`, `score_multiplier=-1`, `hls_param='reg__hidden_layer_sizes'`. Visualizza con `plot_complexity_curve(..., higher_is_better=False)`.
7. **Confronto**: confronta RMSE della Ridge baseline con l'MLP ottimale.

#### Differenze rispetto a Lezione 03

| Aspetto | Lezione 03 (Diabetes) | Questo esercizio |
|---|---|---|
| Task | Classificazione binaria | Regressione |
| Metrica | Accuracy | R² e RMSE |
| Splitter | KFold | KFold (stesso) |
| MLP step name | `clf` | `reg` |
| Ottimale curva | idxmax (accuracy) | idxmin (RMSE) |
| `score_multiplier` | 1 | -1 (neg→pos) |

#### Suggerimenti pratici

- **`scoring='neg_root_mean_squared_error'`**: sklearn usa convenzione "negativa" per uniformare l'API. Il miglior modello ha il valore **meno negativo** (più vicino a 0).
- **`pipe.score()` su Ridge restituisce R²**, non RMSE. Per calcolare RMSE ricalcola manualmente con `mean_squared_error`.
- **`higher_is_better=False`** in `plot_complexity_curve` fa sì che il punto ottimale sia segnato al **minimo** della curva di validazione RMSE.
---

### 2. Esercizio_Wine.ipynb

**Dataset**: Wine (`sklearn.datasets.load_wine`)  
**Task**: Classificazione multiclasse (3 classi, 13 feature chimiche)

#### Obiettivo didattico

Estendere la pipeline dalla classificazione **binaria** alla classificazione **multiclasse** (3 classi). Si impara a:
- usare `multi_class='multinomial'` e softmax nella Logistic Regression
- gestire palette a 3 colori in `plot_pairplot_with_correlation` e `plot_boxplots`
- calcolare il numero di parametri MLP con `n_classes=3`

#### Consegna passo-passo

1. **Carica il dataset** e verifica la distribuzione delle 3 classi.
2. **EDA univariata**: istogrammi di tutte le feature. Nota la multimodalità di `proline` e `flavanoids` (segnale che le classi hanno distribuzioni diverse).
3. **EDA bivariata**: `plot_boxplots` con `palette=('gold','steelblue','salmon')`. Identifica `flavanoids` e `proline` come feature più discriminanti.
4. **EDA multivariata**: `plot_pairplot_with_correlation` con le 5 feature più discriminanti. Verifica la separabilità lineare delle 3 classi.
5. **Modello base (Logistic Regression multinomiale)**: `multi_class='multinomial'`, `solver='lbfgs'`, griglia su `C` e `penalty`. Esegui `nestedKFolfCV`.
6. **Bias-variance (MLP, n_classes=3)**: usa `nested_cv_bias_variance` con `n_classes=3` e `hls_param='clf__hidden_layer_sizes'`.
7. **Confronto**: confronta accuracy LR multinomiale vs MLP ottimale.

#### Differenze rispetto a Lezione 03

| Aspetto | Lezione 03 (Diabetes) | Questo esercizio |
|---|---|---|
| Numero classi | 2 | 3 |
| LR multi_class | default (OvR) | `'multinomial'` |
| LR solver | default | `'lbfgs'` |
| Palette plots | 2 colori | 3 colori |
| MLP n_classes | 1 | 3 |
| Dataset size | 768 campioni | 178 campioni |

#### Suggerimenti pratici

- **`palette=('gold','steelblue','salmon')`**: va specificato **sempre** per tutte le funzioni di visualizzazione che accettano `palette`. Il default è 2 colori.
- **`multi_class='multinomial'`**: necessario per la softmax multi-classe. Il default `'auto'` con 3 classi usa OvR (One-vs-Rest), meno elegante.
- **`n_classes=3`** in `nested_cv_bias_variance`: influisce sul conteggio dei parametri dell'output layer MLP (`n_units*3 + 3` invece di `n_units*1 + 1`).
- **Trabocchetto comune**: passare `palette` con solo 2 colori con 3 classi causa un `IndexError`. Il fix è già in `utils.py` (`default_colors` con fallback).
- **Con 178 campioni** e 5 fold, il training set ha ~142 campioni: la curva di complessità potrebbe essere poco rumorosa (piccolo dataset, poca varianza tra fold).

---

### 3. Esercizio_Titanic.ipynb

**Dataset**: Titanic (`sklearn.datasets.fetch_openml('titanic', version=1)`)  
**Task**: Classificazione binaria (target `survived`)

#### Obiettivo didattico

Affrontare un dataset "realistico" con variabili categoriche, NaN differenziati e data leakage. Si impara a:
- identificare ed eliminare le colonne con data leakage (`boat`, `body`)
- usare `OneHotEncoder` per variabili nominali vs trattare variabili ordinali come numeriche
- costruire una `Pipeline` con `ColumnTransformer` per preprocessing differenziato
- capire perché la Pipeline garantisce l'assenza di data leakage nella nested CV

#### Consegna passo-passo

1. **Carica il dataset** (`fetch_openml`), ispeziona tutte le colonne e i NaN.
2. **EDA NaN**: identifica le colonne con NaN critici. Distingui tra NaN "informativi" (boat/body = data leakage) e NaN mancanti da imputare (age, fare, embarked).
3. **EDA bivariata**: countplot `survived` vs `sex` e `survived` vs `pclass`. Verifica che il sesso sia il predittore più forte.
4. **EDA feature numeriche**: `plot_histograms` su `age`, `fare`, `sibsp`, `parch`.
5. **Comprendi la Pipeline**: leggi la cella markdown sull'encoding e il data leakage PRIMA di scrivere codice.
6. **Preprocessing**: elimina le colonne pericolose, imposta l'ordine corretto delle feature (`['age','fare','sibsp','parch','pclass','sex','embarked']`).
7. **Modello base (LR + build_titanic_pipeline)**: usa `build_titanic_pipeline(LogisticRegression(...))` con `class_weight='balanced'` e `solver='saga'`.
8. **Bias-variance (MLP + build_titanic_pipeline)**: stessa pipeline con `MLPClassifier`.

#### Differenze rispetto a Lezione 03

| Aspetto | Lezione 03 (Diabetes) | Questo esercizio |
|---|---|---|
| Feature types | Solo numeriche | Numeriche + categoriche |
| NaN | Parziali (2 colonne) | Diffusi (molte colonne) |
| Preprocessing | SimpleImputer + Scaler | ColumnTransformer multi-step |
| Encoding | Non necessario | OneHotEncoder per sex, embarked |
| Data leakage | Non presente | boat, body da eliminare |
| Pipeline | Semplice | `build_titanic_pipeline` |

#### Suggerimenti pratici

- **Ordine feature critico**: `build_titanic_pipeline` usa indici posizionali `[0,1,2,3,4]` per numeriche e `[5,6]` per categoriche. L'ordine deve essere esattamente `['age','fare','sibsp','parch','pclass','sex','embarked']`.
- **`X` come numpy array**: anche con colonne object/float miste, `np.array` funziona perché il `ColumnTransformer` gestisce i tipi internamente.
- **`class_weight='balanced'`**: il dataset è sbilanciato (~38% sopravvissuti). Senza bilanciamento, il modello tende a predire sempre "morto" con alta accuracy ma pessima recall.
- **`solver='saga'`**: necessario per supportare sia `penalty='l2'` che `penalty=None` nella griglia di iperparametri.
- **Trabocchetto comune**: dimenticare di droppare `boat` o `body` causa accuracy artificialmente alta (~95%). Se la tua accuracy è molto alta, controlla che queste colonne siano state rimosse.
- **n_features_mlp = 10**: dopo OHE, `sex` diventa 2 colonne, `embarked` 3 colonne (S/C/Q), più 5 numeriche = 10 feature totali in ingresso all'MLP.

---

### 4. Esercizio_Flights.ipynb

**Dataset**: Flights (`seaborn.load_dataset('flights')`)  
**Task**: Regressione su serie temporale (target `passengers`)

#### Obiettivo didattico

Affrontare il caso speciale delle **serie temporali**, dove l'ordine dei dati è fondamentale. Si impara a:
- capire il **data leakage temporale** causato da KFold con shuffle
- usare `TimeSeriesSplit` per rispettare la causalità
- applicare l'**encoding ciclico** (sin/cos) per variabili periodiche come il mese
- passare `outer_splitter` e `inner_cv` come splitter sklearn a `nestedKFolfCV`

#### Consegna passo-passo

1. **Carica il dataset** e visualizza la serie temporale completa (grafico lineare).
2. **Stagionalità**: traccia la media mensile dei passeggeri aggregata su tutti gli anni. Identifica il picco estivo.
3. **Feature engineering**: crea `month_num` (1-12), `month_sin`, `month_cos`, `year_num`. Ordina il DataFrame per `year_num`, `month_num`.
4. **Comprendi TimeSeriesSplit**: leggi la cella markdown obbligatoria PRIMA di costruire qualsiasi modello. È la differenza concettuale più importante di questo esercizio.
5. **Modello base (Ridge + TimeSeriesSplit)**: crea `tscv_outer = TimeSeriesSplit(n_splits=5)` e `tscv_inner = TimeSeriesSplit(n_splits=3)`. Passali a `nestedKFolfCV` come `outer_splitter=tscv_outer` e `inner_cv=tscv_inner`.
6. **Bias-variance (MLP Regressore + TimeSeriesSplit)**: usa `nested_cv_bias_variance` con `outer_splitter=TimeSeriesSplit(n_splits=5)` e `inner_cv=TimeSeriesSplit(n_splits=3)`.
7. **Plot**: `plot_complexity_curve(..., metrica_label='RMSE', higher_is_better=False)`.

#### Differenze rispetto a Lezione 03

| Aspetto | Lezione 03 (Diabetes) | Questo esercizio |
|---|---|---|
| Struttura dati | i.i.d. (indipendenti) | Serie temporale (ordinata) |
| CV splitter | KFold | TimeSeriesSplit |
| Feature month | Stringa → non usata | Encoding sin/cos |
| Feature year | Non presente | `year_num` intero |
| Metrica | Accuracy | RMSE |
| `score_multiplier` | 1 | -1 |

#### Suggerimenti pratici

- **`outer_splitter` vs `random_state`**: quando si passa `outer_splitter`, il parametro `random_state` viene ignorato per la suddivisione esterna. Questo è corretto: `TimeSeriesSplit` non ha shuffle (l'ordine è fisso).
- **`inner_cv=TimeSeriesSplit(n_splits=3)`**: il ciclo interno usa 3 fold (meno di 5) per avere training set abbastanza grandi nel ciclo interno. Con 5 fold interni e dataset piccolo, i training interni sarebbero troppo piccoli.
- **Encoding ciclico**: `month_num` grezzo (1-12) può comunque essere incluso come feature aggiuntiva accanto a sin/cos, per dare al modello più informazioni sul mese. Non è sbagliato tenerlo.
- **Trabocchetto comune**: usare `KFold(shuffle=True)` su dati temporali produce stime di performance ottimistiche perché il test set può precedere temporalmente il training. Usa sempre `TimeSeriesSplit` per dati ordinati nel tempo.
- **Varianza crescente**: il dataset Flights ha stagionalità moltiplicativa (le fluttuazioni estive crescono con il livello del traffico). Ridge e MLP additivi tendono a sottostimare nei picchi degli ultimi anni. Provare a predire `np.log(passengers)` è un'estensione interessante.
- **Attenzione ai fold di TimeSeriesSplit**: il primo fold ha un training set molto piccolo (24 campioni su 144). Questo può causare alta varianza tra i fold nella curva di complessità.
