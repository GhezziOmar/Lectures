"""
utilities.py – Funzioni di supporto per il caso studio OpenDengue
=================================================================
Pipeline statistica completa: EDA, feature engineering, model selection,
sliding-window cross-validation, diagnostica dei residui e valutazione
predittiva per serie storiche settimanali.

Dipendenze: numpy, pandas, matplotlib, seaborn, scipy, sklearn, statsmodels
"""

import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
from scipy import stats
from scipy.stats import norm, probplot
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import TimeSeriesSplit
from sklearn.preprocessing import StandardScaler


# ─────────────────────────────────────────────────────────────────────────────
# STILE GRAFICO GLOBALE
# ─────────────────────────────────────────────────────────────────────────────

PALETTE = {
    "blue":      "#2C7BB6",
    "red":       "#D7191C",
    "green":     "#1A9641",
    "orange":    "#FDAE61",
    "gray":      "#7B7B7B",
    "purple":    "#7B2D8B",
    "teal":      "#00827F",
    "brown":     "#8B4513",
}

plt.rcParams.update({
    "figure.dpi":          110,
    "axes.spines.top":     False,
    "axes.spines.right":   False,
    "axes.grid":           True,
    "axes.grid.axis":      "y",
    "grid.alpha":          0.3,
    "grid.linestyle":      "--",
    "font.size":           11,
    "axes.titlesize":      13,
    "axes.labelsize":      11,
    "legend.fontsize":     10,
})


# ─────────────────────────────────────────────────────────────────────────────
# 1.  CARICAMENTO E PREPARAZIONE DEI DATI
# ─────────────────────────────────────────────────────────────────────────────

def load_dengue_national(zip_path: str) -> pd.DataFrame:
    """
    Carica National_extract di OpenDengue direttamente dallo zip.

    Parameters
    ----------
    zip_path : str
        Percorso al file National_extract_V1_3.zip

    Returns
    -------
    pd.DataFrame con parse_dates su calendar_start_date e calendar_end_date.
    """
    import zipfile
    with zipfile.ZipFile(zip_path) as z:
        csv_name = [n for n in z.namelist() if n.endswith(".csv")][0]
        with z.open(csv_name) as f:
            df = pd.read_csv(
                f,
                parse_dates=["calendar_start_date", "calendar_end_date"],
                low_memory=False,
            )
    return df


def prepare_country_weekly(df: pd.DataFrame, country: str) -> pd.DataFrame:
    """
    Estrae la serie settimanale (T_res == 'Week') per un paese,
    elimina i duplicati per data, la ordina e aggiunge:
        - date        : data di inizio settimana (datetime)
        - Year        : anno ISO
        - week_iso    : settimana ISO (1–53)
        - t_cal       : settimane trascorse dal primo osservazione (float)
        - log_dengue  : log(dengue_total + 1)

    Parameters
    ----------
    df : pd.DataFrame
        Output di load_dengue_national()
    country : str
        Nome del paese in maiuscolo (es. 'NICARAGUA')

    Returns
    -------
    pd.DataFrame ordinato per data, senza duplicati.
    """
    sub = (
        df[(df["adm_0_name"] == country) & (df["T_res"] == "Week")]
        .rename(columns={"calendar_start_date": "date"})
        .sort_values("date")
        .drop_duplicates("date")
        .copy()
    )
    sub = sub[["date", "Year", "dengue_total"]].reset_index(drop=True)
    sub["week_iso"] = sub["date"].dt.isocalendar().week.astype(int)
    ref = sub["date"].iloc[0]
    sub["t_cal"] = (sub["date"] - ref).dt.days / 7.0
    sub["log_dengue"] = np.log(sub["dengue_total"].clip(lower=0) + 1.0)
    return sub


# ─────────────────────────────────────────────────────────────────────────────
# 2.  EDA – GRAFICI ESPLORATIVI
# ─────────────────────────────────────────────────────────────────────────────

def plot_time_series(ts: pd.Series, dates: pd.Series,
                     title: str = "Serie Storica dei Casi di Dengue",
                     ylabel: str = "Casi di Dengue",
                     color: str = PALETTE["blue"],
                     figsize: tuple = (14, 4),
                     highlight_gaps: bool = True) -> None:
    """
    Grafico temporale della serie con trend OLS sovrapposto.
    Le lacune nella serie vengono evidenziate come bande verticali grigie.
    """
    fig, ax = plt.subplots(figsize=figsize)
    ax.plot(dates, ts, color=color, linewidth=0.9, alpha=0.85, zorder=3)

    # Trend lineare
    t = np.arange(len(ts), dtype=float)
    mask = ~np.isnan(ts.values) if hasattr(ts, "values") else np.ones(len(ts), dtype=bool)
    if mask.sum() > 2:
        coef = np.polyfit(t[mask], np.asarray(ts)[mask], 1)
        ax.plot(dates, np.polyval(coef, t),
                color=PALETTE["red"], linewidth=1.5, linestyle="--",
                label=f"Trend OLS (β₁ = {coef[0]:.3f}/sett.)", zorder=4)

    # Eventuali lacune (bande verticali)
    if highlight_gaps and hasattr(dates, "diff"):
        dt = dates.diff().dt.days
        gap_starts = dates[dt > 10]
        for gs in gap_starts:
            prev = dates[dates < gs].iloc[-1] if (dates < gs).any() else gs
            ax.axvspan(prev, gs, alpha=0.12, color=PALETTE["orange"], zorder=1)

    ax.set_title(title, fontweight="bold")
    ax.set_xlabel("Data")
    ax.set_ylabel(ylabel)
    ax.legend()
    plt.tight_layout()
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


def plot_distribution_transform(ts_raw: pd.Series,
                                 ts_log: pd.Series,
                                 figsize: tuple = (12, 4)) -> None:
    """
    Pannello 2×2: istogramma + QQ plot per la serie originale e
    per la trasformazione logaritmica, per motivare la trasformazione.
    """
    fig, axes = plt.subplots(1, 4, figsize=figsize)

    for col, ts, label in [
        (0, ts_raw, "Dengue (scala originale)"),
        (2, ts_log, "log(Dengue + 1)"),
    ]:
        ts_clean = ts.dropna()

        # Istogramma
        axes[col].hist(ts_clean, bins=35, color=PALETTE["blue"],
                       density=True, alpha=0.75, edgecolor="white")
        mu, sigma = ts_clean.mean(), ts_clean.std()
        x = np.linspace(ts_clean.min(), ts_clean.max(), 300)
        axes[col].plot(x, norm.pdf(x, mu, sigma),
                       color=PALETTE["red"], linewidth=2, label="N(μ,σ²)")
        axes[col].set_title(f"Distribuzione\n{label}", fontsize=10)
        axes[col].set_xlabel(label, fontsize=9)
        axes[col].set_ylabel("Densità" if col == 0 else "")
        axes[col].legend(fontsize=8)

        # Q-Q plot
        (osm, osr), (slope, intercept, _) = probplot(ts_clean, dist="norm")
        axes[col+1].scatter(osm, osr, s=8, alpha=0.5, color=PALETTE["blue"])
        lims = [min(osm.min(), osr.min()), max(osm.max(), osr.max())]
        axes[col+1].plot(lims, [slope*l + intercept for l in lims],
                         color=PALETTE["red"], linewidth=1.8)
        sk = stats.skew(ts_clean)
        ku = stats.kurtosis(ts_clean)
        axes[col+1].set_title(
            f"Q-Q Plot\nskew={sk:.2f}, kurt={ku:.2f}", fontsize=10)
        axes[col+1].set_xlabel("Quantili teorici N(0,1)", fontsize=9)
        axes[col+1].set_ylabel("Quantili campionari" if col == 0 else "")

    fig.suptitle("Analisi della Distribuzione e Giustificazione della Trasformazione Logaritmica",
                 fontsize=13, fontweight="bold")
    plt.tight_layout()
    plt.show()


def plot_seasonal_profile(df: pd.DataFrame,
                           col: str = "log_dengue",
                           figsize: tuple = (14, 5),
                           country: str = "Paese") -> None:
    """
    Pannello affiancato:
    - Heatmap Anno × Settimana ISO (profilo stagionale multi-annuale)
    - Boxplot del profilo mediano con IQR (stagionalità intra-annuale)
    """
    df_plot = df[["Year", "week_iso", col]].dropna()

    fig, axes = plt.subplots(1, 2, figsize=figsize)

    # Heatmap
    pivot = df_plot.pivot_table(values=col, index="Year", columns="week_iso",
                                 aggfunc="mean")
    sns.heatmap(pivot, ax=axes[0], cmap="YlOrRd", linewidths=0,
                cbar_kws={"label": col, "shrink": 0.85})
    axes[0].set_title("Heatmap: Anno × Settimana ISO", fontweight="bold")
    axes[0].set_xlabel("Settimana ISO")
    axes[0].set_ylabel("Anno")

    # Profilo stagionale (mediana ± IQR)
    grp = df_plot.groupby("week_iso")[col]
    med = grp.median()
    q25 = grp.quantile(0.25)
    q75 = grp.quantile(0.75)
    idx = med.index

    axes[1].fill_between(idx, q25, q75, alpha=0.25, color=PALETTE["blue"],
                          label="IQR [25°–75°]")
    axes[1].plot(idx, med, color=PALETTE["blue"], linewidth=2.2, label="Mediana")
    axes[1].plot(idx, grp.max(), color=PALETTE["orange"], linewidth=0.9,
                  linestyle=":", alpha=0.7, label="Max")
    axes[1].set_title("Profilo Stagionale Settimanale", fontweight="bold")
    axes[1].set_xlabel("Settimana ISO")
    axes[1].set_ylabel(col)
    axes[1].legend()

    fig.suptitle(f"Stagionalità Intra-Annuale dei Casi di Dengue – {country}",
                 fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.show()


def plot_stl_decomposition(ts: pd.Series, dates: pd.Series,
                            period: int = 52,
                            figsize: tuple = (14, 10),
                            country: str = "Paese") -> None:
    """
    Decomposizione STL (Seasonal-Trend via LOESS) della serie.
    Mostra le quattro componenti: osservata, trend, stagionalità, residuo STL.
    """
    from statsmodels.tsa.seasonal import STL
    ts_filled = ts.fillna(ts.median())
    stl = STL(ts_filled, period=period, robust=True)
    result = stl.fit()

    labels = ["Osservata", "Trend", "Stagionalità", "Residuo STL"]
    components = [ts_filled, result.trend, result.seasonal, result.resid]
    colors = [PALETTE["blue"], PALETTE["red"], PALETTE["green"], PALETTE["gray"]]

    fig, axes = plt.subplots(4, 1, figsize=figsize, sharex=True)
    for ax, data, label, col in zip(axes, components, labels, colors):
        ax.plot(dates, data, color=col, linewidth=0.9)
        ax.set_ylabel(label, fontsize=10)
        if label in ("Residuo STL", "Stagionalità"):
            ax.axhline(0, color="k", linewidth=0.6, linestyle="--")

    axes[0].set_title(f"Decomposizione STL della Serie Storica Dengue ({country})",
                      fontsize=14, fontweight="bold")
    axes[-1].set_xlabel("Data")
    plt.tight_layout()
    plt.show()


def plot_acf_pacf(ts: pd.Series, lags: int = 60,
                   title: str = "",
                   figsize: tuple = (14, 5)) -> None:
    """
    Grafico ACF e PACF con bande di confidenza al 95% (±1.96/√n).
    """
    from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
    ts_clean = ts.dropna()

    fig, axes = plt.subplots(1, 2, figsize=figsize)
    plot_acf(ts_clean, lags=lags, ax=axes[0], alpha=0.05, zero=False,
             color=PALETTE["blue"],
             vlines_kwargs={"colors": PALETTE["blue"]},
             title="ACF – Autocorrelazione")
    plot_pacf(ts_clean, lags=lags, ax=axes[1], alpha=0.05, zero=False,
              method="ywm", color=PALETTE["red"],
              vlines_kwargs={"colors": PALETTE["red"]},
              title="PACF – Autocorrelazione Parziale")
    for ax in axes:
        ax.axhline(0, color="k", linewidth=0.5)
        ax.set_xlabel("Lag (settimane)")
    if title:
        fig.suptitle(title, fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.show()


# ─────────────────────────────────────────────────────────────────────────────
# 3.  TEST DI STAZIONARIETÀ
# ─────────────────────────────────────────────────────────────────────────────

def run_stationarity_tests(ts: pd.Series, name: str = "Serie") -> pd.DataFrame:
    """
    Esegue i test ADF (Augmented Dickey-Fuller) e KPSS sulla serie fornita
    e restituisce un DataFrame riassuntivo con statistica, p-value, lag ottimale
    e conclusione sul risultato del test.

    H₀ ADF  : presenza di radice unitaria (non stazionaria)
    H₀ KPSS : serie stazionaria (o trend-stazionaria)

    Parameters
    ----------
    ts : pd.Series
        Serie temporale (NaN vengono rimossi prima del test)
    name : str
        Etichetta descrittiva per la serie

    Returns
    -------
    pd.DataFrame con colonne: Test, H₀, Statistica, p-value, Lag, Conclusione
    """
    from statsmodels.tsa.stattools import adfuller, kpss
    ts_clean = ts.dropna().values

    # ADF
    adf_stat, adf_p, adf_lag, _, adf_cv, _ = adfuller(ts_clean, autolag="AIC")
    adf_concl = "Stazionaria (rifiuto H₀)" if adf_p < 0.05 else "Non stazionaria"

    # KPSS
    kpss_stat, kpss_p, kpss_lag, kpss_cv = kpss(ts_clean, regression="c", nlags="auto")
    # KPSS: H₀ = stazionaria; se p < 0.05 → rifiuto H₀ → non stazionaria
    kpss_concl = "Non stazionaria (rifiuto H₀)" if kpss_p < 0.05 else "Stazionaria"

    rows = [
        {
            "Serie":    name,
            "Test":     "ADF",
            "H₀":       "Radice unitaria (non stazionaria)",
            "Statistica": round(adf_stat, 4),
            "p-value":  round(adf_p, 4),
            "Lag":      adf_lag,
            "VC 5%":    round(adf_cv["5%"], 4),
            "Conclusione": adf_concl,
        },
        {
            "Serie":    name,
            "Test":     "KPSS",
            "H₀":       "Serie stazionaria",
            "Statistica": round(kpss_stat, 4),
            "p-value":  round(kpss_p, 4),
            "Lag":      kpss_lag,
            "VC 5%":    round(kpss_cv["5%"], 4),
            "Conclusione": kpss_concl,
        },
    ]
    return pd.DataFrame(rows)


# ─────────────────────────────────────────────────────────────────────────────
# 4.  FEATURE ENGINEERING
# ─────────────────────────────────────────────────────────────────────────────

def make_fourier_features(t_cal: np.ndarray,
                           n_harmonics: int = 4,
                           period: float = 365.25 / 7) -> pd.DataFrame:
    """
    Genera le componenti di Fourier per la stagionalità annuale.

    Per ogni k = 1, …, n_harmonics calcola:
        sin_k = sin(2πk·t_cal / T)
        cos_k = cos(2πk·t_cal / T)

    dove t_cal è l'indice temporale in settimane e T è il periodo annuale
    (default 365.25/7 ≈ 52.18 settimane).

    Parameters
    ----------
    t_cal : array-like, shape (n,)
        Indice temporale in settimane (può essere calcolato come
        (date - date_riferimento).dt.days / 7).
    n_harmonics : int
        Numero di armoniche.
    period : float
        Periodo stagionale in settimane.

    Returns
    -------
    pd.DataFrame con colonne sin_1, cos_1, …, sin_K, cos_K.
    """
    t = np.asarray(t_cal, dtype=float)
    cols = {}
    for k in range(1, n_harmonics + 1):
        cols[f"sin_{k}"] = np.sin(2 * np.pi * k * t / period)
        cols[f"cos_{k}"] = np.cos(2 * np.pi * k * t / period)
    return pd.DataFrame(cols)


def build_feature_matrix(df: pd.DataFrame,
                          n_harmonics: int = 4,
                          include_trend: bool = True,
                          t_ref: float = 0.0,
                          t_scale: float = None) -> pd.DataFrame:
    """
    Costruisce la matrice delle feature per i modelli di regressione:
    - Trend lineare normalizzato t̃ = (t_cal - t_ref) / t_scale
    - Trend quadratico t̃²
    - n_harmonics armoniche di Fourier (2·n_harmonics feature)

    I parametri di normalizzazione (t_ref, t_scale) devono essere calcolati
    esclusivamente sul training set e poi applicati a train, val e test
    per prevenire il data leakage.

    Parameters
    ----------
    df : pd.DataFrame
        Deve contenere la colonna 't_cal' (settimane dal riferimento).
    n_harmonics : int
        Numero di armoniche.
    include_trend : bool
        Se True include t̃ e t̃² come regressori trend.
    t_ref : float
        Media del t_cal del training set (per centratura).
    t_scale : float or None
        Deviazione standard del t_cal del training set.
        Se None si usa 1 (nessuna scalatura).

    Returns
    -------
    pd.DataFrame delle feature (righe allineate a df).
    """
    t_cal = df["t_cal"].values.astype(float)
    scale = t_scale if t_scale is not None and t_scale > 0 else 1.0
    t_norm = (t_cal - t_ref) / scale

    parts = {}
    if include_trend:
        parts["t_norm"]    = t_norm
        parts["t_norm_sq"] = t_norm ** 2

    fourier = make_fourier_features(t_cal, n_harmonics=n_harmonics)
    for col in fourier.columns:
        parts[col] = fourier[col].values

    return pd.DataFrame(parts, index=df.index)


# ─────────────────────────────────────────────────────────────────────────────
# 5.  CROSS-VALIDATION TEMPORALE (EXPANDING WINDOW)
# ─────────────────────────────────────────────────────────────────────────────

def sliding_window_cv(model,
                       X: np.ndarray,
                       y: np.ndarray,
                       n_splits: int = 5,
                       gap: int = 0,
                       scaler_cls=None,
                       min_train_size: int = 0) -> dict:
    """
    Cross-validation a finestra espansa (expanding window) per serie storiche.

    Rispetta la struttura temporale: il fold di validazione è sempre
    temporalmente successivo al training. Il parametro `gap` consente di
    inserire un intervallo tra train e val per simulare il ritardo nella
    disponibilità dei dati.

    Parameters
    ----------
    model : estimator sklearn con metodi fit / predict
    X : np.ndarray, shape (n, p)
    y : np.ndarray, shape (n,)
    n_splits : int
        Numero di fold.
    gap : int
        Osservazioni saltate tra fine train e inizio val.
    scaler_cls : class or None
        Se fornito (es. StandardScaler), un'istanza viene fittata sul fold
        di training e applicata al fold di validazione (prevenzione data leakage).
    min_train_size : int
        Numero minimo di osservazioni di training per utilizzare un fold.
        I fold con meno osservazioni vengono scartati. Impostare ad almeno
        2×T_seasonale per garantire l'identificabilità dei parametri stagionali
        (es. 104 per dati settimanali con T=52).

    Returns
    -------
    dict con:
        rmse_mean, rmse_std, mae_mean, mae_std, r2_mean, r2_std,
        rmse_folds, mae_folds, r2_folds  (liste per fold)
    """
    tscv = TimeSeriesSplit(n_splits=n_splits, gap=gap)
    rmse_list, mae_list, r2_list = [], [], []
    skipped = 0

    for train_idx, val_idx in tscv.split(X):
        if len(train_idx) < min_train_size:
            skipped += 1
            continue

        X_tr, X_val = X[train_idx], X[val_idx]
        y_tr, y_val = y[train_idx], y[val_idx]

        if scaler_cls is not None:
            sc = scaler_cls()
            X_tr  = sc.fit_transform(X_tr)
            X_val = sc.transform(X_val)

        model.fit(X_tr, y_tr)
        y_hat = model.predict(X_val)

        rmse_list.append(np.sqrt(mean_squared_error(y_val, y_hat)))
        mae_list.append(mean_absolute_error(y_val, y_hat))
        r2_list.append(r2_score(y_val, y_hat))

    if skipped > 0:
        print(f"  [CV] {skipped} fold/s scartati (train_size < {min_train_size}); "
              f"fold validi: {len(rmse_list)}/{n_splits}")

    return {
        "rmse_mean":   np.mean(rmse_list), "rmse_std":  np.std(rmse_list),
        "mae_mean":    np.mean(mae_list),  "mae_std":   np.std(mae_list),
        "r2_mean":     np.mean(r2_list),   "r2_std":    np.std(r2_list),
        "rmse_folds":  rmse_list,
        "mae_folds":   mae_list,
        "r2_folds":    r2_list,
    }

def arima_nested_walk_forward_gap(
    method,
    y_train: np.ndarray,
    y_test: np.ndarray,
    dates_test: pd.Series,
    arima_grid: list,
    n_inner: int = 3,
    min_inner_train: int = 52,
    gap_weeks: int = 52,
    weeks_per_outer: int = 52,
    n_init: int = 4,
    verbose: bool = True,
) -> dict:
    from sklearn.model_selection import TimeSeriesSplit

    # ── Utility: costruisce kwargs per SARIMAX in base al tipo di ordine ──────
    def _build_kwargs(order_entry):
        """
        Accetta sia (p,d,q) che ((p,d,q),(P,D,Q,m)) e restituisce
        i kwargs corretti per SARIMAX.
        """
        if (
            isinstance(order_entry, (list, tuple))
            and len(order_entry) == 2
            and isinstance(order_entry[0], (list, tuple))
            and isinstance(order_entry[1], (list, tuple))
        ):
            return {"order": order_entry[0], "seasonal_order": order_entry[1]}
        else:
            return {"order": order_entry}

    def _order_label(order_entry):
        """Stringa leggibile per il verbose."""
        if isinstance(order_entry[0], (list, tuple)):
            return f"ARIMA{order_entry[0]}x{order_entry[1]}"
        return f"ARIMA{order_entry}"

    # ── 1. INNER CV su y_train: selezione ordine ─────────────────────────────
    if verbose:
        print("=" * 70)
        print("  INNER CV — selezione ordine su y_train")
        print(f"  Grid: {len(arima_grid)} ordini  |  Inner folds: {n_inner}")
        print("=" * 70)

    inner_cv     = TimeSeriesSplit(n_splits=n_inner)
    best_order   = None
    best_rmse_in = np.inf
    order_rmses  = []

    for order_entry in arima_grid:
        kwargs     = _build_kwargs(order_entry)
        fold_rmses = []
        skip_order = False

        for in_tr_idx, in_val_idx in inner_cv.split(y_train):
            if len(in_tr_idx) < min_inner_train:
                skip_order = True
                break

            y_in_tr  = y_train[in_tr_idx]
            y_in_val = y_train[in_val_idx]

            try:
                mod    = method(y_in_tr, trend="n",
                                enforce_stationarity=True,
                                enforce_invertibility=True,
                                **kwargs)
                fit_in = mod.fit(disp=False, method="lbfgs", maxiter=200)
                preds  = np.asarray(fit_in.forecast(steps=len(y_in_val)))
                fold_rmses.append(
                    float(np.sqrt(mean_squared_error(y_in_val, preds)))
                )
            except Exception:
                fold_rmses.append(np.inf)

        if skip_order or not fold_rmses:
            continue

        mean_rmse_in = float(np.mean(fold_rmses))
        order_rmses.append({"order": order_entry, "inner_rmse": mean_rmse_in})

        if verbose:
            print(f"  {_order_label(order_entry)}  Inner-RMSE={mean_rmse_in:.4f}")

        if mean_rmse_in < best_rmse_in:
            best_rmse_in = mean_rmse_in
            best_order   = order_entry

    if verbose:
        print(f"\n  → Best order: {_order_label(best_order)}"
              f"  (Inner-RMSE={best_rmse_in:.4f})\n")

    # ── 2. OUTER walk-forward annuale su y_test ───────────────────────────────
    if verbose:
        print("=" * 70)
        print("  OUTER Walk-Forward — forecast annuale su y_test")
        print(f"  Condizioni iniziali: {n_init} settimane per anno")
        print("=" * 70)

    best_kwargs   = _build_kwargs(best_order)
    n_years       = len(y_test) // weeks_per_outer
    outer_results = []

    for fold in range(n_years):
        year_start = fold * weeks_per_outer
        year_end   = year_start + weeks_per_outer

        y_year       = y_test[year_start:year_end]
        y_init       = y_year[:n_init]
        y_target     = y_year[n_init:]
        dates_target = dates_test.iloc[year_start + n_init: year_end]
        y_test_seen  = y_test[:year_start]

        y_context = np.concatenate([
            y_train,
            np.full(gap_weeks, np.nan),
            y_test_seen,
            y_init,
        ])

        try:
            mod_final = method(y_train, trend="n",
                               enforce_stationarity=True,
                               enforce_invertibility=True,
                               **best_kwargs)
            fit_final = mod_final.fit(disp=False, method="lbfgs", maxiter=300)
            fit_ctx   = fit_final.apply(y_context)
            preds     = np.asarray(fit_ctx.forecast(steps=len(y_target)))
            rmse      = float(np.sqrt(mean_squared_error(y_target, preds)))
            mae       = float(mean_absolute_error(y_target, preds))

        except Exception as exc:
            if verbose:
                print(f"  [Outer fold {fold+1}] Errore: {exc}")
            preds = np.full(len(y_target), np.nan)
            rmse  = np.nan
            mae   = np.nan

        outer_results.append({
            "fold":         fold + 1,
            "year":         2021 + fold,
            "n_init":       n_init,
            "n_forecast":   len(y_target),
            "rmse":         rmse,
            "mae":          mae,
            "y_target":     y_target,
            "preds":        preds,
            "dates_target": dates_target.values,
        })

        if verbose:
            print(
                f"  [Outer fold {fold+1} — {2021+fold}]  "
                f"Contesto={len(y_context)} sett.  "
                f"Init={n_init}  Forecast={len(y_target)} sett.  "
                f"RMSE={rmse:.4f}  MAE={mae:.4f}"
            )

    # ── 3. Metriche aggregate ─────────────────────────────────────────────────
    rmse_list = [r["rmse"] for r in outer_results]
    mae_list  = [r["mae"]  for r in outer_results]

    if verbose:
        print(f"\n  RMSE medio: {np.nanmean(rmse_list):.4f} "
              f"± {np.nanstd(rmse_list):.4f}")

    return {
        "best_order":      best_order,           # (p,d,q) o ((p,d,q),(P,D,Q,m))
        "best_order_label": _order_label(best_order),
        "best_inner_rmse": best_rmse_in,
        "order_rmses":     sorted(order_rmses, key=lambda x: x["inner_rmse"]),
        "outer_results":   outer_results,
        "cv_rmse_mean":    float(np.nanmean(rmse_list)),
        "cv_mae_mean":     float(np.nanmean(mae_list)),
        "cv_rmse_std":     float(np.nanstd(rmse_list)),
        "cv_mae_std":      float(np.nanstd(mae_list)),
    }


def plot_cv_results(cv_results: dict, model_names: list,
                    figsize: tuple = (13, 4)) -> None:
    """
    Visualizza i risultati CV (RMSE, MAE, R²) per ogni modello come
    boxplot sovrapposti ai singoli fold (strip plot), utile per valutare
    sia le performance medie sia la variabilità tra fold.
    """
    metrics = ["rmse", "mae", "r2"]
    ylabels = ["RMSE (spazio log)", "MAE (spazio log)", "R²"]
    colors = list(PALETTE.values())

    fig, axes = plt.subplots(1, 3, figsize=figsize)
    for mi, (met, ylabel) in enumerate(zip(metrics, ylabels)):
        ax = axes[mi]
        all_vals = [cv_results[name][f"{met}_folds"] for name in model_names]
        bp = ax.boxplot(all_vals, patch_artist=True, widths=0.5,
                        medianprops={"color": "k", "linewidth": 2})
        for patch, col in zip(bp["boxes"], colors):
            patch.set_facecolor(col)
            patch.set_alpha(0.6)
        for xi, vals in enumerate(all_vals, 1):
            ax.scatter([xi]*len(vals), vals, color="k", s=18, zorder=5,
                       alpha=0.7)
        ax.set_xticks(range(1, len(model_names) + 1))
        ax.set_xticklabels(model_names, rotation=25, ha="right", fontsize=9)
        ax.set_title(ylabel, fontweight="bold")
        ax.set_ylabel(ylabel)
    fig.suptitle("Confronto CV – Expanding Window (5 Fold)", fontsize=13,
                 fontweight="bold")
    plt.tight_layout()
    plt.show()


def plot_arima_nested_cv_results(results, top_k=8):
    """
    Visualizza:
    1. RMSE outer CV per anno
    2. Classifica degli ordini ARIMA dalla inner CV

    Parameters
    ----------
    results : dict
        Dizionario contenente:
        - outer_results
        - best_order
        - order_rmses

    top_k : int, default=8
        Numero di ordini ARIMA da mostrare nella classifica.
    """

    fig, axes = plt.subplots(1, 2, figsize=(13, 4))

    # ─────────────────────────────────────────────────────────────
    # (a) RMSE outer per anno
    # ─────────────────────────────────────────────────────────────
    folds = [r["fold"] for r in results["outer_results"]]
    years = [r["year"] for r in results["outer_results"]]
    rmses = [r["rmse"] for r in results["outer_results"]]

    colors = [PALETTE["blue"]] * len(folds)

    mean_rmse = np.nanmean(rmses)

    axes[0].bar(
        years,
        rmses,
        color=colors,
        alpha=0.8,
        edgecolor="white"
    )

    axes[0].axhline(
        mean_rmse,
        color=PALETTE["red"],
        linewidth=1.8,
        linestyle="--",
        label=f"Media = {mean_rmse:.4f}"
    )

    axes[0].set_xticks(years)
    axes[0].set_xlabel("Anno")
    axes[0].set_ylabel("RMSE (spazio log)")

    axes[0].set_title(
        f"RMSE Outer per Anno\n"
        f"ARIMA{results['best_order']} selezionato da Inner CV",
        fontweight="bold"
    )

    axes[0].legend()

    # ─────────────────────────────────────────────────────────────
    # (b) Classifica ordini inner CV
    # ─────────────────────────────────────────────────────────────
    top_orders = results["order_rmses"][:top_k]

    order_labels = [
        f"ARIMA{e['order']}"
        for e in top_orders
    ]

    order_vals = [
        e["inner_rmse"]
        for e in top_orders
    ]

    bar_colors = [
        PALETTE["red"]
        if e["order"] == results["best_order"]
        else PALETTE["blue"]
        for e in top_orders
    ]

    axes[1].barh(
        range(len(top_orders)),
        order_vals,
        color=bar_colors,
        alpha=0.8,
        edgecolor="white"
    )

    axes[1].set_yticks(range(len(top_orders)))
    axes[1].set_yticklabels(order_labels, fontsize=9)

    axes[1].invert_yaxis()

    axes[1].set_xlabel("Inner RMSE (spazio log)")

    axes[1].set_title(
        "Classifica Ordini – Inner CV\n"
        "(rosso = ordine scelto)",
        fontweight="bold"
    )
    fig.suptitle(
        "Nested Walk-Forward CV – ARIMA",
        fontsize=13,
        fontweight="bold"
    )

    plt.tight_layout()
    plt.show()

import pandas as pd
import matplotlib.pyplot as plt

def plot_arima_outer_predictions(results, df_train, y_train):
    """
    Visualizza le previsioni degli outer fold
    confrontate con i valori osservati.

    Parameters
    ----------
    results : dict
        Dizionario contenente:
        - outer_results
        - best_order

    df_train : pd.DataFrame
        DataFrame del training set.
        Deve contenere la colonna 'date'.

    y_train : array-like
        Serie target del training storico.
    """

    _, ax = plt.subplots(figsize=(14, 5))

    ax.plot(
        df_train["date"],
        y_train,
        color=PALETTE["gray"],
        linewidth=0.8,
        alpha=0.5,
        label="Training storico (2010-2019)"
    )

    ax.axvspan(
        pd.Timestamp("2020-01-01"),
        pd.Timestamp("2020-12-31"),
        alpha=0.1,
        color=PALETTE["orange"],
        label="2020 (escluso)"
    )

    colors_fold = list(PALETTE.values())

    for i, r in enumerate(results["outer_results"]):

        te_dates = pd.to_datetime(r["dates_target"])

        # Osservato
        ax.plot(
            te_dates,
            r["y_target"],
            color="k",
            linewidth=1.4,
            alpha=0.4,
            label="Osservato" if i == 0 else None
        )

        # Predizione
        ax.plot(
            te_dates,
            r["preds"],
            color=colors_fold[i % len(colors_fold)],
            linewidth=1.5,
            linestyle="--",
            label=(
                f"{r['year']} – "
                f"ARIMA{results['best_order']} "
                f"(RMSE={r['rmse']:.3f}, "
                f"init={r['n_init']} sett.)"
            )
        )

    ax.set_title(
        f"Outer Walk-Forward – Previsioni vs Osservato\n"
        f"Ordine ARIMA{results['best_order']} "
        f"selezionato da Inner CV",
        fontweight="bold"
    )

    ax.set_xlabel("Data")
    ax.set_ylabel("log(Casi + 1)")

    ax.legend(
        fontsize=8,
        loc="upper left"
    )

    plt.tight_layout()
    plt.show()


# ─────────────────────────────────────────────────────────────────────────────
# 6.  METRICHE DI VALUTAZIONE PREDITTIVA
# ─────────────────────────────────────────────────────────────────────────────

def compute_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> dict:
    """
    Calcola il pannello standard di metriche predittive.

    Bias  = Ê[ŷ − y]   (errore sistematico)
    RMSE  = √(MSE)
    RRMSE = RMSE / ȳ    (adimensionale)
    MAE   = Ê[|ŷ − y|]
    R²    = 1 − SS_res / SS_tot

    Returns
    -------
    dict con chiavi: Bias, RMSE, RRMSE, MAE, R²
    """
    residuals = np.asarray(y_pred) - np.asarray(y_true)
    bias  = float(np.mean(residuals))
    rmse  = float(np.sqrt(np.mean(residuals ** 2)))
    mae   = float(np.mean(np.abs(residuals)))
    y_bar = float(np.mean(np.abs(y_true)))
    rrmse = rmse / y_bar if y_bar > 0 else np.nan
    r2    = float(r2_score(y_true, y_pred))
    return {"Bias": bias, "RMSE": rmse, "RRMSE": rrmse, "MAE": mae, "R²": r2}


def persistence_predictions(y_all: np.ndarray, n_test: int) -> np.ndarray:
    """
    Modello di riferimento naïve (Random Walk, persistenza 1 passo):
        ŷ_{t+1} = y_t

    Per il test set di lunghezza n_test si usano le osservazioni
    immediatamente precedenti del training set + test set stesso.

    Parameters
    ----------
    y_all : np.ndarray
        Array con training + test concatenati (ordinati temporalmente).
    n_test : int
        Numero di osservazioni del test set (ultime n_test di y_all).

    Returns
    -------
    np.ndarray con le previsioni di persistenza per il test set.
    """
    n_train = len(y_all) - n_test
    return y_all[n_train - 1 : n_train - 1 + n_test]


# ─────────────────────────────────────────────────────────────────────────────
# 7.  DIAGNOSTICA DEI RESIDUI
# ─────────────────────────────────────────────────────────────────────────────

def plot_residual_diagnostics(residuals: np.ndarray,
                               dates=None,
                               lags: int = 40,
                               model_name: str = "Modello",
                               figsize: tuple = (14, 10)) -> dict:
    """
    Pannello completo di diagnostica dei residui (4 grafici):
      (a) Serie temporale dei residui con banda ±2σ
      (b) Istogramma + curva normale teorica
      (c) ACF dei residui (test visivo di white noise)
      (d) Normal probability plot (Q-Q)

    Esegue e restituisce i risultati dei test:
      - Ljung-Box (autocorrelazione a lag 6, 12, 24)
      - Jarque-Bera (normalità)
      - Shapiro-Wilk (normalità, su campione ≤ 5000 osservazioni)

    Parameters
    ----------
    residuals : array-like
    dates : array-like or None
    lags : int – lag massimo per ACF
    model_name : str – etichetta del modello

    Returns
    -------
    dict con chiavi: ljung_box, jarque_bera, shapiro_wilk,
                     skewness, excess_kurtosis, mean_residual, std_residual
    """
    from statsmodels.stats.diagnostic import acorr_ljungbox
    from statsmodels.graphics.tsaplots import plot_acf as _plot_acf

    res = np.asarray(residuals).flatten()
    n   = len(res)
    mu  = res.mean()
    sig = res.std()

    fig = plt.figure(figsize=figsize)
    gs  = gridspec.GridSpec(2, 2, hspace=0.40, wspace=0.35)
    ax_ts = fig.add_subplot(gs[0, :])
    ax_ac = fig.add_subplot(gs[1, 0])
    ax_qq = fig.add_subplot(gs[1, 1])

    # (a) Serie residui
    xax = dates if dates is not None else np.arange(n)
    ax_ts.plot(xax, res, color=PALETTE["gray"], linewidth=0.75, alpha=0.85)
    ax_ts.axhline(0,       color="k",          linewidth=1.0, linestyle="--")
    ax_ts.axhline(+2*sig,  color=PALETTE["red"], linewidth=0.8, linestyle=":", label="±2σ")
    ax_ts.axhline(-2*sig,  color=PALETTE["red"], linewidth=0.8, linestyle=":")
    ax_ts.set_title(f"Residui – {model_name}")
    ax_ts.set_xlabel("Tempo")
    ax_ts.set_ylabel("Residuo")
    ax_ts.legend()

    # Istogramma in un inset
    ax_in = ax_ts.inset_axes([0.76, 0.08, 0.22, 0.78])
    ax_in.hist(res, bins=28, density=True, color=PALETTE["blue"],
               alpha=0.65, edgecolor="white")
    xg = np.linspace(res.min(), res.max(), 200)
    ax_in.plot(xg, norm.pdf(xg, mu, sig), color=PALETTE["red"], linewidth=1.5)
    ax_in.set_title("Distribuz.", fontsize=8)
    ax_in.tick_params(labelsize=7)

    # (b) ACF
    _plot_acf(res, lags=lags, ax=ax_ac, alpha=0.05, zero=False,
              color=PALETTE["blue"],
              vlines_kwargs={"colors": PALETTE["blue"]},
              title="ACF dei Residui")
    ax_ac.axhline(0, color="k", linewidth=0.5)

    # (c) Q-Q
    (osm, osr), (slope, intercept, _) = probplot(res, dist="norm")
    ax_qq.scatter(osm, osr, s=8, alpha=0.5, color=PALETTE["blue"])
    lims = [min(osm.min(), osr.min()), max(osm.max(), osr.max())]
    ax_qq.plot(lims, [slope*l + intercept for l in lims],
               color=PALETTE["red"], linewidth=1.8)
    ax_qq.set_title("Q-Q Plot (Normal Probability Plot)")
    ax_qq.set_xlabel("Quantili teorici N(0,1)")
    ax_qq.set_ylabel("Quantili campionari")

    fig.suptitle(f"Diagnostica dei Residui – {model_name}",
                 fontsize=14, fontweight="bold", y=1.01)
    plt.tight_layout()
    plt.show()

    # Test statistici
    lb = acorr_ljungbox(res, lags=[6, 12, 24], return_df=True)
    jb_stat, jb_p = stats.jarque_bera(res)
    sw_stat, sw_p = stats.shapiro(res[:min(5000, n)])

    return {
        "ljung_box":       lb,
        "jarque_bera":     {"statistic": jb_stat, "p_value": jb_p},
        "shapiro_wilk":    {"statistic": sw_stat,  "p_value": sw_p},
        "skewness":        float(stats.skew(res)),
        "excess_kurtosis": float(stats.kurtosis(res)),
        "mean_residual":   float(mu),
        "std_residual":    float(sig),
    }


def print_diagnostics_summary(diagnostics: dict,
                                model_name: str = "") -> None:
    """
    Stampa in console la tabella riassuntiva dei test statistici sui residui.
    """
    sep = "=" * 60
    print(f"\n{sep}")
    print(f"  DIAGNOSTICA RESIDUI – {model_name}")
    print(sep)
    print(f"  Residuo medio    : {diagnostics['mean_residual']:+.5f}  (≈ 0 desiderabile)")
    print(f"  Std dei residui  : {diagnostics['std_residual']:.5f}")
    print(f"  Skewness         : {diagnostics['skewness']:+.4f}  (|s|<1 accettabile)")
    print(f"  Kurtosi eccesso  : {diagnostics['excess_kurtosis']:+.4f}  (≈0 per normale)")
    print()
    print("  Test Ljung-Box  (H₀: i residui non sono autocorrelati)")
    lb = diagnostics["ljung_box"]
    for _, row in lb.iterrows():
        lag = int(row.name)
        pv  = row["lb_pvalue"]
        verdict = "✗  rifiuto H₀" if pv < 0.05 else "✓  non rifiuto H₀"
        print(f"    lag={lag:2d}:  Q = {row['lb_stat']:8.3f},  p = {pv:.4f}  →  {verdict}")
    print()
    jb = diagnostics["jarque_bera"]
    sig_jb = "✗  rifiuto H₀" if jb["p_value"] < 0.05 else "✓  non rifiuto H₀"
    print(f"  Test Jarque-Bera  (H₀: normalità):  "
          f"JB = {jb['statistic']:.3f},  p = {jb['p_value']:.4f}  →  {sig_jb}")
    sw = diagnostics["shapiro_wilk"]
    sig_sw = "✗  rifiuto H₀" if sw["p_value"] < 0.05 else "✓  non rifiuto H₀"
    print(f"  Test Shapiro-Wilk (H₀: normalità):  "
          f"W  = {sw['statistic']:.4f},  p = {sw['p_value']:.4f}  →  {sig_sw}")
    print(sep + "\n")


# ─────────────────────────────────────────────────────────────────────────────
# 8.  VISUALIZZAZIONI FINALI
# ─────────────────────────────────────────────────────────────────────────────

def plot_forecast(train_dates, train_y,
                  test_dates, test_y,
                  forecasts: dict,
                  log_scale: bool = True,
                  figsize: tuple = (14, 5)) -> None:
    """
    Sovrappone le previsioni di più modelli ai dati osservati.

    Parameters
    ----------
    train_dates, train_y : training set (per contesto storico)
    test_dates, test_y   : test set osservato
    forecasts : dict {nome_modello: array_previsioni}
    log_scale : se True l'asse Y è in scala log(dengue+1)
    """
    colors = list(PALETTE.values())
    fig, ax = plt.subplots(figsize=figsize)

    ax.plot(train_dates, train_y, color=PALETTE["gray"], linewidth=0.7,
            alpha=0.55, label="Training (osservato)")
    ax.plot(test_dates, test_y, color="k", linewidth=1.8,
            alpha=0.9, label="Test (osservato)")

    ax.axvline(x=test_dates.iloc[0] if hasattr(test_dates, "iloc") else test_dates[0],
               color="k", linewidth=1, linestyle=":", alpha=0.6)

    for i, (name, y_hat) in enumerate(forecasts.items()):
        ax.plot(test_dates, y_hat, color=colors[i % len(colors)],
                linewidth=1.7, linestyle="--", alpha=0.85, label=name)

    ax.set_title("Previsioni sul Test Set – Confronto dei Modelli",
                 fontweight="bold")
    ax.set_xlabel("Data")
    ax.set_ylabel("log(Casi + 1)" if log_scale else "Casi di Dengue")
    ax.legend(fontsize=9)
    plt.tight_layout()
    plt.show()


def plot_metrics_comparison(metrics_dict: dict,
                             figsize: tuple = (13, 4)) -> pd.DataFrame:
    """
    Crea un pannello di bar chart per ogni metrica (RMSE, MAE, RRMSE, R²)
    confrontando tutti i modelli, e restituisce la tabella riassuntiva.

    Parameters
    ----------
    metrics_dict : dict {nome_modello: {Bias, RMSE, RRMSE, MAE, R²}}

    Returns
    -------
    pd.DataFrame con modelli come righe e metriche come colonne.
    """
    metric_names = ["RMSE", "MAE", "RRMSE", "R²"]
    model_names  = list(metrics_dict.keys())
    colors       = list(PALETTE.values())

    fig, axes = plt.subplots(1, 4, figsize=figsize)
    for mi, mname in enumerate(metric_names):
        ax   = axes[mi]
        vals = [metrics_dict[m].get(mname, np.nan) for m in model_names]
        bars = ax.bar(model_names, vals,
                      color=colors[: len(model_names)],
                      alpha=0.80, edgecolor="white", linewidth=0.8)
        ax.set_title(mname, fontweight="bold")
        ax.set_xticklabels(model_names, rotation=30, ha="right", fontsize=8)
        for bar, val in zip(bars, vals):
            if not np.isnan(val):
                ax.text(bar.get_x() + bar.get_width() / 2,
                        bar.get_height() * 1.01,
                        f"{val:.3f}", ha="center", va="bottom", fontsize=8)

    fig.suptitle("Performance sul Test Set – Confronto dei Modelli",
                 fontsize=13, fontweight="bold")
    plt.tight_layout()
    plt.show()

    df_metrics = pd.DataFrame(
        {m: [metrics_dict[n].get(m, np.nan) for n in model_names]
         for m in ["Bias", "RMSE", "RRMSE", "MAE", "R²"]},
        index=model_names,
    ).round(4)
    return df_metrics


def print_model_summary_table(cv_dict: dict, test_metrics_dict: dict) -> None:
    """
    Stampa in console una tabella a doppia colonna con CV-RMSE e test metrics
    per tutti i modelli.
    """
    header = f"{'Modello':<22} {'CV-RMSE (mean±std)':<24} {'Test RMSE':<12} {'Test R²':<10} {'Test MAE':<10}"
    print("\n" + "=" * len(header))
    print("  RIEPILOGO PERFORMANCE MODELLI")
    print("=" * len(header))
    print(header)
    print("-" * len(header))
    for name in cv_dict:
        cv  = cv_dict[name]
        tst = test_metrics_dict.get(name, {})
        print(
            f"{name:<22} "
            f"{cv['rmse_mean']:.4f} ± {cv['rmse_std']:.4f}     "
            f"{tst.get('RMSE', float('nan')):<12.4f} "
            f"{tst.get('R²',   float('nan')):<10.4f} "
            f"{tst.get('MAE',  float('nan')):<10.4f}"
        )
    print("=" * len(header) + "\n")
