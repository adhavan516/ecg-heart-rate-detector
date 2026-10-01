from scipy.datasets import electrocardiogram
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt

ecg = electrocardiogram()

fs = 360

print("Number of samples", len(ecg))
print("Duration in seconds", len(ecg)/fs)
print("First 10 readings (Mv)", ecg[:10])
print("Highest reading:", ecg.max(), "mV")
print("Lowest reading:", ecg.min(), "mV")

#Bulding time axis,reading number/ reading per second =second
time = np.arange(len(ecg)) / fs

# Band-pass filter: keep heartbeat speeds (0.5–40 Hz), remove drift and jitter
b, a = butter(2, [0.5, 40], btype="bandpass", fs=fs)
ecg_clean = filtfilt(b, a, ecg)


# Draw raw and cleaned ECG, one above the other
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 6), sharex=True)

ax1.plot(time, ecg)
ax1.set_title("Raw ECG - MIT-BIH Record 208")
ax1.set_ylabel("Voltage (mV)")
ax1.grid(True)

ax2.plot(time, ecg_clean, color="green")
ax2.set_title("Filtered ECG (0.5–40 Hz band-pass)")
ax2.set_xlabel("Time (seconds)")
ax2.set_ylabel("Voltage (mV)")
ax2.grid(True)

ax1.set_xlim(38,48)
plt.tight_layout()
plt.savefig("raw_vs_filtered.png", dpi=150)
plt.show()
