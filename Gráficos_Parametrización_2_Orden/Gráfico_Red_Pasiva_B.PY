# Librerías Utilizadas
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


# Leer el archivo CSV de la red pasiva FBa-02
ruta_csv = r"C:\Users\paull\Desktop\waveform.RA.FBa-02.csv"  # Ruta del archivo CSV.
datos = pd.read_csv(ruta_csv, sep='\t', skiprows=1)  # Lectura del archivo CSV.




# Variables para los cálculos
channel2 = datos['Channel2']
time = datos['Time']




# Valor de régimen (valor final del sistema)
valor_regimen = channel2.iloc[-1]




# Valor de pico y tiempo de pico
valor_pico = channel2.max()
tiempo_pico = time[channel2.idxmax()]




# Sobreoscilación máxima porcentual
sobreoscilacion = ((valor_pico - valor_regimen) / abs(valor_regimen)) * 100




# Tiempo de subida (10% a 90% del valor de régimen)
try:
    tiempo_subida_inicio = time[np.where(channel2.values >= 0.1 * valor_regimen)[0][0]]
    tiempo_subida_fin = time[np.where(channel2.values >= 0.9 * valor_regimen)[0][0]]
    tiempo_subida = tiempo_subida_fin - tiempo_subida_inicio
except IndexError:
    tiempo_subida = None  # Si no hay datos suficientes, asignar None.




# Tiempo de retardo (tiempo en alcanzar el 50% del valor de régimen)
try:
    tiempo_retardo = time[np.where(channel2.values >= 0.5 * valor_regimen)[0][0]]
except IndexError:
    tiempo_retardo = None




# Tiempo de asentamiento (criterio del 2% del valor de régimen)
margen_asentamiento = 0.02 * abs(valor_regimen)
indices_asentamiento = np.where(
    (channel2.values >= valor_regimen - margen_asentamiento) &
    (channel2.values <= valor_regimen + margen_asentamiento)
)[0]
tiempo_asentamiento = time[indices_asentamiento[-1]] if len(indices_asentamiento) > 0 else None




# Período de oscilación (tiempo entre dos picos consecutivos si existen)
peaks_indices = np.where((channel2.values[1:-1] > channel2.values[:-2]) & (channel2.values[1:-1] > channel2.values[2:]))[0] + 1
if len(peaks_indices) > 1:
    periodo_oscilacion = time[peaks_indices[1]] - time[peaks_indices[0]]
else:
    periodo_oscilacion = None




# Frecuencia de oscilación
if periodo_oscilacion:
    frecuencia_oscilacion = 1 / periodo_oscilacion
else:
    frecuencia_oscilacion = None




# Crear la gráfica
plt.figure(figsize=(12, 12))
plt.plot(time, datos['Channel1'], marker='o', label='Channel1', color='blue')
plt.plot(time, channel2, marker='x', label='Channel2', color='orange')




# Añadir los parámetros principales a la gráfica
plt.axhline(y=valor_regimen, color='red', linestyle='--', label=f'Valor de régimen = {valor_regimen:.6f}')
plt.scatter(tiempo_pico, valor_pico, color='purple', label=f'Valor de pico = {valor_pico:.6f}, Tiempo de pico = {tiempo_pico:.6f}s')
if tiempo_subida:
    plt.axvline(x=tiempo_subida_inicio, color='green', linestyle='--', label=f'Tiempo de subida = {tiempo_subida:.6f}s')
if tiempo_retardo:
    plt.axvline(x=tiempo_retardo, color='cyan', linestyle='--', label=f'Tiempo de retardo = {tiempo_retardo:.6f}s')
if tiempo_asentamiento:
    plt.axvline(x=tiempo_asentamiento, color='magenta', linestyle='--', label=f'Tiempo de asentamiento = {tiempo_asentamiento:.6f}s')
parametros_adicionales = f'Sobreoscilación = {sobreoscilacion:.2f}%'
if frecuencia_oscilacion:
    parametros_adicionales += f'\nFrecuencia de oscilación = {frecuencia_oscilacion:.2f}Hz'
plt.legend(fontsize=10, title=parametros_adicionales)






# Personalizar la gráfica
plt.title('Red Pasiva FBa-02', fontsize=14)
plt.xlabel('Tiempo (s)', fontsize=12)
plt.ylabel('Amplitud', fontsize=12)
plt.grid()





# Mostrar la gráfica
plt.show()