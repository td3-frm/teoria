import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import firwin, lfilter, freqz

# Parámetros del filtro
fc = 1000      # Frecuencia de corte (Hz)
fs = 8000      # Frecuencia de muestreo (Hz)
orden = 101    # Orden del filtro (número de coeficientes - 1)

# Diseño del filtro FIR pasa bajos
filtro_fir = firwin(numtaps=orden, cutoff=fc, fs=fs)

# Análisis de la respuesta en frecuencia
w, h = freqz(filtro_fir, worN=8000)
plt.figure(figsize=(10, 4))
plt.plot((w / np.pi) * (fs / 2), 20 * np.log10(np.abs(h)), 'b')
plt.title('Respuesta en frecuencia del filtro FIR pasa bajos')
plt.xlabel('Frecuencia [Hz]')
plt.ylabel('Magnitud [dB]')
plt.grid()
plt.show()

# Señal de prueba: combinación de dos senoidales (una dentro y otra fuera de la banda)
t = np.arange(0, 0.01, 1/fs)
senal = np.sin(2 * np.pi * 500 * t) + 0.5 * np.sin(2 * np.pi * 2500 * t)

# Aplicar el filtro FIR
senal_filtrada = lfilter(filtro_fir, 1.0, senal)

# Graficar las señales
plt.figure(figsize=(10, 6))
plt.subplot(2, 1, 1)
plt.plot(t, senal)
plt.title('Señal original (500 Hz + 2500 Hz)')
plt.xlabel('Tiempo [s]')
plt.ylabel('Amplitud')
plt.grid()

plt.subplot(2, 1, 2)
plt.plot(t, senal_filtrada, color='orange')
plt.title('Señal filtrada (solo componente de baja frecuencia)')
plt.xlabel('Tiempo [s]')
plt.ylabel('Amplitud')
plt.grid()

plt.tight_layout()
plt.show()
