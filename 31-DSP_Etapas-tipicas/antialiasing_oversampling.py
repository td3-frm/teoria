import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq

# Step 1: Generate a continuous-time signal
def generate_signal(duration, fs, f1, f2):
    t = np.linspace(0, duration, int(fs * duration), endpoint=False)
    signal = np.sin(2 * np.pi * f1 * t) + 0.5 * np.sin(2 * np.pi * f2 * t)
    return t, signal

# Step 2: Define parameters
duration = 1.0  # seconds
f1 = 50  # frequency of the first sine wave
f2 = 200  # frequency of the second sine wave

# Nyquist sampling parameters
fs_nyquist = 2 * f2  # Nyquist rate (twice the max frequency)

# Oversampling parameters
oversampling_factor = 5  # oversampling by a factor of 5
fs_oversampled = oversampling_factor * fs_nyquist

# Generate signals
t_nyquist, signal_nyquist = generate_signal(duration, fs_nyquist, f1, f2)
t_oversampled, signal_oversampled = generate_signal(duration, fs_oversampled, f1, f2)

# Step 3: Perform FFT for frequency-domain analysis
def compute_fft(signal, fs):
    N = len(signal)
    signal_fft = fft(signal)
    freqs = fftfreq(N, 1/fs)[:N//2]
    magnitudes = 2.0/N * np.abs(signal_fft[:N//2])
    return freqs, magnitudes

# FFT for Nyquist-sampled signal
freqs_nyquist, magnitudes_nyquist = compute_fft(signal_nyquist, fs_nyquist)

# FFT for Oversampled signal
freqs_oversampled, magnitudes_oversampled = compute_fft(signal_oversampled, fs_oversampled)

# Plotting
plt.figure(figsize=(15, 10))

# Original Signal in Time Domain
plt.subplot(3, 1, 1)
plt.plot(t_oversampled, signal_oversampled, label='Original Signal')
plt.title('Original Continuous-Time Signal')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')
plt.grid()

# Frequency Spectrum at Nyquist Sampling
plt.subplot(3, 1, 2)
plt.plot(freqs_nyquist, magnitudes_nyquist, label='Nyquist Sampled Signal', color='r')
plt.title('Frequency Spectrum at Nyquist Sampling Rate')
plt.xlabel('Frequency [Hz]')
plt.ylabel('Magnitude')
plt.grid()

# Frequency Spectrum with Oversampling
plt.subplot(3, 1, 3)
plt.plot(freqs_oversampled, magnitudes_oversampled, label='Oversampled Signal', color='g')
plt.title('Frequency Spectrum with Oversampling')
plt.xlabel('Frequency [Hz]')
plt.ylabel('Magnitude')
plt.grid()

plt.tight_layout()
plt.show()

dumb = 1