# Librerías usadas
import matplotlib.pyplot as plt
import pandas as pd  
import numpy as np 




# Leer el archivo CSV de la red pasiva FAa-07
ruta_csv = r"C:\Users\paull\Desktop\waveform.RAb_Bb.FAb-02.csv"  # Ruta del archivo CSV
datos = pd.read_csv(ruta_csv, sep='\t', skiprows=1)  # Lectura del archivo CSV




# Filtrar los datos solo para los cálculos (valores donde Time > 0)
datos_filtrados = datos[datos['Time'] > 0].reset_index(drop=True)





# Verificar si hay datos suficientes después del filtrado
if datos_filtrados.empty:
    raise ValueError("No hay valores mayores a 0 en 'Time'. Verifica los datos.")





# Ganancia estática, se escoge el valor final ya que es un sistema de primer orden

K = datos_filtrados['Channel2'].iloc[-1]  # Obtener el último valor de 'Channel2' después del filtrado
print(f"Ganancia estática (K) = {K:.6f}")  # Imprimir la ganancia estática





# Encontrar el índice para τ (63.2% de K)

tau_threshold = 0.632 * K  # Calcular el 63.2% de K
tau_index = np.where(datos_filtrados['Channel2'] >= tau_threshold)[0]  # Índices donde 'Channel2' cruza el umbral

if tau_index.size == 0:
    raise ValueError("No se encontró un valor que alcance el 63.2% de K. Verifica los datos.")




# Calcular τ

idx_before = tau_index[0] - 1  # Índice anterior al cruce del umbral
idx_after = tau_index[0]  # Índice del cruce del umbral
x1, x2 = datos_filtrados['Time'].iloc[idx_before], datos_filtrados['Time'].iloc[idx_after]  # Tiempos antes y después del cruce
y1, y2 = datos_filtrados['Channel2'].iloc[idx_before], datos_filtrados['Channel2'].iloc[idx_after]  # Valores de 'Channel2' antes y después del cruce





# Evitar división por cero

if y2 == y1:
    tau = datos_filtrados['Time'].iloc[tau_index[0]]  # Asume τ como el tiempo del índice más cercano
else:
    tau = x1 + (tau_threshold - y1) * (x2 - x1) / (y2 - y1)  # Interpolación lineal






# Crear gráfico

plt.figure(figsize=(10, 6))
plt.plot(datos['Time'], datos['Channel1'], marker='o', label='Channel1', color='blue')  # Graficar todos los datos de 'Channel1'
plt.plot(datos['Time'], datos['Channel2'], marker='x', label='Channel2', color='orange')  # Graficar todos los datos de 'Channel2'





# Agregar líneas horizontales y verticales solo basadas en cálculos filtrados

plt.axhline(y=K, color='red', linestyle='--', label=f'Ganancia estática (K) = {K:.6f}')  # Línea horizontal en K
plt.axvline(x=tau, color='green', linestyle='--', label=f'Constante de tiempo (τ) = {tau:.6f} s')  # Línea vertical en τ





# Texto con los valores de K y τ

plt.text(datos['Time'].min() + 0.05, K + 0.05, f"K = {K:.6f}", color='red', fontsize=12)
plt.text(tau + 0.05, datos['Channel1'].min() + 0.05, f"τ = {tau:.6f} s", color='green', fontsize=12)






# Personalizar la gráfica

plt.title('Red Pasiva FAb-02')  
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud')
plt.legend()
plt.grid()





# Mostrar la gráfica

plt.show()
