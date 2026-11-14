"""Medidas de error entre una serie real y una pronosticada."""

import numpy as np
import pandas as pd


def medidas_error(real, pronostico, nombre="modelo"):
    """ME, RMSE, MAE, MPE y MAPE entre dos series alineadas por índice."""
    real = pd.Series(real).astype(float)
    pronostico = pd.Series(pronostico).astype(float).reindex(real.index)
    error = real - pronostico
    porcentual = error / real.replace(0, np.nan)
    return pd.Series(
        {
            "ME": error.mean(),
            "RMSE": np.sqrt((error ** 2).mean()),
            "MAE": error.abs().mean(),
            "MPE": (porcentual * 100).mean(),
            "MAPE": (porcentual.abs() * 100).mean(),
        },
        name=nombre,
    )


def imprimir_medidas(real, pronostico, nombre="modelo"):
    """Formato parecido al del enunciado."""
    m = medidas_error(real, pronostico, nombre)
    print(f"{nombre}")
    print(f"{'Mean Error (ME) :':>42} {m['ME']:.4f}")
    print(f"{'Root Mean Squared Error (RMSE) :':>42} {m['RMSE']:.4f}")
    print(f"{'Mean Absolute Error (MAE) :':>42} {m['MAE']:.4f}")
    print(f"{'Mean Percentage Error (MPE) :':>42} {m['MPE']:.4f}")
    print(f"{'Mean Absolute Percentage Error (MAPE) :':>42} {m['MAPE']:.4f}")
    return m


def tabla_comparativa(resultados):
    """resultados: dict {nombre: (real, pronostico)} -> DataFrame de métricas."""
    return pd.DataFrame(
        [medidas_error(real, pred, nombre) for nombre, (real, pred) in resultados.items()]
    )
