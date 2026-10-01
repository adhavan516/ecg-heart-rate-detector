from scipy.datasets import electrocardiogram
import numpy as np
import matplotlib.pyplot as plt


ecg = electrocardiogram()

fs = 360

print("Number of samples", len(ecg))
print("Duration in seconds", len(ecg)/fs)
print("First 10 readings (Mv)", ecg[:10])
print("Highest reading:", ecg.max(), "mV")
print("Lowest reading:", ecg.min(), "mV")

#Bulding time axis,reading number/ reading per second =second
time = np.arange(len(ecg)) / fs

#draw the ecg
plt.figure(figsize = (12,4))
plt.plot(time, ecg)
plt.xlabel("Time (seconds)")
plt.ylabel("Voltage (mV)")
plt.title("Raw ECG - MIT-BIH Record 208")
plt.xlim(0,10)
plt.grid(True)
plt.show()