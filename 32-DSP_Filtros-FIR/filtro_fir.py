import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt

# Parámetros del filtro
fs = 44100  # Frecuencia de muestreo (Hz)
cutoff = 5000  # Frecuencia de corte del filtro (Hz)
numtaps = 101  # Número de coeficientes del filtro (orden + 1)

# Diseño del filtro FIR paso bajo usando el método de ventanas (ventana Hamming)
fir_coefficients = signal.firwin(numtaps, cutoff, fs=fs, window='hamming')

# Crear una señal de prueba (mezcla de señales)
t = np.linspace(0, 0.01, fs)
signal_original = np.sin(2 * np.pi * 1000 * t) + 0.5 * np.sin(2 * np.pi * 7000 * t)

# Aplicar el filtro FIR a la señal
signal_filtrada = signal.lfilter(fir_coefficients, 1.0, signal_original)

# Graficar la señal original y la señal filtrada
plt.figure(figsize=(12, 6))
plt.subplot(2, 1, 1)
plt.plot(t, signal_original, label='Señal Original')
plt.title('Señal Original')
plt.xlabel('Tiempo [s]')
plt.ylabel('Amplitud')
plt.grid(True)

plt.subplot(2, 1, 2)
plt.plot(t, signal_filtrada, label='Señal Filtrada', color='orange')
plt.title('Señal Filtrada con Filtro FIR')
plt.xlabel('Tiempo [s]')
plt.ylabel('Amplitud')
plt.grid(True)

plt.tight_layout()
plt.show()
