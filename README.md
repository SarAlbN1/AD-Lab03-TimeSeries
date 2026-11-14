# Laboratorio de análisis de series de tiempo

**Pontificia Universidad Javeriana · Analítica de Datos**

Análisis de la **Tasa Interbancaria Mensual (TIB)** de Colombia (Banco de la República, enero 2000 – octubre
2026) con técnicas de series de tiempo: tendencia, estacionalidad, descomposición y pronóstico con modelos
naïve, regresión lineal, media móvil y ARIMA. El enunciado está en [`enunciado.md`](enunciado.md).

## Estructura

```text
AD-Lab03-TimeSeries/
├── README.md
├── enunciado.md
├── requirements.txt
├── data/
│   ├── raw/File.xlsx              # descarga original de BanRep (sin modificar)
│   └── processed/tib_mensual.csv  # versión limpia usada por el notebook
├── notebooks/
│   └── laboratorio_series_tiempo.ipynb   # desarrollo completo de las 15 actividades
├── src/
│   ├── preprocessing.py           # carga, limpieza e índice temporal
│   ├── metrics.py                 # ME, RMSE, MAE, MPE, MAPE
│   └── forecasting.py             # naïve, regresión, media móvil, ARIMA
├── outputs/
│   ├── figures/                   # 11 figuras generadas por el notebook
│   └── metrics/metricas_validacion.csv
└── reporte/
    ├── laboratorio_series_tiempo.html
    └── laboratorio_series_tiempo.pdf     # notebook ejecutado, exportado a PDF
```

## Serie analizada

| | |
|---|---|
| Serie | Tasa Interbancaria Mensual (TIB) |
| Fuente | Banco de la República — Portal de Estadísticas Económicas |
| Unidad | Porcentaje (%), promedio mensual |
| Periodo | Enero 2000 – Octubre 2026 (322 observaciones, sin faltantes) |
| Partición | 286 meses de entrenamiento / 36 de validación (nov-2023 → oct-2026) |

## Resultados principales

- La TIB **no presenta estacionalidad mensual**: el perfil por mes varía ~3 % del nivel (±1.5 %) frente a un
  rango total de 1.7 % a 13.3 %. Lo confirman la superposición de años, `seasonal_decompose` y la ACF en los
  rezagos 12, 24 y 36.
- **No hay tendencia lineal** (R² = 0.00); una tendencia cuadrática captura la forma de U del periodo
  (R² = 0.43). Lo que domina es el ciclo de política monetaria.
- La **descomposición multiplicativa** es la adecuada: la dispersión del residuo aditivo crece con el nivel de
  la tasa (0.23 → 0.37 pp).
- La serie es **I(1)** (ADF: p = 0.074 en niveles, p = 0.000 en primera diferencia).
- A 36 meses ningún modelo univariado acierta. RMSE sobre validación: media móvil (12) **2.38** < naïve
  estacional 2.50 < regresión 2.91 < ARIMA(1,1,1) 3.05 ≪ ARIMA(2,0,1) elegido por AIC **6.26**.
- A **un paso adelante**, ARIMA(1,1,1) baja el MAPE a **2.04 %**: la serie es muy predecible en el corto plazo
  e impredecible a tres años.

## Reproducir

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
jupyter lab
```

Ejecutar `notebooks/laboratorio_series_tiempo.ipynb` de principio a fin (≈ 15 s). Regenera `data/processed/`,
`outputs/figures/` y `outputs/metrics/`.

Exportar el PDF sin LaTeX instalado:

```bash
jupyter nbconvert --to html --embed-images --output-dir reporte \
  notebooks/laboratorio_series_tiempo.ipynb
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu \
  --no-pdf-header-footer --print-to-pdf="reporte/laboratorio_series_tiempo.pdf" \
  "file://$PWD/reporte/laboratorio_series_tiempo.html"
```

## Entregables

1. `notebooks/laboratorio_series_tiempo.ipynb` — código y respuestas de las 15 actividades.
2. `data/raw/File.xlsx` — archivo original.
3. `data/processed/tib_mensual.csv` — archivo modificado.
