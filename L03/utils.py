import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

from scipy.stats import pearsonr
from sklearn.model_selection import GridSearchCV, KFold

def plot_boxplots(df, variables, target='Outcome', palette=('#FFFF00', '#800080'), figsize=(18, 6)):
    """
    Disegna una griglia di boxplot di target vs variabili indipendenti,
    robusta ai valori NaN.

    Parametri:
    -----------
    df : pd.DataFrame
        Il dataframe contenente le variabili e il target
    variables : list
        Lista di nomi delle colonne da plottare
    target : str
        Nome della variabile target
    palette : tuple
        Colori dei boxplot
    figsize : tuple
        Dimensione della figura
    """
    n_vars = len(variables)
    n_cols = n_vars
    n_rows = 1
    
    fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)
    axes = axes.flatten()  # rendiamo axes 1D per iterare facilmente
    
    for i, var in enumerate(variables):
        # seleziona solo righe non NaN in target e feature corrente
        data = df[[target, var]].dropna()
        
        palette_arg = list(palette) if isinstance(palette, tuple) else palette
        sns.boxplot(
            ax=axes[i],
            x=data[target],
            y=data[var],
            hue=data[target],
            palette=palette_arg
        )
        axes[i].set_title(f"{target} vs {var}", fontsize=12)
        axes[i].legend_.remove()  # rimuoviamo la legenda ripetuta
    
    # nascondi eventuali assi vuoti
    for j in range(i+1, len(axes)):
        axes[j].set_visible(False)
    
    fig.suptitle(f'{target} Distribution WRT All Independent Variables', fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()


def plot_histograms(df, variables, bins=20, color="#800080", figsize=(18, 6)):
    """
    Disegna una griglia di istogrammi per le variabili selezionate,
    robusta ai valori NaN.

    Parametri:
    -----------
    df : pd.DataFrame
        Il dataframe contenente le variabili
    variables : list
        Lista di nomi delle colonne da plottare
    bins : int
        Numero di bin per gli istogrammi
    color : str
        Colore degli istogrammi
    figsize : tuple
        Dimensione della figura
    """
    n_vars = len(variables)
    n_cols = n_vars
    n_rows = 1

    fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)
    axes = axes.flatten()

    for i, var in enumerate(variables):
        data = df[var].dropna()
        
        axes[i].hist(data, bins=bins, color=color, edgecolor='black')
        axes[i].set_title(var, fontsize=11)
        axes[i].set_ylabel("Frequency")
    
    # Nascondi eventuali subplot vuoti
    for j in range(i + 1, len(axes)):
        axes[j].set_visible(False)

    fig.suptitle("Feature Distributions", fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()

def plot_pairplot_with_correlation(df, variables, target='Outcome', palette=('#FFFF00', '#800080'), figsize=(18, 18)):
    """
    Disegna una matrice di scatter plot (pairplot) con correlazioni di Pearson,
    simile a sns.pairplot ma con controllo completo.

    Parametri:
    -----------
    df : pd.DataFrame
        Il dataframe contenente le variabili e il target
    variables : list
        Lista di nomi delle colonne da plottare
    target : str
        Nome della variabile target per colorazione
    palette : tuple
        Colori per le classi del target (classe 0, classe 1)
    figsize : tuple
        Dimensione della figura
    """
    n_vars = len(variables)
    
    # Crea la griglia di subplot
    fig, axes = plt.subplots(n_vars, n_vars, figsize=figsize)
    
    # Prepara i dati separati per classe
    df_clean = df[variables + [target]].dropna()
    classes = df_clean[target].unique()
    default_colors = ['#FFFF00', '#800080', '#1f77b4', '#ff7f0e', '#2ca02c']
    colors = {}
    for i, cls in enumerate(sorted(df_clean[target].unique())):
        colors[cls] = palette[i] if i < len(palette) else default_colors[i % len(default_colors)]

    # Itera su tutte le combinazioni
    for i, var_y in enumerate(variables):
        for j, var_x in enumerate(variables):
            ax = axes[i, j]

            if i == j:
                # DIAGONALE: istogrammi/KDE per ogni classe
                for cls in sorted(classes):
                    data = df_clean[df_clean[target] == cls][var_x].dropna()
                    ax.hist(data, bins=20, alpha=0.6, color=colors[cls], 
                           label=f'{target}={int(cls)}', density=True)
                
                ax.set_ylabel('Density' if j == 0 else '', fontsize=10)
                ax.set_xlabel(var_x if i == n_vars - 1 else '', fontsize=10)
                
                if j == n_vars - 1:
                    ax.legend(loc='upper right', fontsize=8)
                
            else:
                # FUORI DIAGONALE: scatter plot colorato per classe
                for cls in sorted(classes):
                    data = df_clean[df_clean[target] == cls]
                    ax.scatter(data[var_x], data[var_y], 
                             alpha=0.5, s=20, color=colors[cls], 
                             label=f'{target}={int(cls)}')
                
                # Calcola correlazione di Pearson (su tutti i dati, non per classe)
                data_corr = df_clean[[var_x, var_y]].dropna()
                if len(data_corr) > 2:
                    corr, p_value = pearsonr(data_corr[var_x], data_corr[var_y])
                    
                    # Aggiungi testo con correlazione
                    # Posiziona in alto a sinistra o in basso a destra in base al segno
                    if corr >= 0:
                        text_x, text_y = 0.05, 0.95  # alto a sinistra
                        va = 'top'
                    else:
                        text_x, text_y = 0.95, 0.05  # basso a destra
                        va = 'bottom'
                    
                    ax.text(text_x, text_y, f'r={corr:.3f}', 
                           transform=ax.transAxes,
                           fontsize=10, weight='bold',
                           bbox=dict(boxstyle='round', facecolor='white', alpha=0.8),
                           verticalalignment=va,
                           horizontalalignment='left' if corr >= 0 else 'right')
                
                # Labels solo sui bordi
                ax.set_ylabel(var_y if j == 0 else '', fontsize=10)
                ax.set_xlabel(var_x if i == n_vars - 1 else '', fontsize=10)
            
            # Rimuovi tick labels interni per pulizia
            if i < n_vars - 1:
                ax.set_xticklabels([])
            if j > 0:
                ax.set_yticklabels([])
    
    fig.suptitle(f'Pairplot with Pearson Correlation - Colored by {target}', 
                 fontsize=18, y=0.995)
    plt.tight_layout(rect=[0, 0, 1, 0.99])
    plt.show()


def nestedKFolfCV(X, y, pipe, param_grid, inner_cv=5, outer_cv=5, random_state=42,
                  scoring='accuracy', outer_splitter=None):
    """
    Esegue nested K-fold cross-validation.

    Parameters:
    -----------
    X : array-like, shape (n_samples, n_features)
        Feature matrix
    y : array-like, shape (n_samples,)
        Target vector
    pipe : Pipeline
        Pipeline sklearn con preprocessing e classificatore
    param_grid : dict
        Griglia iperparametri per GridSearchCV
    inner_cv : int or CV splitter
        Numero di fold (o splitter) per CV interno (selezione iperparametri)
    outer_cv : int
        Numero di fold per CV esterno (valutazione performance); ignorato se outer_splitter è fornito
    random_state : int
        Seed per riproducibilità (ignorato se outer_splitter è fornito)
    scoring : str
        Metrica di scoring per GridSearchCV (default: 'accuracy')
    outer_splitter : CV splitter o None
        Se None usa KFold(shuffle=True); altrimenti usa lo splitter fornito (es. TimeSeriesSplit)

    Returns:
    --------
    dict con chiavi:
        - 'outer_scores': list di score per ogni fold esterno
        - 'best_params_per_fold': list di dict con migliori iperparametri per fold
        - 'best_models': list di modelli ottimi per ogni fold
        - 'mean_score': score media
        - 'std_score': deviazione standard score
    """

    if outer_splitter is None:
        outer_cv_splitter = KFold(n_splits=outer_cv, shuffle=True, random_state=random_state)
    else:
        outer_cv_splitter = outer_splitter

    # Correzione di segno: sklearn usa 'neg_*' per uniformare l'API (più alto = meglio).
    sign = -1 if scoring.startswith('neg_') else 1
    metric_label = scoring.replace('neg_', '').replace('_', ' ').upper()

    # Scorer coerente con il ciclo interno (usato per train/test esterno)
    from sklearn.metrics import check_scoring
    from sklearn.base import is_regressor
    scorer = check_scoring(pipe, scoring=scoring)

    # Rileva automaticamente se il task è regressione (per mostrare anche R²)
    final_step = pipe.steps[-1][1] if hasattr(pipe, 'steps') else pipe
    is_reg = is_regressor(final_step)

    outer_train_score = []
    outer_scores      = []
    outer_r2_scores   = []          # solo per regressione
    best_params_per_fold = []
    best_models = []

    print("=" * 80)
    print("NESTED CROSS-VALIDATION - DETAILED RESULTS")
    print("=" * 80)

    for fold_idx, (train_idx, test_idx) in enumerate(outer_cv_splitter.split(X), 1):
        X_train, X_test = X[train_idx], X[test_idx]
        y_train, y_test = y[train_idx], y[test_idx]

        # GridSearchCV sul fold esterno
        grid_search = GridSearchCV(
            estimator=pipe,
            param_grid=param_grid,
            cv=inner_cv,
            scoring=scoring,
            n_jobs=-1,
            return_train_score=True
        )

        grid_search.fit(X_train, y_train)

        best_params = grid_search.best_params_
        best_params_per_fold.append(best_params)
        best_model = grid_search.best_estimator_
        best_models.append(best_model)

        # Score esterno nella metrica primaria (sign corregge neg_*)
        train_score = sign * scorer(best_model, X_train, y_train)
        test_score  = sign * scorer(best_model, X_test,  y_test)
        outer_train_score.append(train_score)
        outer_scores.append(test_score)

        # Per regressione: R² aggiuntivo (best_model.score() = R² per qualsiasi regressore sklearn)
        if is_reg:
            train_r2 = best_model.score(X_train, y_train)
            test_r2  = best_model.score(X_test,  y_test)
            outer_r2_scores.append(test_r2)

        # Stampa risultati fold
        print(f"\nFOLD {fold_idx}:")
        print(f"  Best params            : {best_params}")
        print(f"  Best CV score (inner)  [{metric_label}]: {sign * grid_search.best_score_:.4f}")
        if is_reg:
            print(f"  Train score   (outer)  [{metric_label}]: {train_score:.4f}  [R²]: {train_r2:.4f}")
            print(f"  Test score    (outer)  [{metric_label}]: {test_score:.4f}  [R²]: {test_r2:.4f}")
        else:
            print(f"  Train score   (outer)  [{metric_label}]: {train_score:.4f}")
            print(f"  Test score    (outer)  [{metric_label}]: {test_score:.4f}")
        print(f"  Train size: {len(y_train)}, Test size: {len(y_test)}")

    # Risultati finali
    mean_train_score = np.mean(outer_train_score)
    mean_score = np.mean(outer_scores)
    std_score  = np.std(outer_scores)

    print("\n" + "=" * 80)
    print("FINAL RESULTS")
    print("=" * 80)
    print(f"Outer CV scores [{metric_label}]: {[f'{s:.4f}' for s in outer_scores]}")
    if is_reg:
        mean_r2 = np.mean(outer_r2_scores)
        std_r2  = np.std(outer_r2_scores)
        print(f"Mean score (train) [{metric_label}]: {mean_train_score:.4f}   "
              f"Mean score (test)  [{metric_label}]: {mean_score:.4f} (+/- {std_score:.4f})")
        print(f"Mean R² (test): {mean_r2:.4f} (+/- {std_r2:.4f})")
    else:
        print(f"Mean score (train) [{metric_label}]: {mean_train_score:.4f}   "
              f"Mean score (test)  [{metric_label}]: {mean_score:.4f} (+/- {std_score:.4f})")

    return {
        'outer_train_scores': outer_train_score,
        'outer_scores':        outer_scores,
        'outer_r2_scores':     outer_r2_scores if is_reg else None,
        'best_params_per_fold': best_params_per_fold,
        'best_models':         best_models,
        'mean_train_score':    mean_train_score,
        'mean_score': mean_score,
        'std_score': std_score
    }


def count_mlp_params(depth, n_units, n_features, n_classes=1):
    """
    Calcola il numero totale di parametri (pesi + bias) di un MLP uniforme.

    Parametri:
    ----------
    depth     : int  — numero di hidden layer
    n_units   : int  — neuroni per ogni hidden layer
    n_features: int  — dimensione dell'input
    n_classes : int  — neuroni nell'output layer (1 per classificazione binaria)

    Returns:
    --------
    int — numero totale di parametri
    """
    params = n_features * n_units + n_units          # primo hidden layer
    for _ in range(depth - 1):
        params += n_units * n_units + n_units         # hidden layer successivi
    params += n_units * n_classes + n_classes         # output layer
    return params


def nested_cv_bias_variance(X, y, pipe, depth_list, n_units_list, n_features,
                            inner_cv=5, outer_cv=5, n_classes=1, random_state=42,
                            scoring='accuracy', score_multiplier=1,
                            outer_splitter=None,
                            hls_param='clf__hidden_layer_sizes'):
    """
    Nested K-fold CV per la curva di complessità di un MLP (generico: classificazione o regressione).

    Esplora in un solo lancio la griglia (depth × n_units) e raccoglie
    training e validation score per ogni configurazione, mediando sui
    fold del ciclo esterno.

    Parametri:
    ----------
    X, y              : dati
    pipe              : Pipeline sklearn con step contenente hidden_layer_sizes
    depth_list        : list di int — valori di depth da esplorare
    n_units_list      : list di int — valori di n_units da esplorare
    n_features        : int — numero di feature in input
    inner_cv          : int o CV splitter — fold del ciclo interno
    outer_cv          : int — fold del ciclo esterno (ignorato se outer_splitter fornito)
    n_classes         : int — neuroni output (1 per regressione/classificazione binaria)
    random_state      : int (ignorato se outer_splitter fornito)
    scoring           : str — metrica di scoring per GridSearchCV
    score_multiplier  : float — moltiplica i cv_results_ scores (usa -1 per neg_root_mean_squared_error)
    outer_splitter    : CV splitter o None — se None usa KFold(shuffle=True)
    hls_param         : str — nome del parametro hidden_layer_sizes nella pipeline

    Returns:
    --------
    dict con:
        - 'complexity_df'       : DataFrame [depth, n_units, n_params,
                                   mean_train_acc, std_train_acc,
                                   mean_val_acc,   std_val_acc]
        - 'outer_scores'        : score test per ogni fold esterno
        - 'best_params_per_fold': migliori iperparametri per fold
        - 'best_models'         : modelli ottimi per fold
        - 'mean_score'          : score media esterna
        - 'std_score'           : deviazione standard score esterna
    """
    # Costruzione griglia
    param_configs = [
        (depth, n_units, (n_units,) * depth)
        for depth in depth_list
        for n_units in n_units_list
    ]
    param_grid = {
        hls_param: [hls for _, _, hls in param_configs]
    }

    if outer_splitter is None:
        outer_cv_split = KFold(n_splits=outer_cv, shuffle=True, random_state=random_state)
    else:
        outer_cv_split = outer_splitter

    # Correzione segno e rilevamento task (regressione → mostra anche R²)
    sign = -1 if scoring.startswith('neg_') else 1
    metric_label = scoring.replace('neg_', '').replace('_', ' ').upper()
    from sklearn.metrics import check_scoring
    from sklearn.base import is_regressor
    scorer_fn = check_scoring(pipe, scoring=scoring)
    final_step = pipe.steps[-1][1] if hasattr(pipe, 'steps') else pipe
    is_reg = is_regressor(final_step)

    train_scores_per_config = {hls: [] for _, _, hls in param_configs}
    val_scores_per_config   = {hls: [] for _, _, hls in param_configs}

    outer_scores      = []
    outer_r2_scores   = []          # solo per regressione
    best_params_per_fold = []
    best_models       = []

    print("=" * 80)
    print("NESTED CROSS-VALIDATION — BIAS-VARIANCE TRADEOFF (MLP)")
    print("=" * 80)

    for fold_idx, (train_idx, test_idx) in enumerate(outer_cv_split.split(X), 1):
        X_tr, X_te = X[train_idx], X[test_idx]
        y_tr, y_te = y[train_idx], y[test_idx]

        grid_search = GridSearchCV(
            estimator=pipe,
            param_grid=param_grid,
            cv=inner_cv,
            scoring=scoring,
            n_jobs=-1,
            return_train_score=True
        )
        grid_search.fit(X_tr, y_tr)
        cv_res = grid_search.cv_results_

        for j, p in enumerate(cv_res['params']):
            hls = p[hls_param]
            if hls in train_scores_per_config:
                train_scores_per_config[hls].append(cv_res['mean_train_score'][j] * sign)
                val_scores_per_config[hls].append(cv_res['mean_test_score'][j] * sign)

        best_params_per_fold.append(grid_search.best_params_)
        best_model = grid_search.best_estimator_
        best_models.append(best_model)

        # Score esterno coerente con ciclo interno (sign corregge neg_*)
        test_score = sign * scorer_fn(best_model, X_te, y_te)
        outer_scores.append(test_score)
        if is_reg:
            test_r2 = best_model.score(X_te, y_te)
            outer_r2_scores.append(test_r2)

        hls_best = grid_search.best_params_[hls_param]
        print(f"\nFOLD {fold_idx}:")
        print(f"  Best hidden_layer_sizes : {hls_best}")
        print(f"  Best CV score (inner)   [{metric_label}]: {sign * grid_search.best_score_:.4f}")
        if is_reg:
            print(f"  Test score    (outer)   [{metric_label}]: {test_score:.4f}  [R²]: {test_r2:.4f}")
        else:
            print(f"  Test score    (outer)   [{metric_label}]: {test_score:.4f}")

    records = []
    for depth, n_units, hls in param_configs:
        n_params = count_mlp_params(depth, n_units, n_features, n_classes)
        records.append({
            'depth'          : depth,
            'n_units'        : n_units,
            'n_params'       : n_params,
            'mean_train_acc' : np.mean(train_scores_per_config[hls]),
            'std_train_acc'  : np.std(train_scores_per_config[hls]),
            'mean_val_acc'   : np.mean(val_scores_per_config[hls]),
            'std_val_acc'    : np.std(val_scores_per_config[hls]),
        })

    complexity_df = (pd.DataFrame(records)
                     .sort_values('n_params')
                     .reset_index(drop=True))

    mean_score = np.mean(outer_scores)
    std_score  = np.std(outer_scores)

    print("\n" + "=" * 80)
    print("RISULTATI FINALI")
    print("=" * 80)
    print(f"Outer CV scores [{metric_label}]: {[f'{s:.4f}' for s in outer_scores]}")
    if is_reg:
        mean_r2 = np.mean(outer_r2_scores)
        std_r2  = np.std(outer_r2_scores)
        print(f"Mean score [{metric_label}]: {mean_score:.4f} (+/- {std_score:.4f})  "
              f"[R²]: {mean_r2:.4f} (+/- {std_r2:.4f})")
    else:
        print(f"Mean score [{metric_label}]: {mean_score:.4f} (+/- {std_score:.4f})")

    return {
        'complexity_df'       : complexity_df,
        'outer_scores'        : outer_scores,
        'outer_r2_scores'     : outer_r2_scores if is_reg else None,
        'best_params_per_fold': best_params_per_fold,
        'best_models'         : best_models,
        'mean_score'          : mean_score,
        'std_score'           : std_score,
        'mean_r2_score'       : np.mean(outer_r2_scores) if is_reg else None,
        'std_r2_score'        : np.std(outer_r2_scores)  if is_reg else None,
    }


def nested_cv_bias_variance_MLP(X, y, pipe, depth_list, n_units_list, n_features,
                             inner_cv=5, outer_cv=5, n_classes=1, random_state=42):
    """
    Nested K-fold CV per la curva di complessità di un MLP.

    Esplora in un solo lancio la griglia (depth × n_units) e raccoglie
    training e validation accuracy per ogni configurazione, mediando sui
    fold del ciclo esterno.

    Parametri:
    ----------
    X, y         : dati
    pipe         : Pipeline sklearn con step 'clf' = MLPClassifier
    depth_list   : list di int — valori di depth da esplorare
    n_units_list : list di int — valori di n_units da esplorare
    n_features   : int — numero di feature in input
    inner_cv     : int — fold del ciclo interno
    outer_cv     : int — fold del ciclo esterno
    n_classes    : int — neuroni output (1 per classificazione binaria)
    random_state : int

    Returns:
    --------
    dict con:
        - 'complexity_df'      : DataFrame [depth, n_units, n_params,
                                  mean_train_acc, std_train_acc,
                                  mean_val_acc,   std_val_acc]
        - 'outer_scores'       : accuracy test per ogni fold esterno
        - 'best_params_per_fold': migliori iperparametri per fold
        - 'best_models'        : modelli ottimi per fold
        - 'mean_score'         : accuracy media esterna
        - 'std_score'          : deviazione standard accuracy esterna
    """
    # Costruzione griglia: lista di tuple (depth, n_units, hls)
    param_configs = [
        (depth, n_units, (n_units,) * depth)
        for depth in depth_list
        for n_units in n_units_list
    ]
    # Passare le tuple come lista di valori evita che sklearn le "srotoli"
    param_grid = {
        'clf__hidden_layer_sizes': [hls for _, _, hls in param_configs]
    }

    outer_splitter = KFold(n_splits=outer_cv, shuffle=True, random_state=random_state)

    # Accumula train/val score per ogni configurazione attraverso i fold esterni
    train_scores_per_config = {hls: [] for _, _, hls in param_configs}
    val_scores_per_config   = {hls: [] for _, _, hls in param_configs}

    outer_scores       = []
    best_params_per_fold = []
    best_models        = []

    print("=" * 80)
    print("NESTED CROSS-VALIDATION — BIAS-VARIANCE TRADEOFF (MLP)")
    print("=" * 80)

    for fold_idx, (train_idx, test_idx) in enumerate(outer_splitter.split(X), 1):
        X_tr, X_te = X[train_idx], X[test_idx]
        y_tr, y_te = y[train_idx], y[test_idx]

        grid_search = GridSearchCV(
            estimator=pipe,
            param_grid=param_grid,
            cv=inner_cv,
            scoring='accuracy',
            n_jobs=-1,
            return_train_score=True
        )
        grid_search.fit(X_tr, y_tr)
        cv_res = grid_search.cv_results_

        # Abbina ogni riga di cv_results_ alla configurazione corrispondente
        for j, p in enumerate(cv_res['params']):
            hls = p['clf__hidden_layer_sizes']
            if hls in train_scores_per_config:
                train_scores_per_config[hls].append(cv_res['mean_train_score'][j])
                val_scores_per_config[hls].append(cv_res['mean_test_score'][j])

        best_params_per_fold.append(grid_search.best_params_)
        best_models.append(grid_search.best_estimator_)
        test_score = grid_search.best_estimator_.score(X_te, y_te)
        outer_scores.append(test_score)

        hls_best = grid_search.best_params_['clf__hidden_layer_sizes']
        print(f"\nFOLD {fold_idx}:")
        print(f"  Best hidden_layer_sizes : {hls_best}")
        print(f"  Best CV score (inner)   : {grid_search.best_score_:.4f}")
        print(f"  Test score   (outer)    : {test_score:.4f}")

    # Costruzione DataFrame della curva di complessità
    records = []
    for depth, n_units, hls in param_configs:
        n_params = count_mlp_params(depth, n_units, n_features, n_classes)
        records.append({
            'depth'          : depth,
            'n_units'        : n_units,
            'n_params'       : n_params,
            'mean_train_acc' : np.mean(train_scores_per_config[hls]),
            'std_train_acc'  : np.std(train_scores_per_config[hls]),
            'mean_val_acc'   : np.mean(val_scores_per_config[hls]),
            'std_val_acc'    : np.std(val_scores_per_config[hls]),
        })

    complexity_df = (pd.DataFrame(records)
                     .sort_values('n_params')
                     .reset_index(drop=True))

    mean_score = np.mean(outer_scores)
    std_score  = np.std(outer_scores)

    print("\n" + "=" * 80)
    print("RISULTATI FINALI")
    print("=" * 80)
    print(f"Outer CV scores : {[f'{s:.4f}' for s in outer_scores]}")
    print(f"Mean accuracy   : {mean_score:.4f} (+/- {std_score:.4f})")

    return {
        'complexity_df'      : complexity_df,
        'outer_scores'       : outer_scores,
        'best_params_per_fold': best_params_per_fold,
        'best_models'        : best_models,
        'mean_score'         : mean_score,
        'std_score'          : std_score,
    }


def plot_complexity_curve(complexity_df, figsize=(12, 6),
                          metrica_label='Accuracy', higher_is_better=True):
    """
    Plotta la curva di complessità (training vs validation score)
    in funzione del numero di parametri del modello.

    Parametri:
    ----------
    complexity_df    : pd.DataFrame — output di nested_cv_bias_variance['complexity_df']
    figsize          : tuple
    metrica_label    : str — etichetta asse Y e titolo (default: 'Accuracy')
    higher_is_better : bool — se False, il punto ottimale è al minimo (es. RMSE)
    """
    fig, ax = plt.subplots(figsize=figsize)
    x = complexity_df['n_params'].values

    # — Curva training
    ax.plot(x, complexity_df['mean_train_acc'], 'o-', color='#800080',
            linewidth=2, markersize=7, label=f'Training {metrica_label} (media ± std)')
    ax.fill_between(x,
                    complexity_df['mean_train_acc'] - complexity_df['std_train_acc'],
                    complexity_df['mean_train_acc'] + complexity_df['std_train_acc'],
                    alpha=0.15, color='#800080')

    # — Curva validazione
    ax.plot(x, complexity_df['mean_val_acc'], 's-', color='steelblue',
            linewidth=2, markersize=7, label=f'Validation {metrica_label} (media ± std)')
    ax.fill_between(x,
                    complexity_df['mean_val_acc'] - complexity_df['std_val_acc'],
                    complexity_df['mean_val_acc'] + complexity_df['std_val_acc'],
                    alpha=0.15, color='steelblue')

    # — Configurazione ottimale
    if higher_is_better:
        best_idx = complexity_df['mean_val_acc'].idxmax()
    else:
        best_idx = complexity_df['mean_val_acc'].idxmin()
    best_x    = complexity_df.loc[best_idx, 'n_params']
    best_y    = complexity_df.loc[best_idx, 'mean_val_acc']

    y_data_min = min(complexity_df['mean_val_acc'].min(),
                     complexity_df['mean_train_acc'].min())
    y_data_max = max(complexity_df['mean_val_acc'].max(),
                     complexity_df['mean_train_acc'].max())
    y_pad  = (y_data_max - y_data_min) * 0.08
    y_bot  = y_data_min - y_pad
    y_top  = y_data_max + y_pad

    # — Zone colorate
    ax.axvspan(x.min() * 0.5, best_x,       alpha=0.06, color='royalblue')
    ax.axvspan(best_x,         x.max() * 2,  alpha=0.06, color='tomato')
    ax.axvline(best_x, color='green', linestyle='--', linewidth=1.5, alpha=0.85)

    # — Etichette zone
    if best_idx > 0:
        mid_under = np.sqrt(x.min() * best_x)
        ax.text(mid_under, y_bot + y_pad * 0.4,
                'Underfitting', ha='center', va='bottom',
                fontsize=11, color='royalblue', alpha=0.85)
    if best_idx < len(complexity_df) - 1:
        mid_over = np.sqrt(best_x * x.max())
        ax.text(mid_over, y_bot + y_pad * 0.4,
                'Overfitting', ha='center', va='bottom',
                fontsize=11, color='tomato', alpha=0.85)

    depth_opt   = complexity_df.loc[best_idx, 'depth']
    n_units_opt = complexity_df.loc[best_idx, 'n_units']
    ax.annotate(
        f'Ottimo\ndepth={depth_opt}, units={n_units_opt}\n({best_x} param)',
        xy=(best_x, best_y),
        xytext=(best_x * 3, best_y - y_pad * 1.5),
        arrowprops=dict(arrowstyle='->', color='green', lw=1.5),
        fontsize=9, color='green',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='green', alpha=0.9)
    )

    ax.set_xscale('log')
    ax.set_xlim(x.min() * 0.5, x.max() * 2)
    ax.set_ylim(y_bot, y_top)
    ax.set_xlabel('Numero di parametri del modello (scala log)', fontsize=13)
    ax.set_ylabel(metrica_label, fontsize=13)
    ax.set_title(f'Curva di Complessità — Bias-Variance Tradeoff ({metrica_label})', fontsize=14)
    ax.legend(fontsize=11, loc='lower right')
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()


def build_titanic_pipeline(clf):
    """
    Costruisce una Pipeline sklearn per il dataset Titanic.
    Include: imputazione differenziata + OneHotEncoding categoriche + StandardScaler + clf.

    Usa indici posizionali nel ColumnTransformer, compatibile con numpy arrays.
    Ordine atteso delle colonne: ['age','fare','sibsp','parch','pclass','sex','embarked']
    -> num=[0,1,2,3,4] (age, fare, sibsp, parch, pclass)
    -> cat=[5,6]       (sex, embarked)

    Parametri:
    ----------
    clf : sklearn estimator (classificatore o regressore)

    Returns:
    --------
    Pipeline sklearn
    """
    from sklearn.pipeline import Pipeline
    from sklearn.compose import ColumnTransformer
    from sklearn.impute import SimpleImputer
    from sklearn.preprocessing import StandardScaler, OneHotEncoder

    # Indici posizionali (ordine: age, fare, sibsp, parch, pclass, sex, embarked)
    num_indices = [0, 1, 2, 3, 4]   # age, fare, sibsp, parch, pclass
    cat_indices = [5, 6]             # sex, embarked

    numeric_transformer = Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler',  StandardScaler())
    ])
    categorical_transformer = Pipeline([
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('ohe',     OneHotEncoder(handle_unknown='ignore', sparse_output=False))
    ])

    preprocessor = ColumnTransformer(transformers=[
        ('num', numeric_transformer,     num_indices),
        ('cat', categorical_transformer, cat_indices),
    ])

    return Pipeline([
        ('preprocessor', preprocessor),
        ('clf',          clf)
    ])
