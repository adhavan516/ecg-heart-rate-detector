from scipy.datasets import electrocardiogram

ecg = electrocardiogram()

fs = 360

print("Number of samples", len(ecg))
print("Duration in seconds", len(ecg)/fs)
print("First 10 readings (Mv)", ecg[:10])
print("Highest reading:", ecg.max(), "mV")
print("Lowest reading:", ecg.min(), "mV")