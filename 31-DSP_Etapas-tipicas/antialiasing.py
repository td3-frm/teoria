import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter, freqz

# Step 1: Generate a continuous-time signal
def generate_signal(duration, fs, f1, f2):
    t = np.linspace(0, duration, int(fs * duration), endpoint=False)
    signal = np.sin(2 * np.pi * f1 * t) + 0.5 * np.sin(2 * np.pi * f2 * t)
    return t, signal

# Step 2: Design a low-pass Butterworth filter
def butter_lowpass(cutoff, fs, order=5):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y

# Step 3: Define parameters
duration = 1.0  # seconds
fs_continuous = 5000  # continuous sampling frequency in Hz
f1 = 50  # frequency of the first sine wave
f2 = 1500  # frequency of the second sine wave (higher frequency)
cutoff = 100  # cutoff frequency for the low-pass filter
fs_sampled = 200  # sampling frequency in Hz

# Generate the signal
t, signal = generate_signal(duration, fs_continuous, f1, f2)

# Apply the low-pass filter
filtered_signal = lowpass_filter(signal, cutoff, fs_continuous)

# Step 4: Sample the filtered signal
t_sampled = np.arange(0, duration, 1/fs_sampled)
sampled_signal = np.interp(t_sampled, t, filtered_signal)

# Plotting
plt.figure(figsize=(15, 10))

# Original Signal
plt.subplot(3, 1, 1)
plt.plot(t, signal, label='Original Signal')
plt.title('Original Signal in Time Domain')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')
plt.grid()

# Filtered Signal
plt.subplot(3, 1, 2)
plt.plot(t, filtered_signal, label='Filtered Signal', color='orange')
plt.title('Filtered Signal (Anti-Aliasing) in Time Domain')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')
plt.grid()

# Sampled Signal
plt.subplot(3, 1, 3)
plt.stem(t_sampled, sampled_signal, linefmt='r-', markerfmt='ro', basefmt='r-') # , use_line_collection=True
plt.title('Sampled Signal after Filtering')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')
plt.grid()

plt.tight_layout()
plt.show()

dumb = 1