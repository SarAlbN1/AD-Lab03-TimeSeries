"""Modelos de pronóstico usados en el laboratorio."""

import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.tsa.arima.model import ARIMA


def particion(serie, n_validacion=36):
    """Divide la serie en entrenamiento y validación por un punto de corte temporal."""
    return serie.iloc[:-n_validacion], serie.iloc[-n_validacion:]


def naive_estacional(entrenamiento, indice_validacion, periodo=12):
    """Repite el último ciclo estacional observado sobre el horizonte de validación."""
    ultimo_ciclo = entrenamiento.iloc[-periodo:].to_numpy()
    valores = np.resize(ultimo_ciclo, len(indice_validacion))
    return pd.Series(valores, index=indice_validacion, name="naive_estacional")


def naive_simple(entrenamiento, indice_validacion):
    """Mantiene constante el último valor observado."""
    return pd.Series(
        entrenamiento.iloc[-1], index=indice_validacion, name="naive_simple", dtype=float
    )


def _matriz_diseno(indice, origen, periodo=12, cuadratica=True):
    trend = np.arange(len(indice)) + (indice[0].to_period("M") - origen.to_period("M")).n + 1
    X = pd.DataFrame({"trend": trend.astype(float)}, index=indice)
    if cuadratica:
        X["trend_squared"] = X["trend"] ** 2
    estacional = pd.get_dummies(indice.month, prefix="mes", drop_first=True).astype(float)
    estacional.index = indice
    return pd.concat([X, estacional], axis=1)


def regresion_tendencia_estacionalidad(entrenamiento, indice_validacion, periodo=12, cuadratica=True):
    """OLS con tendencia (lineal/cuadrática) y variables dummy de mes."""
    X_tr = _matriz_diseno(entrenamiento.index, entrenamiento.index[0], periodo, cuadratica)
    modelo = sm.OLS(entrenamiento.to_numpy(), sm.add_constant(X_tr)).fit()
    X_va = _matriz_diseno(indice_validacion, entrenamiento.index[0], periodo, cuadratica)
    X_va = sm.add_constant(X_va, has_constant="add").reindex(columns=sm.add_constant(X_tr).columns, fill_value=0.0)
    pred = pd.Series(modelo.predict(X_va), index=indice_validacion, name="regresion")
    return modelo, pred


def media_movil(entrenamiento, indice_validacion, ventana=12):
    """Pronóstico plano igual al promedio móvil de las últimas `ventana` observaciones."""
    nivel = entrenamiento.rolling(ventana).mean().iloc[-1]
    return pd.Series(nivel, index=indice_validacion, name=f"media_movil_{ventana}", dtype=float)


def suavizado_ma(serie, ventana=12, centrado=True):
    """Serie suavizada por media móvil, para graficar la componente de nivel."""
    return serie.rolling(ventana, center=centrado).mean()


def ajustar_arima(entrenamiento, indice_validacion, order=(1, 1, 1), seasonal_order=(0, 0, 0, 0)):
    """Ajusta un (S)ARIMA y pronostica el horizonte de validación."""
    modelo = ARIMA(entrenamiento, order=order, seasonal_order=seasonal_order).fit()
    pred = modelo.forecast(steps=len(indice_validacion))
    pred.index = indice_validacion
    pred.name = f"ARIMA{order}x{seasonal_order}"
    return modelo, pred


def buscar_arima(entrenamiento, indice_validacion, grilla_order, grilla_seasonal=((0, 0, 0, 0),)):
    """Búsqueda por AIC sobre una grilla pequeña de órdenes."""
    filas = []
    for order in grilla_order:
        for seasonal in grilla_seasonal:
            try:
                modelo = ARIMA(entrenamiento, order=order, seasonal_order=seasonal).fit()
                filas.append({"order": order, "seasonal_order": seasonal, "aic": modelo.aic})
            except Exception as exc:  # modelos que no convergen
                filas.append({"order": order, "seasonal_order": seasonal, "aic": np.nan, "error": str(exc)})
    return pd.DataFrame(filas).sort_values("aic").reset_index(drop=True)
