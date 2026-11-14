# Laboratorio: Introducción al análisis de Series de tiempo

> **Institución:** Pontificia Universidad Javeriana  
> **Facultad:** Facultad de Ingeniería  
> **Departamento:** Departamento de Ingeniería de Sistemas  
> **Curso:** Analítica de Datos  
> **Fuente:** `lab-time_series-original.pdf` (8 páginas).  
> **Alcance de este archivo:** Transcripción organizada del enunciado, incluyendo instrucciones, preguntas, fragmentos de código, valores del ejemplo y referencias visuales. Las imágenes de cada página se conservan en `figuras-referencia/`. No se presentan soluciones ni resultados inventados.

## 1. Objetivo del laboratorio

Facilitar el análisis de series de tiempo como herramienta para modelar y explicar secuencias de datos (mediciones) con respecto al tiempo.

Usar técnicas estadísticas para analizar secuencias de datos y extraer conclusiones o interpretaciones de los resultados.

## 2. Entregables

- Este taller se desarrolla de forma individual.
- Cada estudiante seleccionará un conjunto de datos distinto del [Portal de Estadísticas Económicas del Banco de la República](https://suameca.banrep.gov.co/estadisticas-economicas/). El conjunto de datos debe ser distinto al utilizado como ejemplo de **Tasa de desempleo en Colombia - total nacional**.
- El entregable es un **Python notebook `.ipynb`** a la plataforma con su código y las respuestas del taller.
- Cargue el archivo de datos utilizado para el taller, tanto en el **formato original** como el **modificado**.

## 3. Laboratorio

Los ejemplos de este documento se basan en la secuencia de datos de la **Tasa de Desempleo en Colombia - Total Nacional** entre los años **2000 y 2025**. Este conjunto de datos se publica junto con el laboratorio con propósito demostrativo.

Adjunto al documento se menciona un documento de la **Oficina Australiana de Estadísticas**, titulado *A Guide to Interpreting Time Series*, donde se referencian las lecturas correspondientes. **Ese documento adicional no está incluido en el PDF recibido.**

### Actividad 1. Selección y descarga de datos

Seleccione y descargue un conjunto de datos del [Portal de Estadísticas Económicas del Banco de la República](https://suameca.banrep.gov.co/estadisticas-economicas/).

### Actividad 2. Carga de la serie

Cargue la secuencia de datos como una **Series de pandas**, y asigne al índice la variable tiempo.

### Actividad 3. Gráfica de la serie temporal

Grafique la serie con respecto al tiempo. Utilice las siguientes bibliotecas de Python:

```python
import pandas as pd
import matplotlib.pylab as plt
import statsmodels.formula.api as sm
from statsmodels.tsa import tsatools
```

**Resultado esperado (ejemplo del documento):** gráfica de la tasa de desempleo respecto a la fecha; consultar la página 2.

![Página 2: instrucciones y gráfica inicial de la serie](figuras-referencia/pagina-02.png)

### Actividad 4. Componentes y estacionalidad

Lea la sección **2.1** de los componentes de una serie de tiempo del documento *A Guide to Interpreting Time Series*. Grafique segmentos de la serie con el propósito de observar estacionalidades.

**Resultado esperado (ejemplo del documento):** comparación mensual de las curvas de distintos años, mostrada en la página 3.

![Página 3: comparación anual de estacionalidad y actividad 5](figuras-referencia/pagina-03.png)

### Actividad 5. `tsatools`, `add_trend` y fórmulas

Lea la documentación del uso de `tsatools`: <https://www.statsmodels.org/stable/tsa.html>, especialmente la función `add_trend`, que agrega valores de tendencia a la serie de datos.

Responda:

**a.** ¿Qué significa el parámetro `ctt`?  
**b.** ¿Cómo funciona el objeto `formula` de la función `ols`?  
**c.** ¿Cuál es el significado del operador tilde (`~`) en la fórmula?

### Actividad 6. Modelo y gráfica de tendencia

Cree un nuevo modelo a partir del **API de fórmula** y grafique la tendencia.

**Código del ejemplo proporcionado en el PDF** (el fragmento previo aparece omitido con `...`):

```python
# ... (fragmento anterior no incluido en el enunciado)
desempleo_lm = sm.ols(
    formula='tasa_desempleo_total_nacional ~ trend + trend_squared',
    data=desempleo_trend_df
).fit()

fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(10, 6))
four_years_df[['tasa_desempleo_total_nacional']].plot(ax=axes[0])
desempleo_df[['tasa_desempleo_total_nacional']].plot(ax=axes[1])
for ax in axes:
    ax.set_xlabel('Fecha')
    ax.set_ylabel('Tasa de Desempleo')
desempleo_lm.predict(desempleo_trend_df).plot(ax=axes[1])
plt.show()
```

**Resultado esperado (ejemplo del documento):** gráfica de un segmento y gráfica completa con tendencia superpuesta, visibles en página 4.

![Página 4: tendencia y actividad 7](figuras-referencia/pagina-04.png)

### Actividad 7. Cálculo de estacionalidad y descomposición

Calcule la estacionalidad. Consulte la documentación de la función **`seasonal_decompose`** y describa el comportamiento de sus datos con respecto a la estacionalidad y el tipo de descomposición aplicada (**multiplicativa y aditiva**).

**Resultado esperado (ejemplos):** descomposiciones con paneles de serie observada, tendencia, componente estacional y residuo, en las páginas 5 y 6.

![Página 5: descomposición multiplicativa y preguntas 8-10](figuras-referencia/pagina-05.png)

![Página 6: descomposición aditiva e instrucciones de partición](figuras-referencia/pagina-06.png)

### Actividad 8. Diferencia entre descomposiciones

¿Cuáles son las diferencias entre la descomposición **aditiva** y la **multiplicativa**, y cómo afecta el tipo de descomposición en la interpretación de su serie de datos?

### Actividad 9. Componentes estacionales

Explique la razón por la cual son distintos los componentes estacionales de la descomposición aditiva de la multiplicativa.

### Actividad 10. Picos, valles y residuos

¿Su serie tiene picos o valles muy prolongados como los del ejemplo? Si es así, ¿cómo se expresan estos valores atípicos en el residuo de la descomposición?

### Actividad 11. Entrenamiento, validación y pronóstico estacional naïve

Seleccione un punto en el tiempo para dividir la serie. El ejemplo mostrado tiene **288 puntos (periodos)** y se utilizaron como punto de división los **últimos 36 periodos**, es decir, **3 años**.

La predicción **Naïve** simplemente mantiene el mismo valor final para los demás puntos. Cuando hay estacionalidad, se tiene simplemente el valor del periodo anterior ajustado a la estacionalidad.

**a.** La primera serie, desde el inicio hasta el punto de corte, es utilizada para **entrenamiento**. Línea azul continua en el ejemplo.  
**b.** La serie posterior, desde el punto de corte hasta el final, se utiliza para **validación**. Línea azul punteada en el ejemplo.  
**c.** Asuma que la predicción corresponde a una **copia del último segmento estacional** (para el ejemplo, **12 periodos**). Línea naranja en el ejemplo.

> **Nota de fidelidad:** el enunciado usa la expresión «predicción Naïve» y, para el ejercicio específico, solicita copiar el último segmento estacional. No se debe sustituir esta condición por un método distinto sin justificarlo.

### Actividad 12. Gráfica de entrenamiento, validación y pronóstico

Grafique la serie de prueba, hasta el punto de corte, y luego la serie real (utilizada como validación) y la serie estimada.

**Resultado esperado (ejemplo del documento):** comparación de valores reales y predichos; consultar página 7.

![Página 7: comparación de pronósticos, errores y actividad 14](figuras-referencia/pagina-07.png)

### Actividad 13. Métricas del error

Construya una función que determine el error entre dos series y muestre:

- **ME:** Mean Error.
- **RMSE:** Root Mean Squared Error.
- **MAE:** Mean Absolute Error.
- **MPE:** Mean Percentage Error.
- **MAPE:** Mean Absolute Percentage Error.

**a.** ¿Cuáles son los valores de error entre la serie de validación (real) y la estimación simple de los valores de la última estación?  
**b.** Escriba el análisis de las medidas de error calculadas.

**Valores publicados en el PDF, solo como ejemplo de referencia** (no corresponden a los datos que el estudiante debe seleccionar):

| Métrica | Valor del ejemplo |
|---|---:|
| Mean Error (ME) | 0.0889 |
| Root Mean Squared Error (RMSE) | 1.2284 |
| Mean Absolute Error (MAE) | 0.9528 |
| Mean Percentage Error (MPE) | -0.6708 |
| Mean Absolute Percentage Error (MAPE) | 10.0333 |

El ejemplo describe una predicción Naïve con línea verde y valores reales con línea punteada.

### Actividad 14. Regresión lineal

Aplique un modelo de **regresión lineal** para capturar la **tendencia y estacionalidad**.

**a.** Describa las ventajas y limitaciones de la regresión lineal para explicar la tendencia y estacionalidad de la serie.

**Resultado esperado (ejemplo del documento):** serie y línea de tendencia ajustada; página 8.

![Página 8: regresión y actividad 15](figuras-referencia/pagina-08.png)

### Actividad 15. Pronóstico con modelos MA y ARIMA

**Pronóstico de series de tiempo con modelos MA y ARIMA.**

Investigue sobre los modelos de **autocorrelación y ARIMA**.

Investigue sobre el **suavizado con promedio / media móvil (MA)**.

**a.** Analice la predicción con los modelos **MA y ARIMA** para el mismo periodo del numeral 11. Grafique los resultados.  
**b.** Analice posibles resultados que puede obtener con los modelos **ARIMA y MA** de la serie de tiempo.

> **Nota de fidelidad:** la redacción del punto 15.b en el PDF es incompleta («Analice posibles con los modelos...»). Se ha hecho una corrección mínima de legibilidad, sin introducir exigencias nuevas. «MA» se emplea en el enunciado para media móvil/suavizado; al desarrollar el notebook conviene aclarar la diferencia con el componente *moving average* de ARIMA.

---

## 4. Fuentes y enlaces citados por el enunciado

1. [Banco de la República: Portal de Estadísticas Económicas](https://suameca.banrep.gov.co/estadisticas-economicas/).
2. [Statsmodels: documentación de series temporales](https://www.statsmodels.org/stable/tsa.html).
3. *A Guide to Interpreting Time Series*, Oficina Australiana de Estadísticas (lectura adicional mencionada, pero no aportada en el archivo recibido).

## 5. Guía de desarrollo del repositorio (recomendación añadida, NO parte del enunciado)

### Orden del notebook

| Sección sugerida del notebook | Actividades del PDF | Evidencia esperada |
|---|---|---|
| 00. Introducción, fuente y dependencias | 1 | Identificación y justificación del dataset |
| 01. Ingesta y preparación | 2 | `pd.Series` con índice temporal; datos procesados exportados |
| 02. Exploración temporal | 3-4 | Serie general y estacionalidad por segmentos |
| 03. Tendencia con OLS | 5-6 | Respuestas teóricas, modelo y gráfica |
| 04. Descomposición | 7-10 | Resultados aditivo/multiplicativo y análisis de residuos |
| 05. Partición y modelo naïve | 11-12 | Entrenamiento, validación y pronóstico visualizados |
| 06. Evaluación del error | 13 | Función de métricas y análisis de resultados |
| 07. Regresión lineal | 14 | Modelo, ajuste y limitaciones |
| 08. Pronóstico MA/ARIMA | 15 | Comparación sobre el mismo horizonte de validación |
| 09. Conclusiones y reproducibilidad | Complemento sugerido | Conclusiones, fuentes y supuestos |

### Criterios para organizar los datos

- `data/raw/`: archivo descargado **sin modificar** del Banco de la República.
- `data/processed/`: versión procesada que conserve fecha, variable, unidad y frecuencia.
- `notebooks/`: el `.ipynb` final con código, visualizaciones y respuestas redactadas.
- `src/`: funciones reutilizables opcionales (preparación, métricas y modelos).
- `outputs/figures/`: figuras exportadas, distintas de las imágenes de referencia del PDF.
- `outputs/metrics/`: tablas de errores o comparaciones exportadas.
- `docs/figuras-referencia/`: capturas fieles de las páginas ilustradas del PDF original.

### Controles de calidad recomendados

- Utilizar un dataset distinto de la tasa de desempleo nacional del ejemplo.
- Verificar la frecuencia de observación y mantener fechas ordenadas y sin duplicados.
- Ajustar el periodo de estacionalidad a la frecuencia de la serie; **12** solo corresponde al caso mensual del ejemplo.
- Separar entrenamiento de validación **antes** de ajustar los modelos para evitar filtración de información futura.
- Calcular todas las métricas sobre las mismas fechas y con una convención de error indicada.
- Documentar valores nulos, ceros, medidas no aplicables y supuestos del modelo multiplicativo.
- No copiar como resultados propios los números ni las gráficas del ejemplo del docente.
