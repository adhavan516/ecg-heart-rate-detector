from scipy.datasets import electrocardiogram
from scipy.signal import butter, filtfilt, find_peaks
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ---------- 1. Load the ECG ----------
# 5-minute real ECG from the MIT-BIH Arrhythmia Database (record 208), in mV
ecg = electrocardiogram()
fs = 360  # sampling rate: 360 readings per second

print("Number of samples:", len(ecg))
print("Duration in seconds:", len(ecg) / fs)
print("Highest reading:", ecg.max(), "mV")
print("Lowest reading:", ecg.min(), "mV")

# Time axis: reading number / readings per second = seconds
time = np.arange(len(ecg)) / fs

# ---------- 2. Clean the signal ----------
# Band-pass filter: keep heartbeat speeds (0.5–40 Hz), remove drift and jitter
b, a = butter(2, [0.5, 40], btype="bandpass", fs=fs)
ecg_clean = filtfilt(b, a, ecg)

# ---------- 3. Detect heartbeats ----------
# R-peaks: points taller than 0.5 mV, at least 0.25 s apart
peaks, _ = find_peaks(ecg_clean, height=0.5, distance=int(0.25 * fs))
print("Heartbeats detected:", len(peaks))

# ---------- 4. Heart rate ----------
# RR intervals: time between neighbouring beats, in seconds
rr = np.diff(peaks) / fs
bpm = 60 / rr
beat_times = time[peaks[1:]]

# Values outside 40–200 BPM come from missed or extra beats, not the patient
valid = (bpm >= 40) & (bpm <= 200)
bpm_valid = bpm[valid]

print("Beats rejected as detection errors:", np.sum(~valid))
print("Median heart rate:", round(np.median(bpm_valid), 1), "BPM")
print("Slowest:", round(bpm_valid.min(), 1), "BPM")
print("Fastest:", round(bpm_valid.max(), 1), "BPM")

# Save a beat-by-beat log that can be opened in Excel
log = pd.DataFrame({
    "time_s": beat_times.round(3),
    "rr_interval_s": rr.round(3),
    "heart_rate_bpm": bpm.round(1),
    "valid": valid,
})
log.to_csv("heart_rate_log.csv", index=False)

# ---------- 5. Plots ----------
# Figure 1: raw vs cleaned ECG, with detected beats
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 6), sharex=True)

ax1.plot(time, ecg)
ax1.set_title("Raw ECG - MIT-BIH Record 208")
ax1.set_ylabel("Voltage (mV)")
ax1.grid(True)

ax2.plot(time, ecg_clean, color="green")
ax2.plot(time[peaks], ecg_clean[peaks], "ro", markersize=4, label="Detected beats")
ax2.legend()
ax2.set_title("Filtered ECG (0.5–40 Hz band-pass)")
ax2.set_xlabel("Time (seconds)")
ax2.set_ylabel("Voltage (mV)")
ax2.grid(True)

ax1.set_xlim(38, 48)
plt.tight_layout()
plt.savefig("detected_beats.png", dpi=150)
plt.show()

# Figure 2: heart rate over time (tachogram)
plt.figure(figsize=(12, 4))
plt.plot(beat_times[valid], bpm_valid, marker=".", label="Heart rate")
plt.plot(beat_times[~valid], bpm[~valid], "rx", markersize=8, label="Rejected (detection error)")
plt.axhline(np.median(bpm_valid), color="gray", linestyle="--", label="Median")
plt.xlabel("Time (seconds)")
plt.ylabel("Heart rate (BPM)")
plt.title("Beat-by-beat heart rate")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("heart_rate.png", dpi=150)
plt.show()
