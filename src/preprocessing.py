"""Funciones de preparación de la serie Tasa Interbancaria Mensual (TIB)."""

from pathlib import Path

import pandas as pd

SHEET = "Series de datos"
HEADER_ROWS = 5  # las primeras filas del archivo de BanRep son encabezados/metadatos


def cargar_tib(ruta_xlsx, inicio="2000-01-01", fin=None):
    """Lee el archivo original de BanRep y devuelve un DataFrame limpio.

    Parameters
    ----------
    ruta_xlsx : str | Path
        Archivo descargado del Portal de Estadísticas Económicas.
    inicio, fin : str | None
        Recorte del periodo de estudio (inclusive).
    """
    crudo = pd.read_excel(
        ruta_xlsx, sheet_name=SHEET, header=None, skiprows=HEADER_ROWS,
        names=["fecha", "tib"],
    )
    fechas = pd.to_datetime(crudo["fecha"], errors="coerce")
    df = crudo.loc[fechas.notna()].copy()
    df["fecha"] = fechas.loc[fechas.notna()]
    # BanRep marca los faltantes con un punto: to_numeric los vuelve NaN
    df["tib"] = pd.to_numeric(df["tib"], errors="coerce")
    df = df.sort_values("fecha").reset_index(drop=True)
    if inicio is not None:
        df = df.loc[df["fecha"] >= pd.Timestamp(inicio)]
    if fin is not None:
        df = df.loc[df["fecha"] <= pd.Timestamp(fin)]
    return df.reset_index(drop=True)


def a_serie(df, columna="tib", freq="MS"):
    """Convierte el DataFrame limpio en una Series con índice temporal regular."""
    serie = pd.Series(df[columna].to_numpy(), index=pd.DatetimeIndex(df["fecha"]), name=columna)
    # las fechas de BanRep son fin de mes; se normalizan a inicio de mes para tener freq fija
    serie.index = serie.index.to_period("M").to_timestamp(how="start")
    serie = serie.asfreq(freq)
    return serie.interpolate(method="time") if serie.isna().any() else serie


def guardar_procesado(serie, ruta_csv):
    """Guarda la versión modificada (fecha, valor) usada por el notebook."""
    ruta = Path(ruta_csv)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    serie.rename("tib").to_frame().rename_axis("fecha").to_csv(ruta)
    return ruta


def tabla_estacional(serie):
    """Matriz año x mes, útil para comparar estacionalidad entre años."""
    df = serie.to_frame("valor")
    df["anio"] = df.index.year
    df["mes"] = df.index.month
    return df.pivot_table(index="mes", columns="anio", values="valor")
