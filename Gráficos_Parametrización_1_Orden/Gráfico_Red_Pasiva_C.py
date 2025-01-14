#librerías usadas
import matplotlib.pyplot as plt
import pandas as pd  
import numpy as np 




# Leer el archivo CSV de la red pasiva FAa-07

ruta_csv = r"C:\Users\paull\Desktop\waveform.RA.FC-07.csv"  #Ruta del archivo CSV.
datos = pd.read_csv(ruta_csv, sep='\t', skiprows=1)  # Lectura del archivo CSV con separador de tabulaciones, omitiendo la primera fila.





# Ganancia estática, se escoge el valor final ya que es un sistema de primer orden.

K = datos['Channel2'].iloc[-1]  # Obtener el último valor de 'Channel2', que representa la ganancia estática.
print(f"Ganancia estática (K) = {K:.6f}")  # Imprimir la ganancia estática.




# Encontrar el índice para τ (63.2% de K)

tau_threshold = 0.632 * K  # Calcular el 63.2% de K, para encontrar τ.
tau_index = np.where(datos['Channel2'] >= tau_threshold)[0]  # Encontrar el índice donde 'Channel2' alcanza o supera este umbral.




# Calcular τ

idx_before = tau_index[0] - 1  # Índice anterior al umbral de τ.
idx_after = tau_index[0]  # Índice en el umbral de τ.
x1, x2 = datos['Time'].iloc[idx_before], datos['Time'].iloc[idx_after]  # Tiempos correspondientes a los índices antes y después del umbral.
y1, y2 = datos['Channel2'].iloc[idx_before], datos['Channel2'].iloc[idx_after]  # Valores de 'Channel2' en los mismos índices.
tau = x1 + (tau_threshold - y1) * (x2 - x1) / (y2 - y1)  # Interpolación lineal para calcular τ.




# Crear gráfico

plt.figure(figsize=(10, 6))  # Crear una nueva figura con tamaño especificado.
plt.plot(datos['Time'], datos['Channel1'], marker='o', label='Channel1', color='blue')  # Graficar 'Channel1' con puntos.
plt.plot(datos['Time'], datos['Channel2'], marker='x', label='Channel2', color='orange')  # Graficar 'Channel2' con cruces.
plt.title('Red Pasiva FC-07')  # Título de la gráfica.
plt.xlabel('Tiempo (s)')  # Etiqueta del eje X.
plt.ylabel('Amplitud')  # Etiqueta del eje Y.
plt.legend()  # Mostrar leyenda de la gráfica.
plt.grid()  # Mostrar la cuadrícula en la gráfica.




# Añadir los parámetros principales a la gráfica

plt.axhline(y=K, color='red', linestyle='--', label=f'Ganancia estática (K) = {K:.6f}')  # Línea horizontal en K.
plt.axvline(x=tau, color='green', linestyle='--', label=f'Constante de tiempo (τ) = {tau:.6f} s')  # Línea vertical en τ.




# Texto con los valores de K y τ en la gráfica

plt.text(datos['Time'].min() + 0.05, K + 0.05, f"K = {K:.6f}", color='red', fontsize=12)  # Añadir texto con el valor de K.
plt.text(tau + 0.05, datos['Channel1'].min() + 0.05, f"τ = {tau:.6f} s", color='green', fontsize=12)  # Añadir texto con el valor de τ.



# Personalizar la gráfica

plt.title('Red Pasiva FC-07')  # Título de la gráfica 
plt.xlabel('Tiempo (s)')  # Etiqueta del eje X 
plt.ylabel('Amplitud')  # Etiqueta del eje Y 
plt.legend()  # Mostrar leyenda 
plt.grid()  # Mostrar cuadrícula 


# Mostrar la gráfica

plt.show() 
