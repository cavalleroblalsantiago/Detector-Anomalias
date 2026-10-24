# 📈 Real-Time Financial Anomaly Monitor

Un monitor interactivo en tiempo real desarrollado en Python para detectar anomalías y movimientos atípicos en activos financieros mediante análisis estadístico de series temporales.

---

## 🎯 Objetivo del Proyecto

El proyecto busca transformar datos crudos de precios intradía (intervalos de 5 minutos) en métricas estadísticas estacionarias que permitan identificar volúmenes atípicos de volatilidad o desviaciones significativas en índices clave (**NASDAQ 100**, **S&P 500**) y criptoactivos (**Micro Bitcoin**).

---

## 🛠️ Tecnologías Utilizadas

- **Lenguaje:** Python 3.x
- **Ingesta de Datos:** `yfinance` (Yahoo Finance API)
- **Procesamiento de Datos:** `pandas`, `numpy`
- **Visualización Dinámica:** `matplotlib`
- **Manejo de Tiempos & Zonas Horarias:** `pytz`, `datetime`

---

## 📊 Metodología Estadística & Análisis

1. **Rendimientos Logarítmicos (`Log Returns`):** 
   En lugar de trabajar con precios absolutos, se calculan los rendimientos logarítmicos para estabilizar la varianza y permitir comparaciones homogéneas entre diferentes periodos:
   $$\text{Log\_Return}_t = \ln\left(\frac{\text{Precio}_t}{\text{Precio}_{t-1}}\right)$$

2. **Estacionalidad y Descomposición:**
   Se remueve la tendencia media mediante una media móvil rolling de $N$ periodos para obtener rendimientos estacionarios alrededor de cero:
   $$\text{Stationary\_Return}_t = \text{Log\_Return}_t - \text{Mean}_{\text{rolling}}$$

3. **Bandas Dinámicas de Anomalía:**
   Se calculan límites superiores e inferiores basados en $k$ desviaciones estándar móviles (`Rolling Std`):
   $$\text{Upper} = k \times \sigma_{\text{rolling}}$$
   $$\text{Lower} = -k \times \sigma_{\text{rolling}}$$
   Cualquier retorno que supere estas bandas es etiquetado automáticamente como una **anomalía en tiempo real**.

---

## ⚙️ Características Clave

- **Panel Interactivo por Consola:** Selección amigable de activos financieros al iniciar el programa.
- **Actualización Dinámica (Live Plotting):** Redibujado en segundo plano con refresco automático en tiempo real.
- **Gestión de Zonas Horarias:** Normalización automática de horarios a huso local (UTC-3 Argentina).
- **Anotaciones visuales:** Indicadores de hora exacta sobre los puntos donde se detectan desviaciones fuera de norma.
