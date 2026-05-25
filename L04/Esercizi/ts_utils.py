"""
ts_utils.py
===========
Modulo di utilità per il notebook Esercizio_regARIMA.ipynb.

Sezioni
-------
1. Data loading
2. EDA plots
3. CV split visualization
4. Nested Walk-Forward CV  (Ridge + MLP)
5. regARIMA modeling        (refit, ARIMA sui residui, forecast)
6. Metrics & reporting
"""

from __future__ import annotations

import warnings
from collections import Counter
from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import GridSearchCV, TimeSeriesSplit
from sklearn.neural_network import MLPRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────────────────────────────────────
# 1. DATA LOADING
# ─────────────────────────────────────────────────────────────────────────────

def load_climate_variable(
    data_dir: Path,
    filename: str,
    target_col: str,
    rename_to: str,
    fortaleza_code: int = 2304400,
) -> pd.DataFrame:
    """
    Carica un file climatico settimanale (sep=';', decimal=','), filtra il
    comune di Fortaleza (code_muni) e restituisce un DataFrame con colonne
    (iso_year, iso_week, rename_to).
    """
    df = pd.read_csv(
        data_dir / filename,
        sep=";", decimal=",", low_memory=False,
        usecols=["code_muni", "year", "week", target_col],
    )
    df = df[df["code_muni"] == fortaleza_code].copy()
    df["year"] = df["year"].astype(int)
    df["week"] = df["week"].astype(int)
    df[target_col] = pd.to_numeric(df[target_col], errors="coerce")
    return (
        df.rename(columns={"year": "iso_year", "week": "iso_week", target_col: rename_to})
          [["iso_year", "iso_week", rename_to]]
    )


# ─────────────────────────────────────────────────────────────────────────────
# 2. EDA PLOTS
# ─────────────────────────────────────────────────────────────────────────────

def plot_dengue_series(
    df: pd.DataFrame,
    dates_col: str = "calendar_start_date",
    raw_col: str = "dengue_total",
    log_col: str = "y_log",
    figsize: tuple = (14, 6),
) -> None:
    """Serie temporale dei casi grezzi e log-trasformati."""
    dates = df[dates_col]
    fig, axes = plt.subplots(2, 1, figsize=figsize, sharex=True)

    axes[0].fill_between(dates, df[raw_col], alpha=0.35, color="#800080")
    axes[0].plot(dates, df[raw_col], lw=0.8, color="#800080")
    axes[0].set_ylabel("Casi settimanali", fontsize=11)
    axes[0].set_title("Fortaleza — Dengue settimanale (2015–2024)",
                      fontsize=13, fontweight="bold")
    axes[0].yaxis.set_major_formatter(
        plt.FuncFormatter(lambda x, _: f"{int(x):,}")
    )

    axes[1].fill_between(dates, df[log_col], alpha=0.35, color="#FF8C00")
    axes[1].plot(dates, df[log_col], lw=0.8, color="#FF8C00")
    axes[1].set_ylabel(r"$y'_t = \log(y_t+1)$", fontsize=11)
    axes[1].set_xlabel("Data", fontsize=11)

    for ax in axes:
        ax.xaxis.set_major_locator(mdates.YearLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
        ax.grid(axis="y", linestyle="--", alpha=0.4)
        ax.spines[["top", "right"]].set_visible(False)

    fig.autofmt_xdate(rotation=0, ha="center")
    plt.tight_layout()
    plt.show()


def plot_climate_histograms(
    df: pd.DataFrame,
    climate_labels: dict | None = None,
    palette: list | None = None,
    figsize: tuple = (14, 4),
) -> None:
    """Istogrammi delle variabili climatiche con media, mediana e skewness."""
    if climate_labels is None:
        climate_labels = {
            "tmin": "Temperatura minima (°C)",
            "tmax": "Temperatura massima (°C)",
            "rh":   "Umidità relativa (%)",
        }
    if palette is None:
        palette = ["#1f77b4", "#d62728", "#2ca02c"]

    fig, axes = plt.subplots(1, len(climate_labels), figsize=figsize)
    for ax, (var, label), color in zip(axes, climate_labels.items(), palette):
        vals = df[var].dropna()
        ax.hist(vals, bins=30, color=color, alpha=0.75,
                edgecolor="white", linewidth=0.5)
        ax.axvline(vals.mean(),   color="black",   lw=1.5, linestyle="--",
                   label=f"media {vals.mean():.1f}")
        ax.axvline(vals.median(), color="dimgrey", lw=1.2, linestyle=":",
                   label=f"mediana {vals.median():.1f}")
        ax.set_title(label, fontsize=11, fontweight="bold")
        ax.set_xlabel("Valore settimanale", fontsize=10)
        ax.set_ylabel("Frequenza", fontsize=10)
        ax.legend(fontsize=8)
        ax.spines[["top", "right"]].set_visible(False)
        ax.text(0.97, 0.95, f"skew = {vals.skew():.2f}",
                transform=ax.transAxes, ha="right", va="top",
                fontsize=8, color="dimgrey")

    plt.suptitle(
        "Distribuzioni variabili climatiche settimanali — Fortaleza (2015–2024)",
        fontsize=12, fontweight="bold", y=1.02,
    )
    plt.tight_layout()
    plt.show()


def plot_correlation_heatmap(
    df: pd.DataFrame,
    feature_cols: list,
    climate_vars: list,
    lag_range: range,
    figsize: tuple = (16, 5),
) -> pd.DataFrame:
    """
    Heatmap di correlazione (lag climatici + y_log) e bar-chart verso il
    target. Stampa il lag ottimale per variabile. Restituisce la matrice.
    """
    corr_matrix = df[["y_log"] + feature_cols].corr()

    fig, axes = plt.subplots(
        1, 2, figsize=figsize, gridspec_kw={"width_ratios": [1, 2.8]}
    )

    corr_target = corr_matrix["y_log"].drop("y_log").sort_values()
    colors = ["#d62728" if v > 0 else "#1f77b4" for v in corr_target]
    axes[0].barh(corr_target.index, corr_target.values, color=colors, alpha=0.8)
    axes[0].axvline(0, color="black", lw=0.8)
    axes[0].set_xlabel(r"Correlazione di Pearson con $y'_t$", fontsize=10)
    axes[0].set_title("Correlazione lag → dengue", fontsize=11, fontweight="bold")
    axes[0].spines[["top", "right"]].set_visible(False)
    for i, val in enumerate(corr_target.values):
        axes[0].text(
            val + 0.01 * np.sign(val), i, f"{val:.2f}",
            va="center", ha="left" if val >= 0 else "right", fontsize=7.5,
        )

    mask = np.triu(np.ones_like(corr_matrix, dtype=bool), k=1)
    sns.heatmap(
        corr_matrix, mask=mask, annot=True, fmt=".2f", cmap="RdBu_r",
        center=0, vmin=-1, vmax=1, linewidths=0.4,
        annot_kws={"size": 7}, ax=axes[1], cbar_kws={"shrink": 0.7},
    )
    axes[1].set_title(
        "Matrice di correlazione (lag climatici + target)",
        fontsize=11, fontweight="bold",
    )
    axes[1].tick_params(axis="x", rotation=45, labelsize=8)
    axes[1].tick_params(axis="y", rotation=0,  labelsize=8)

    plt.suptitle(
        "EDA — Relazioni tra lag climatici e incidenza dengue (log)",
        fontsize=12, fontweight="bold", y=1.02,
    )
    plt.tight_layout()
    plt.show()

    print("\nLag con correlazione assoluta massima verso y_log:")
    for var in climate_vars:
        lag_cols = [f"{var}_lag{l}" for l in lag_range]
        best   = corr_matrix.loc[lag_cols, "y_log"].abs().idxmax()
        best_r = corr_matrix.loc[best, "y_log"]
        print(f"  {var:4s}  →  {best}  (r = {best_r:+.3f})")

    return corr_matrix


# ─────────────────────────────────────────────────────────────────────────────
# 3. CV SPLIT VISUALIZATION
# ─────────────────────────────────────────────────────────────────────────────

def plot_cv_splits(
    df: pd.DataFrame,
    X_all: np.ndarray,
    n_outer: int,
    horizon: int,
    dates_col: str = "calendar_start_date",
    figsize: tuple = (13, 3),
) -> None:
    """Barchart orizzontale degli outer fold (train=viola, val=arancio) + riepilogo date."""
    outer_tss = TimeSeriesSplit(n_splits=n_outer, test_size=horizon)
    fig, ax = plt.subplots(figsize=figsize)

    for fold_idx, (tr_idx, val_idx) in enumerate(outer_tss.split(X_all), 1):
        ax.barh(fold_idx, len(tr_idx), left=0, height=0.5,
                color="#800080", alpha=0.6,
                label="Train" if fold_idx == 1 else "")
        ax.barh(fold_idx, len(val_idx), left=len(tr_idx), height=0.5,
                color="#FF8C00", alpha=0.8,
                label="Val" if fold_idx == 1 else "")

    ax.set_xlabel("Indice settimana (campioni)", fontsize=10)
    ax.set_ylabel("Fold esterno", fontsize=10)
    ax.set_yticks(range(1, n_outer + 1))
    ax.set_title(
        f"Nested Expanding Window CV — {n_outer} fold esterni × {horizon} sett. di test",
        fontsize=11, fontweight="bold",
    )
    ax.legend(loc="lower right", fontsize=9)
    ax.spines[["top", "right"]].set_visible(False)
    plt.tight_layout()
    plt.show()

    print(f"Dataset: {len(X_all)} campioni totali")
    for fold_idx, (tr, va) in enumerate(outer_tss.split(X_all), 1):
        print(
            f"  Fold {fold_idx}: train={len(tr):4d} sett.  "
            f"({df[dates_col].iloc[tr[0]].date()} → "
            f"{df[dates_col].iloc[tr[-1]].date()})  |  "
            f"val={len(va)} sett.  "
            f"({df[dates_col].iloc[va[0]].date()} → "
            f"{df[dates_col].iloc[va[-1]].date()})"
        )


# ─────────────────────────────────────────────────────────────────────────────
# 4. NESTED WALK-FORWARD CV
# ─────────────────────────────────────────────────────────────────────────────

def _count_mlp_params(depth: int, n_units: int, n_features: int,
                      n_output: int = 1) -> int:
    sizes = [n_features] + [n_units] * depth + [n_output]
    return sum(sizes[i] * sizes[i + 1] + sizes[i + 1] for i in range(len(sizes) - 1))


def nested_walk_forward_bias_variance_ridge(
    X: np.ndarray,
    y: np.ndarray,
    alpha_list: list,
    n_outer: int = 5,
    n_inner: int = 3,
    min_train_size: int = 52,
    horizon: int = 52,
    verbose: bool = True,
) -> dict:
    """
    Nested Walk-Forward CV (expanding window) per Ridge Regression.

    Ciclo esterno : TimeSeriesSplit(test_size=horizon) — valuta la
                    generalizzazione temporale del modello.
    Ciclo interno : TimeSeriesSplit — seleziona alpha su ogni training esterno.
    StandardScaler è incapsulato nella Pipeline → fittato solo sul training
    di ogni fold, mai sul validation (no data leakage).

    Parametri
    ----------
    X, y           : array numpy
    alpha_list     : griglia di regolarizzazione (es. [0.001, 0.01, 1, 10, …])
    n_outer        : fold del ciclo esterno
    n_inner        : fold del ciclo interno
    min_train_size : fold con meno righe vengono saltati
    horizon        : settimane di test per fold esterno
    verbose        : stampa progress

    Ritorna
    -------
    dict con complexity_df, outer_rmse_folds, outer_r2_folds,
    best_params_per_fold, best_models, mean/std rmse/r2
    """
    pipe = Pipeline([("scaler", StandardScaler()), ("ridge", Ridge())])
    param_grid = {"ridge__alpha": alpha_list}
    outer_tss  = TimeSeriesSplit(n_splits=n_outer, test_size=horizon)
    inner_tss  = TimeSeriesSplit(n_splits=n_inner)

    train_scores = {a: [] for a in alpha_list}
    val_scores   = {a: [] for a in alpha_list}
    outer_rmse, outer_r2 = [], []
    best_params_per_fold, best_models = [], []

    if verbose:
        print("=" * 72)
        print("NESTED WALK-FORWARD CV — Ridge Regression (Expanding Window)")
        print(f"  Outer: {n_outer} fold × {horizon} sett.  |  Inner: {n_inner} fold")
        print(f"  Alpha grid ({len(alpha_list)}): {alpha_list}")
        print("=" * 72)

    for fold_idx, (tr_idx, val_idx) in enumerate(outer_tss.split(X), 1):
        if len(tr_idx) < min_train_size:
            if verbose:
                print(f"  [Fold {fold_idx}] Skipped (N_train={len(tr_idx)})")
            continue

        X_tr, X_val = X[tr_idx], X[val_idx]
        y_tr, y_val = y[tr_idx], y[val_idx]

        gs = GridSearchCV(pipe, param_grid, cv=inner_tss,
                          scoring="neg_root_mean_squared_error",
                          n_jobs=-1, return_train_score=True)
        gs.fit(X_tr, y_tr)
        cv_res = gs.cv_results_

        for j, p in enumerate(cv_res["params"]):
            a = p["ridge__alpha"]
            train_scores[a].append(-cv_res["mean_train_score"][j])
            val_scores[a].append(  -cv_res["mean_test_score"][j])

        best_params_per_fold.append(gs.best_params_)
        best_models.append(gs.best_estimator_)

        val_preds = gs.best_estimator_.predict(X_val)
        rmse_val  = float(np.sqrt(mean_squared_error(y_val, val_preds)))
        ss_res    = float(np.sum((y_val - val_preds) ** 2))
        ss_tot    = float(np.sum((y_val - y_val.mean()) ** 2))
        r2_val    = 1.0 - ss_res / ss_tot if ss_tot > 0 else np.nan
        outer_rmse.append(rmse_val)
        outer_r2.append(r2_val)

        if verbose:
            print(
                f"  [Fold {fold_idx}]  N_train={len(tr_idx):4d}  "
                f"best_α={gs.best_params_['ridge__alpha']:8.4f}  "
                f"Inner-RMSE={-gs.best_score_:.4f}  "
                f"Outer-RMSE={rmse_val:.4f}  R²={r2_val:.4f}"
            )

    complexity_df = pd.DataFrame([
        {
            "alpha":           a,
            "log_alpha":       np.log10(a),
            "mean_train_rmse": np.mean(train_scores[a]),
            "std_train_rmse":  np.std(train_scores[a]),
            "mean_val_rmse":   np.mean(val_scores[a]),
            "std_val_rmse":    np.std(val_scores[a]),
        }
        for a in alpha_list
    ])

    mean_rmse = float(np.mean(outer_rmse))
    std_rmse  = float(np.std(outer_rmse))
    mean_r2   = float(np.mean(outer_r2))
    std_r2    = float(np.std(outer_r2))

    if verbose:
        print(f"\n  RMSE esterno: {mean_rmse:.4f} ± {std_rmse:.4f}")
        print(f"  R²   esterno: {mean_r2:.4f} ± {std_r2:.4f}")

    return {
        "complexity_df":        complexity_df,
        "outer_rmse_folds":     outer_rmse,
        "outer_r2_folds":       outer_r2,
        "best_params_per_fold": best_params_per_fold,
        "best_models":          best_models,
        "mean_rmse": mean_rmse, "std_rmse": std_rmse,
        "mean_r2":   mean_r2,   "std_r2":   std_r2,
    }


def nested_walk_forward_bias_variance_mlp(
    X: np.ndarray,
    y: np.ndarray,
    depth_list: list,
    n_units_list: list,
    n_features: int,
    n_outer: int = 5,
    n_inner: int = 3,
    min_train_size: int = 52,
    horizon: int = 52,
    max_iter: int = 500,
    random_state: int = 42,
    verbose: bool = True,
) -> dict:
    """
    Nested Walk-Forward CV (expanding window) per MLP Regressor.

    La griglia di complessità è il prodotto cartesiano depth_list × n_units_list.
    Ogni configurazione è identificata da hidden_layer_sizes = (n_units,)*depth.
    StandardScaler incapsulato nella Pipeline → no leakage.

    Parametri
    ----------
    X, y           : array numpy
    depth_list     : profondità da esplorare (es. [1, 2, 3])
    n_units_list   : neuroni per strato (es. [16, 32, 64, 128])
    n_features     : numero di feature (per contare i parametri)
    n_outer        : fold esterni
    n_inner        : fold interni
    min_train_size : fold con meno righe vengono saltati
    horizon        : settimane di test per fold esterno
    max_iter       : iterazioni massime MLPRegressor
    random_state   : seed
    verbose        : stampa progress

    Ritorna
    -------
    dict con complexity_df, outer_rmse_folds, outer_r2_folds,
    best_params_per_fold, best_models, mean/std rmse/r2
    """
    param_configs = [
        (depth, n_units, (n_units,) * depth)
        for depth in depth_list
        for n_units in n_units_list
    ]
    hls_list   = [hls for _, _, hls in param_configs]
    param_grid = {"mlp__hidden_layer_sizes": hls_list}

    pipe = Pipeline([
        ("scaler", StandardScaler()),
        ("mlp", MLPRegressor(max_iter=max_iter, random_state=random_state)),
    ])
    outer_tss = TimeSeriesSplit(n_splits=n_outer, test_size=horizon)
    inner_tss = TimeSeriesSplit(n_splits=n_inner)

    train_scores = {hls: [] for hls in hls_list}
    val_scores   = {hls: [] for hls in hls_list}
    outer_rmse, outer_r2 = [], []
    best_params_per_fold, best_models = [], []

    if verbose:
        print("=" * 72)
        print("NESTED WALK-FORWARD CV — MLP Regressor (Expanding Window)")
        print(f"  Outer: {n_outer} fold × {horizon} sett.  |  Inner: {n_inner} fold")
        print(f"  Griglia: {len(param_configs)} config "
              f"(depth={depth_list} × units={n_units_list})")
        print("=" * 72)

    for fold_idx, (tr_idx, val_idx) in enumerate(outer_tss.split(X), 1):
        if len(tr_idx) < min_train_size:
            if verbose:
                print(f"  [Fold {fold_idx}] Skipped (N_train={len(tr_idx)})")
            continue

        X_tr, X_val = X[tr_idx], X[val_idx]
        y_tr, y_val = y[tr_idx], y[val_idx]

        gs = GridSearchCV(pipe, param_grid, cv=inner_tss,
                          scoring="neg_root_mean_squared_error",
                          n_jobs=-1, return_train_score=True)
        gs.fit(X_tr, y_tr)
        cv_res = gs.cv_results_

        for j, p in enumerate(cv_res["params"]):
            hls = p["mlp__hidden_layer_sizes"]
            if hls in train_scores:
                train_scores[hls].append(-cv_res["mean_train_score"][j])
                val_scores[hls].append(  -cv_res["mean_test_score"][j])

        best_params_per_fold.append(gs.best_params_)
        best_models.append(gs.best_estimator_)

        val_preds = gs.best_estimator_.predict(X_val)
        rmse_val  = float(np.sqrt(mean_squared_error(y_val, val_preds)))
        ss_res    = float(np.sum((y_val - val_preds) ** 2))
        ss_tot    = float(np.sum((y_val - y_val.mean()) ** 2))
        r2_val    = 1.0 - ss_res / ss_tot if ss_tot > 0 else np.nan
        outer_rmse.append(rmse_val)
        outer_r2.append(r2_val)

        if verbose:
            print(
                f"  [Fold {fold_idx}]  N_train={len(tr_idx):4d}  "
                f"best_hls={str(gs.best_params_['mlp__hidden_layer_sizes']):18s}  "
                f"Inner-RMSE={-gs.best_score_:.4f}  "
                f"Outer-RMSE={rmse_val:.4f}  R²={r2_val:.4f}"
            )

    complexity_df = pd.DataFrame([
        {
            "depth":              depth,
            "n_units":            n_units,
            "n_params":           _count_mlp_params(depth, n_units, n_features),
            "hidden_layer_sizes": hls,
            "mean_train_rmse":    np.mean(train_scores[hls]),
            "std_train_rmse":     np.std(train_scores[hls]),
            "mean_val_rmse":      np.mean(val_scores[hls]),
            "std_val_rmse":       np.std(val_scores[hls]),
        }
        for depth, n_units, hls in param_configs
    ]).sort_values("n_params").reset_index(drop=True)

    mean_rmse = float(np.mean(outer_rmse))
    std_rmse  = float(np.std(outer_rmse))
    mean_r2   = float(np.mean(outer_r2))
    std_r2    = float(np.std(outer_r2))

    if verbose:
        print(f"\n  RMSE esterno: {mean_rmse:.4f} ± {std_rmse:.4f}")
        print(f"  R²   esterno: {mean_r2:.4f} ± {std_r2:.4f}")

    return {
        "complexity_df":        complexity_df,
        "outer_rmse_folds":     outer_rmse,
        "outer_r2_folds":       outer_r2,
        "best_params_per_fold": best_params_per_fold,
        "best_models":          best_models,
        "mean_rmse": mean_rmse, "std_rmse": std_rmse,
        "mean_r2":   mean_r2,   "std_r2":   std_r2,
    }


def plot_walk_forward_complexity(
    results: dict,
    model_name: str = "Modello",
    x_col: str = "log_alpha",
    x_label: str = r"$\log_{10}(\alpha)$  [← più complesso | meno complesso →]",
    figsize: tuple = (13, 5),
) -> None:
    """
    Curva bias-varianza (pannello sx) + boxplot RMSE fold esterni (pannello dx).

    Parametri
    ----------
    results    : dict da nested_walk_forward_bias_variance_ridge/mlp
    model_name : etichetta per titoli
    x_col      : colonna complexity_df sull'asse x ('log_alpha' o 'n_params')
    x_label    : etichetta asse x
    """
    df  = results["complexity_df"]
    fig, axes = plt.subplots(1, 2, figsize=figsize)

    x = df[x_col].values
    ax = axes[0]
    ax.plot(x, df["mean_train_rmse"], "o-", color="#800080", lw=2,
            label="Train RMSE (inner)")
    ax.fill_between(x,
                    df["mean_train_rmse"] - df["std_train_rmse"],
                    df["mean_train_rmse"] + df["std_train_rmse"],
                    alpha=0.15, color="#800080")
    ax.plot(x, df["mean_val_rmse"], "s--", color="#FF8C00", lw=2,
            label="Val RMSE (inner)")
    ax.fill_between(x,
                    df["mean_val_rmse"] - df["std_val_rmse"],
                    df["mean_val_rmse"] + df["std_val_rmse"],
                    alpha=0.15, color="#FF8C00")
    best_idx = df["mean_val_rmse"].idxmin()
    ax.axvline(x[best_idx], color="black", lw=1.2, linestyle=":",
               label=f"Ottimo: {x[best_idx]:.2f}")
    ax.set_xlabel(x_label, fontsize=10)
    ax.set_ylabel("RMSE (spazio log)", fontsize=10)
    ax.set_title(f"{model_name} — Curva bias-varianza\n"
                 "(inner walk-forward, media fold esterni)",
                 fontsize=11, fontweight="bold")
    ax.legend(fontsize=9)
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    ax.spines[["top", "right"]].set_visible(False)

    ax2 = axes[1]
    outer = results["outer_rmse_folds"]
    bp = ax2.boxplot(outer, patch_artist=True, widths=0.5,
                     medianprops={"color": "k", "linewidth": 2})
    bp["boxes"][0].set_facecolor("#1f77b4")
    bp["boxes"][0].set_alpha(0.55)
    ax2.scatter([1] * len(outer), outer, color="#1f77b4", zorder=3, s=40, alpha=0.8)
    ax2.set_xticks([1])
    ax2.set_xticklabels([model_name])
    ax2.set_ylabel("RMSE esterno (spazio log)", fontsize=10)
    ax2.set_title(
        f"Stabilità — RMSE per fold esterno\n"
        f"μ={results['mean_rmse']:.4f}  σ={results['std_rmse']:.4f}",
        fontsize=11, fontweight="bold",
    )
    ax2.grid(axis="y", linestyle="--", alpha=0.4)
    ax2.spines[["top", "right"]].set_visible(False)

    plt.suptitle(f"Nested Walk-Forward CV — {model_name}",
                 fontsize=12, fontweight="bold", y=1.02)
    plt.tight_layout()
    plt.show()


def plot_model_comparison(
    ridge_results: dict,
    mlp_results: dict,
    figsize: tuple = (13, 4),
) -> None:
    """Boxplot RMSE e R² per fold esterno: Ridge vs MLP a confronto diretto."""
    fig, axes = plt.subplots(1, 2, figsize=figsize)
    labels = ["Ridge", "MLP"]
    colors = ["#800080", "#1f77b4"]

    for ax, metric, ylabel, title in [
        (axes[0], "outer_rmse_folds", "RMSE esterno (spazio log)", "Confronto RMSE — Outer fold"),
        (axes[1], "outer_r2_folds",   "R² esterno",                "Confronto R²   — Outer fold"),
    ]:
        data = [ridge_results[metric], mlp_results[metric]]
        bp   = ax.boxplot(data, patch_artist=True, widths=0.5,
                          medianprops={"color": "k", "linewidth": 2})
        for patch, col in zip(bp["boxes"], colors):
            patch.set_facecolor(col)
            patch.set_alpha(0.55)
        for xi, (vals, col) in enumerate(zip(data, colors), 1):
            ax.scatter([xi] * len(vals), vals, color=col, zorder=3, s=40, alpha=0.9)
        ax.set_xticklabels(labels)
        ax.set_ylabel(ylabel, fontsize=10)
        ax.set_title(title, fontsize=11, fontweight="bold")
        ax.grid(axis="y", linestyle="--", alpha=0.4)
        ax.spines[["top", "right"]].set_visible(False)

    plt.suptitle("Ridge vs MLP — Nested Walk-Forward CV",
                 fontsize=12, fontweight="bold", y=1.02)
    plt.tight_layout()
    plt.show()

    print("\nRiepilogo:")
    for name, res in [("Ridge", ridge_results), ("MLP", mlp_results)]:
        print(f"  {name:5s}  RMSE={res['mean_rmse']:.4f}±{res['std_rmse']:.4f}  "
              f"R²={res['mean_r2']:.4f}±{res['std_r2']:.4f}")


# ─────────────────────────────────────────────────────────────────────────────
# 5. REGARIMA MODELING
# ─────────────────────────────────────────────────────────────────────────────

def select_best_hyperparam(results: dict, param_key: str):
    """
    Restituisce l'iperparametro più frequente (maggioranza dei fold nested CV).

    Esempio
    -------
    best_alpha = select_best_hyperparam(ridge_results, "ridge__alpha")
    best_hls   = select_best_hyperparam(mlp_results,   "mlp__hidden_layer_sizes")
    """
    vals = [p[param_key] for p in results["best_params_per_fold"]]
    return Counter(vals).most_common(1)[0][0]


def refit_on_train(
    X_train: np.ndarray,
    y_train: np.ndarray,
    model_type: str,
    best_value,
    max_iter: int = 1000,
    random_state: int = 42,
) -> Pipeline:
    """
    Costruisce e fitta una Pipeline (StandardScaler + modello) sull'intero
    training set con l'iperparametro ottimale selezionato dalla nested CV.

    Parametri
    ----------
    model_type : "ridge" oppure "mlp"
    best_value : float (alpha Ridge) o tuple (hidden_layer_sizes MLP)
    """
    if model_type == "ridge":
        estimator = Ridge(alpha=best_value)
    elif model_type == "mlp":
        estimator = MLPRegressor(
            hidden_layer_sizes=best_value,
            max_iter=max_iter, random_state=random_state,
        )
    else:
        raise ValueError(f"model_type deve essere 'ridge' o 'mlp', non '{model_type}'")

    pipe = Pipeline([("scaler", StandardScaler()), ("model", estimator)])
    pipe.fit(X_train, y_train)
    return pipe


def plot_residual_acf_pacf(
    residuals: np.ndarray,
    lags: int = 40,
    figsize: tuple = (12, 4),
) -> None:
    """ACF e PACF dei residui di regressione per identificare l'ordine ARIMA."""
    from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

    fig, axes = plt.subplots(1, 2, figsize=figsize)
    plot_acf( residuals, lags=lags, ax=axes[0], alpha=0.05)
    plot_pacf(residuals, lags=lags, ax=axes[1], alpha=0.05, method="ywm")

    axes[0].set_title("ACF — Residui della regressione",  fontsize=11, fontweight="bold")
    axes[1].set_title("PACF — Residui della regressione", fontsize=11, fontweight="bold")
    for ax in axes:
        ax.spines[["top", "right"]].set_visible(False)

    plt.suptitle("Diagnostica residui: ACF e PACF",
                 fontsize=12, fontweight="bold", y=1.02)
    plt.tight_layout()
    plt.show()


def fit_arima_on_residuals(
    residuals_train: np.ndarray,
    arima_orders: list,
    n_inner: int = 3,
    min_train_size: int = 52,
    verbose: bool = True,
) -> dict:
    """
    Seleziona il miglior ARIMA(p,d,q) per i residui di regressione via inner
    TimeSeriesSplit, poi fitta il modello scelto sull'intero vettore residui.

    Parametri
    ----------
    residuals_train : array 1-D dei residui sul training set
    arima_orders    : lista di tuple (p,d,q) da esplorare
    n_inner         : fold del ciclo interno
    min_train_size  : minima dimensione del training interno
    verbose         : stampa progress

    Ritorna
    -------
    dict con best_order, fitted_model, order_rmses, residuals_of_residuals
    """
    from statsmodels.tsa.statespace.sarimax import SARIMAX

    inner_tss   = TimeSeriesSplit(n_splits=n_inner)
    best_order  = None
    best_rmse   = np.inf
    order_rmses = []

    if verbose:
        print("=" * 60)
        print("  INNER CV — selezione ordine ARIMA sui residui")
        print(f"  Grid: {len(arima_orders)} ordini  |  Inner fold: {n_inner}")
        print("=" * 60)

    for order in arima_orders:
        fold_rmses = []
        skip = False
        for tr_idx, val_idx in inner_tss.split(residuals_train):
            if len(tr_idx) < min_train_size:
                skip = True
                break
            try:
                mod  = SARIMAX(residuals_train[tr_idx], order=order, trend="n",
                               enforce_stationarity=False, enforce_invertibility=False)
                fit  = mod.fit(disp=False, method="lbfgs", maxiter=200)
                pred = np.asarray(fit.forecast(steps=len(val_idx)))
                fold_rmses.append(
                    float(np.sqrt(mean_squared_error(residuals_train[val_idx], pred)))
                )
            except Exception:
                fold_rmses.append(np.inf)

        if skip or not fold_rmses:
            continue

        mean_rmse = float(np.mean(fold_rmses))
        order_rmses.append({"order": order, "inner_rmse": mean_rmse})
        if verbose:
            print(f"  ARIMA{order}  Inner-RMSE={mean_rmse:.4f}")

        if mean_rmse < best_rmse:
            best_rmse  = mean_rmse
            best_order = order

    if verbose:
        print(f"\n  → Best order: ARIMA{best_order}  (RMSE={best_rmse:.4f})")
        print("  Fit finale su tutti i residui di training…")

    mod_final = SARIMAX(residuals_train, order=best_order, trend="n",
                        enforce_stationarity=False, enforce_invertibility=False)
    fit_final = mod_final.fit(disp=False, method="lbfgs", maxiter=300)

    return {
        "best_order":             best_order,
        "best_inner_rmse":        best_rmse,
        "order_rmses":            sorted(order_rmses, key=lambda x: x["inner_rmse"]),
        "fitted_model":           fit_final,
        "residuals_of_residuals": np.asarray(fit_final.resid),
    }


def regarima_forecast(
    reg_model: Pipeline,
    X_test: np.ndarray,
    arima_fit,
    verbose: bool = True,
) -> dict:
    """
    Forecast finale regARIMA sul test set:

        ŷ_t = m̂(x_t)   +   ARIMA_forecast(ê_t)
               regressione    componente stocastica

    Parametri
    ----------
    reg_model : Pipeline fittata (scaler + regressor)
    X_test    : feature matrix del test set
    arima_fit : modello SARIMAX fittato sui residui di training

    Ritorna
    -------
    dict con reg_preds, arima_fc, combined
    """
    n_test    = len(X_test)
    reg_preds = reg_model.predict(X_test)
    arima_fc  = np.asarray(arima_fit.forecast(steps=n_test))
    combined  = reg_preds + arima_fc

    if verbose:
        print(f"Test set: {n_test} settimane")
        print(f"  Regressione    — media: {reg_preds.mean():.3f}  std: {reg_preds.std():.3f}")
        print(f"  ARIMA forecast — media: {arima_fc.mean():.3f}   std: {arima_fc.std():.3f}")
        print(f"  Combinato      — media: {combined.mean():.3f}   std: {combined.std():.3f}")

    return {"reg_preds": reg_preds, "arima_fc": arima_fc, "combined": combined}


def plot_regarima_forecast(
    df: pd.DataFrame,
    y_all: np.ndarray,
    n_test: int,
    reg_preds_train: np.ndarray,
    fc: dict,
    dates_col: str = "calendar_start_date",
    figsize: tuple = (14, 5),
) -> None:
    """
    Visualizza il forecast regARIMA finale.

    - Grigio : osservato (train)
    - Nero   : osservato (test)
    - Viola  : fit regressione in-sample (train)
    - Blu    : forecast regressione (test)
    - Rosso  : forecast regARIMA = regressione + ARIMA (test)

    Parametri
    ----------
    fc              : dict da regarima_forecast()
    reg_preds_train : predizioni della regressione sul training (fit in-sample)
    """
    dates       = df[dates_col]
    dates_train = dates.iloc[:-n_test]
    dates_test  = dates.iloc[-n_test:]
    y_train     = y_all[:-n_test]
    y_test      = y_all[-n_test:]

    fig, ax = plt.subplots(figsize=figsize)

    ax.plot(dates_train, y_train,         color="grey",    lw=0.8, alpha=0.5,
            label="Osservato (train)")
    ax.plot(dates_test,  y_test,          color="black",   lw=1.8,
            label="Osservato (test)")
    ax.plot(dates_train, reg_preds_train, color="#800080", lw=1.2, alpha=0.7,
            linestyle="--", label="Regressione fit (train)")
    ax.plot(dates_test,  fc["reg_preds"], color="#1f77b4", lw=1.5, alpha=0.85,
            linestyle="--", label="Regressione forecast (test)")
    ax.plot(dates_test,  fc["combined"],  color="#d62728", lw=2.2,
            label="regARIMA forecast (test)")

    ax.axvline(dates.iloc[-n_test], color="black", lw=1,
               linestyle=":", alpha=0.5, label="Inizio test set")

    ax.set_xlabel("Data", fontsize=10)
    ax.set_ylabel(r"$y'_t = \log(\text{dengue}+1)$", fontsize=10)
    ax.set_title("Previsione finale regARIMA — Fortaleza (Brasile)",
                 fontsize=12, fontweight="bold")
    ax.legend(fontsize=9, loc="upper left")
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    ax.spines[["top", "right"]].set_visible(False)
    fig.autofmt_xdate(rotation=0, ha="center")
    plt.tight_layout()
    plt.show()


# ─────────────────────────────────────────────────────────────────────────────
# 6. METRICS & REPORTING
# ─────────────────────────────────────────────────────────────────────────────

def compute_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> dict:
    """Restituisce RMSE, MAE e R² (nello spazio di y_true, tipicamente log)."""
    rmse   = float(np.sqrt(mean_squared_error(y_true, y_pred)))
    mae    = float(np.mean(np.abs(y_true - y_pred)))
    ss_res = float(np.sum((y_true - y_pred) ** 2))
    ss_tot = float(np.sum((y_true - y_true.mean()) ** 2))
    r2     = float(1.0 - ss_res / ss_tot) if ss_tot > 0 else np.nan
    return {"RMSE": rmse, "MAE": mae, "R²": r2}


def print_metrics_table(metrics_dict: dict) -> None:
    """
    Stampa una tabella RMSE / MAE / R² per più modelli.

    Parametri
    ----------
    metrics_dict : {"Nome modello": compute_metrics(y_true, y_pred), …}
    """
    print("=" * 54)
    print(f"{'Modello':<22} {'RMSE':>8} {'MAE':>8} {'R²':>8}")
    print("-" * 54)
    for name, m in metrics_dict.items():
        print(f"{name:<22} {m['RMSE']:>8.4f} {m['MAE']:>8.4f} {m['R²']:>8.4f}")
    print("=" * 54)
