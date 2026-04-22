"""
Ejercicio 2: Filtro IIR en el dominio de la frecuencia con señales de audio en Python
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import scipy.io

# 2a. Cargar el archivo de audio Tchaikovsky.mat
data = scipy.io.loadmat('Tchaikovsky.mat')
Fs = data['Fs'][0, 0]  # Frecuencia de muestreo
signal_audio = data['signal']  # Señal de audio estéreo
canal = signal_audio[:, 0]  # Seleccionar el primer canal

# Normalización de la señal para evitar problemas numéricos
canal = canal / np.max(np.abs(canal))

# 2b. Diseño del filtro IIR elíptico
orden = 6
f1, f2 = 300, 3400  # Frecuencias de corte en Hz
rp = 0.5  # Ripple en la banda de paso en dB
rs = 60   # Atenuación en la banda de rechazo en dB

# Diseño del filtro pasa-banda Elíptico
b, a = signal.ellip(orden, rp, rs, [f1, f2], btype='bandpass', fs=Fs)

# 2c. Graficar la respuesta en frecuencia del filtro IIR
w, h = signal.freqz(b, a, worN=2000)
plt.figure(figsize=(12, 6))
plt.subplot(2, 1, 1)
plt.plot(w * Fs / (2 * np.pi), 20 * np.log10(abs(h)), color='blue')
plt.title('Respuesta en frecuencia del filtro Elíptico Pasa-Banda (Orden 6)')
plt.xlabel('Frecuencia [Hz]')
plt.ylabel('Amplitud [dB]')
plt.grid(True)
plt.axvline(f1, color='green', linestyle='--', label='Frecuencia de corte inferior')
plt.axvline(f2, color='green', linestyle='--', label='Frecuencia de corte superior')
plt.legend()

# Graficar respuesta de fase
plt.subplot(2, 1, 2)
plt.plot(w * Fs / (2 * np.pi), np.unwrap(np.angle(h)), color='blue')
plt.xlabel('Frecuencia [Hz]')
plt.ylabel('Fase [radianes]')
plt.grid(True)
plt.tight_layout()
plt.show()

# 2d. Aumentar el orden del filtro a 12 y graficar su respuesta
orden_12 = 12
b, a = signal.ellip(orden_12, rp, rs, [f1, f2], btype='bandpass', fs=Fs)

# Respuesta en frecuencia del filtro IIR (orden 12)
w, h = signal.freqz(b, a, worN=2000)
plt.figure(figsize=(12, 6))
plt.plot(w * Fs / (2 * np.pi), 20 * np.log10(abs(h)), color='red', label='Orden 12')
plt.title('Respuesta en frecuencia del filtro Elíptico Pasa-Banda (Orden 12)')
plt.xlabel('Frecuencia [Hz]')
plt.ylabel('Amplitud [dB]')
plt.grid(True)
plt.axvline(f1, color='green', linestyle='--')
plt.axvline(f2, color='green', linestyle='--')
plt.legend()
plt.show()

# 2e. Transformar el filtro a una arquitectura SOS (Second-Order Sections)
sos = signal.tf2sos(b, a)

# 2f. Filtrar la señal de audio usando la representación SOS
senal_filtrada = signal.sosfilt(sos, canal)

# Verificación de valores NaN en la señal filtrada
if np.isnan(senal_filtrada).any():
    print("La señal filtrada contiene NaN. Se reemplazarán por ceros.")
    senal_filtrada = np.nan_to_num(senal_filtrada)

# 2g. Graficar los espectros de la señal original y filtrada
frequencies = np.fft.fftfreq(len(canal), d=1/Fs)
Y_original = np.fft.fft(canal)
Y_filtrada = np.fft.fft(senal_filtrada)

plt.figure(figsize=(12, 6))
plt.plot(frequencies[:len(frequencies)//2], np.abs(Y_original)[:len(frequencies)//2], label='Original')
plt.plot(frequencies[:len(frequencies)//2], np.abs(Y_filtrada)[:len(frequencies)//2], label='Filtrada', alpha=0.7, color='red')
plt.title('Espectros de la señal original y filtrada')
plt.xlabel('Frecuencia [Hz]')
plt.ylabel('Amplitud')
plt.legend()
plt.grid()
plt.show()

# 2h. Observación de las gráficas
print("Compare las gráficas de los espectros para notar la diferencia en la atenuación fuera de la banda de paso.")
