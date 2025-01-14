import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Datos para todas las redes
redes = {
    "RED FAa-07": {
        "frequencies": [100, 100, 500, 500, 1000, 1000],
        "v_rms_ch1": [354.0, 356.1, 281.1, 356.1, 191.6, 191.1],
        "v_rms_ch2": [351.3, 352.6, 280.3, 352.6, 190.2, 190.1],
        "phase_ch1": [8.634, 8.564, 35.39, 34.77, 63.73, 61.85],
        "phase_ch2": [-8.646, -8.519, 325.2, 325.2, 318.2, 0]
    },
    "RED FBa-02": {
        "frequencies": [100, 100, 500, 500, 1000, 1000],
        "v_rms_ch1": [354.9, 354.1, 341.1, 355.7, 253.4, 253.5],
        "v_rms_ch2": [352.4, 353.6, 339.4, 353.6, 252.2, 251.4],
        "phase_ch1": [5.111, 6.102, 32.83, 33.23, 82.31, 81.91],
        "phase_ch2": [353.5, 354.1, 326.6, 326.6, 274.5, 275.2]
    },
    "RED FC-07": {
        "frequencies": [100, 100, 500, 500, 1000, 1000],
        "v_rms_ch1": [354.7, 355.7, 353.8, 355.7, 353.4, 353.5],
        "v_rms_ch2": [353.2, 354.5, 244.5, 242.6, 155.2, 153.4],
        "phase_ch1": [7.273, 10.323, 36.34, 37.13, 62.71, 63.23],
        "phase_ch2": [-7.200, -11.422, 313.9, 313.6, -20.61, -19.98]
    },
    "RED FAb-02": {
        "frequencies": [100, 100, 500, 500, 1000, 1000],
        "v_rms_ch1": [354.7, 355.7, 49.98, 52.43, 353.4, 353.5],
        "v_rms_ch2": [11.52, 12.43, 352.5, 353.8, 94.42, 94.04],
        "phase_ch1": [-108.3, -108.3, -84.23, -83.04, -72.71, -73.23],
        "phase_ch2": [106.1, -103.1, 85.23, 86.14, 75.61, 73.68]
    }
}

# Función para calcular ganancia y diferencia de fase
def calcular_puntos(red):
    frequencies = red["frequencies"]
    v_rms_ch1 = np.array(red["v_rms_ch1"])
    v_rms_ch2 = np.array(red["v_rms_ch2"])
    phase_ch1 = np.array(red["phase_ch1"])
    phase_ch2 = np.array(red["phase_ch2"])

    # Cálculo de ganancia en dB
    gain_db = 20 * np.log10(v_rms_ch2 / v_rms_ch1)

    # Cálculo de diferencia de fase
    phase_diff = phase_ch2 - phase_ch1
    phase_diff = np.where(phase_diff < -180, phase_diff + 360, phase_diff)
    phase_diff = np.where(phase_diff > 180, phase_diff - 360, phase_diff)

    return frequencies, gain_db, phase_diff

# Gráficas y resultados
for red_name, red_data in redes.items():
    frequencies, gain_db, phase_diff = calcular_puntos(red_data)

    # Crear un DataFrame para los resultados
    data = {
        'Frecuencia (Hz)': frequencies,
        'Ganancia (dB)': gain_db,
        'Diferencia de Fase (°)': phase_diff
    }
    df = pd.DataFrame(data)
    print(f"\nResultados para {red_name}:")
    print(df)

    # Graficar
    fig, ax = plt.subplots(2, 1, figsize=(8, 6))

    # Magnitud (Ganancia)
    ax[0].semilogx(frequencies, gain_db, marker='o', label='Ganancia (dB)', color='b')
    for freq, gain in zip(frequencies, gain_db):
        ax[0].text(freq, gain, f"({freq}Hz, {gain:.2f}dB)", fontsize=8, ha='left')
    ax[0].set_title(f"Diagrama de Bode - {red_name} - Magnitud")
    ax[0].set_xlabel("Frecuencia (Hz)")
    ax[0].set_ylabel("Ganancia (dB)")
    ax[0].grid(which="both", linestyle="--", linewidth=0.5)
    ax[0].legend()

    # Fase
    ax[1].semilogx(frequencies, phase_diff, marker='o', label='Diferencia de Fase (°)', color='r')
    for freq, phase in zip(frequencies, phase_diff):
        ax[1].text(freq, phase, f"({freq}Hz, {phase:.2f}°)", fontsize=8, ha='left')
    ax[1].set_title(f"Diagrama de Bode - {red_name} - Fase")
    ax[1].set_xlabel("Frecuencia (Hz)")
    ax[1].set_ylabel("Fase (°)")
    ax[1].grid(which="both", linestyle="--", linewidth=0.5)
    ax[1].legend()

    plt.tight_layout()
    plt.show()
