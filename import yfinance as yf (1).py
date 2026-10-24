import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import time
import pytz

# --- FUNCIÓN PRINCIPAL DEL MONITOR ---
def iniciar_monitor(ticker_simbolo, nombre_indice, multiplicador_std, window_size=20):
    intervalo = "5m"
    periodo = "5d" 
    zona_horaria_arg = pytz.timezone('America/Argentina/Buenos_Aires')

    plt.ion() 
    fig, ax = plt.subplots(figsize=(14, 7))
    # El título de la ventana ahora también es dinámico
    fig.canvas.manager.set_window_title(f'Monitor {nombre_indice} - UTC-3')

    try:
        while True:
            # Descarga de datos
            data = yf.download(ticker_simbolo, period=periodo, interval=intervalo, progress=False)
            
            if data.empty:
                time.sleep(15)
                continue

            # Localización a Argentina
            if data.index.tz is None:
                data.index = data.index.tz_localize('UTC')
            data.index = data.index.tz_convert(zona_horaria_arg)

            # Cálculos
            data['Log_Return'] = np.log(data['Close'] / data['Close'].shift(1))
            data['Mean'] = data['Log_Return'].rolling(window=window_size).mean()
            data['Std'] = data['Log_Return'].rolling(window=window_size).std()
            data['Stationary_Return'] = data['Log_Return'] - data['Mean']
            data['Upper'] = multiplicador_std * data['Std']
            data['Lower'] = -multiplicador_std * data['Std']
            
            anomalias = data[(data['Stationary_Return'] > data['Upper']) | (data['Stationary_Return'] < data['Lower'])].copy()
            
            # --- TERMINAL: LIMPIA Y MUESTRA INFO DE RECOLECCIÓN ---
            print("\033c", end="") 
            print(f"=== MONITOR ACTIVO: {nombre_indice} ===")
            print(f"ÚLTIMA ACTUALIZACIÓN DE DATOS: {datetime.now(zona_horaria_arg).strftime('%H:%M:%S')}")
            print("-" * 50)
            
            if not anomalias.empty:
                for h in anomalias.index:
                    print(f"Punto detectado el día: {h.strftime('%d/%m/%Y')} a las: {h.strftime('%H:%M:%S')}")
            else:
                print("\nBuscando nuevas anomalías...")

            # --- DIBUJAR GRÁFICO ---
            ax.clear() 
            ax.axhline(y=0, color='black', linestyle='-', alpha=0.2)
            ax.plot(data.index, data['Stationary_Return'], color='gray', alpha=0.3)
            ax.plot(data.index, data['Upper'], color='red', linestyle='--', alpha=0.5)
            ax.plot(data.index, data['Lower'], color='green', linestyle='--', alpha=0.5)
            ax.scatter(anomalias.index, anomalias['Stationary_Return'], color='orange', s=35, zorder=5)

            # Anotaciones horarios
            ultimas_label = anomalias.tail(12)
            for idx in ultimas_label.index:
                valor_y = ultimas_label.loc[idx, 'Stationary_Return']
                if isinstance(valor_y, pd.Series): valor_y = valor_y.iloc[0]
                ax.annotate(idx.strftime('%H:%M'), (idx, float(valor_y)),
                            textcoords="offset points", xytext=(0,10), ha='center', 
                            fontsize=9, color='darkblue', rotation=45, fontweight='bold')

            # --- LÍNEA CORREGIDA: Título dinámico en el gráfico ---
            ax.set_title(f"{nombre_indice} ({intervalo}) - Argentina UTC-3")
            ax.grid(True, alpha=0.15)
            fig.canvas.draw_idle() 
            plt.pause(60) 

    except Exception as e:
        # Manejo simple de errores para evitar que el script se cierre por tipos de datos
        print(f"\nOcurrió un error: {e}")
        plt.show(block=True)

# --- MENÚ ---
if __name__ == "__main__":
    print("========================================")
    print("   PANEL DE CONTROL - TRADING MONITOR   ")
    print("========================================")
    print("1. NASDAQ 100")
    print("2. S&P 500")
    print("3. Micro BTC")
    print("========================================")
    
    opcion = input("Seleccione índice: ")
    
    if opcion == "1": 
        iniciar_monitor("NQ=F", "NASDAQ 100", 2.0)
    elif opcion == "2": 
        iniciar_monitor("ES=F", "S&P 500", 2.0)
    elif opcion == "3": 
        iniciar_monitor("MBT=F", "Micro Bitcoin", 2.5, 30)
    else:
        print("Opción inválida.")