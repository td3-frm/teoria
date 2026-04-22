"""
Ejercicio 1: Filtro Leaking Integrator (LI) con señales senoidales en Python

a) Genere una señal senoidal con frecuencia fundamental de 100 Hz.

b) Agregue ruido a la señal senoidal tal que la relación señal a ruido entre la 
   señal senoidal y la señal con ruido sea de 15 dB.

c) Diseñe un filtro Leaking Integrator (LI) con λ igual a 0.7.

d) Grafique la respuesta en frecuencia y fase del filtro LI. Use la función freqz().
   Determine la frecuencia de corte fco con:

   fco = - ln(λ) * fs / π

e) Determine el cero y el polo del filtro con la función zplane(). ¿Es el filtro estable?

f) Aplique el filtro LI a la señal con ruido. Utilice la función lfilter() de scipy.signal.
   Determine los valores de b y a.

g) Grafique la respuesta en el tiempo de las señales original y filtrada y compare.

h) Grafique la respuesta en frecuencia de las señales original y filtrada y compare.

i) Repita los puntos c) a h) para λ igual a 0.9 y 0.98. Analice el comportamiento de la fco.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import lfilter, freqz

# 1a. Generación de una señal senoidal de 100 Hz
frecuencia_fundamental = 100  # Frecuencia de la señal en Hz
frecuencia_muestreo = 1000  # Frecuencia de muestreo en Hz
duracion = 1  # Duración de la señal en segundos
t = np.arange(0, duracion, 1/frecuencia_muestreo)  # Vector de tiempo
senal_senoidal = np.sin(2 * np.pi * frecuencia_fundamental * t)  # Señal senoidal

# 1b. Agregar ruido gaussiano con SNR de 15 dB
SNR = 15  # Relación señal-ruido en dB
potencia_senal = np.mean(senal_senoidal**2)
potencia_ruido = potencia_senal / (10**(SNR / 10))
ruido = np.sqrt(potencia_ruido) * np.random.randn(len(t))
senal_ruidosa = senal_senoidal + ruido

# Función para graficar zplane
def zplane(b, a):
    from matplotlib import patches
    from numpy import roots

    ax = plt.subplot(111)
    unit_circle = patches.Circle((0, 0), radius=1, fill=False, color='black', ls='dotted')
    ax.add_patch(unit_circle)

    poles = roots(a)
    zeros = roots(b)
    plt.scatter(np.real(zeros), np.imag(zeros), color='blue', label='Ceros')
    plt.scatter(np.real(poles), np.imag(poles), color='red', label='Polos')
    plt.title('Diagrama de Polos y Ceros')
    plt.xlabel('Re')
    plt.ylabel('Im')
    plt.grid()
    plt.axhline(0, color='black', lw=1)
    plt.axvline(0, color='black', lw=1)
    plt.legend(loc='best')
    plt.show()

# 1c. Diseño del filtro Leaking Integrator (LI) con λ = 0.7
lmbd = 0.7
b = [1]  # Coeficiente de numerador
a = [1, -lmbd]  # Coeficientes de denominador

# 1d. Respuesta en frecuencia del filtro LI y cálculo de la frecuencia de corte
w, h = freqz(b, a, worN=8000)
fco = -np.log(lmbd) * frecuencia_muestreo / np.pi

# Gráfica de la respuesta en frecuencia y fase
plt.figure(figsize=(12, 6))
plt.subplot(2, 1, 1)
plt.plot(w * frecuencia_muestreo / (2 * np.pi), 20 * np.log10(abs(h)))
plt.title('Respuesta en frecuencia del filtro LI (λ=0.7)')
plt.xlabel('Frecuencia [Hz]')
plt.ylabel('Amplitud [dB]')
plt.grid()

plt.subplot(2, 1, 2)
plt.plot(w * frecuencia_muestreo / (2 * np.pi), np.angle(h))
plt.xlabel('Frecuencia [Hz]')
plt.ylabel('Fase [radianes]')
plt.grid()
plt.tight_layout()
plt.show()

# 1e. Diagrama de polos y ceros
zplane(b, a)

# 1f. Filtrado de la señal con ruido usando el filtro LI
senal_filtrada = lfilter(b, a, senal_ruidosa)

# 1g. Gráfica de las señales en el dominio del tiempo
plt.figure(figsize=(12, 6))
plt.plot(t, senal_senoidal, label='Señal original')
plt.plot(t, senal_ruidosa, label='Señal con ruido', alpha=0.7)
plt.plot(t, senal_filtrada, label='Señal filtrada', alpha=0.7)
plt.title('Señales en el dominio del tiempo')
plt.xlabel('Tiempo [s]')
plt.ylabel('Amplitud')
plt.legend()
plt.grid()
plt.xlim(0, 0.1)  # Mostrar solo los primeros 0.1 segundos
plt.show()

# 1h. Respuesta en frecuencia de las señales original y filtrada
frequencies = np.fft.fftfreq(len(t), d=1/frecuencia_muestreo)
Y_original = np.fft.fft(senal_senoidal)
Y_filtrada = np.fft.fft(senal_filtrada)

plt.figure(figsize=(12, 6))
plt.plot(frequencies[:len(frequencies)//2], np.abs(Y_original)[:len(frequencies)//2], label='Original')
plt.plot(frequencies[:len(frequencies)//2], np.abs(Y_filtrada)[:len(frequencies)//2], label='Filtrada', alpha=0.7)
plt.title('Respuesta en frecuencia de las señales')
plt.xlabel('Frecuencia [Hz]')
plt.ylabel('Amplitud')
plt.legend()
plt.grid()
plt.show()

# 1i. Repetir para λ = 0.9 y λ = 0.98
for lmbd in [0.9, 0.98]:
    b = [1]
    a = [1, -lmbd]
    fco = -np.log(lmbd) * frecuencia_muestreo / np.pi
    senal_filtrada = lfilter(b, a, senal_ruidosa)

    # Gráfica de la respuesta en frecuencia
    w, h = freqz(b, a, worN=8000)
    plt.figure(figsize=(12, 6))
    plt.plot(w * frecuencia_muestreo / (2 * np.pi), 20 * np.log10(abs(h)), label=f'λ={lmbd}')
    plt.title(f'Respuesta en frecuencia del filtro LI (λ={lmbd})')
    plt.xlabel('Frecuencia [Hz]')
    plt.ylabel('Amplitud [dB]')
    plt.grid()
    plt.legend()
    plt.show()
