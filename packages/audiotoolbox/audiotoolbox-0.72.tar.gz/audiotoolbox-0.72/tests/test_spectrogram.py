import audiotoolbox as audio
from scipy.signal import stft
import numpy as np
import matplotlib.pyplot as plt

sig = audio.Signal(1, 1, 48000)
sig.add_tone(500)
sig.add_tone(5000)

freq, time, st = stft(sig, fs=sig.fs)

fig, ax = plt.subplots(1, 1)
plt.pcolormesh(time, freq, np.abs(st))
ax.set_ylim(20, 20000)
ax.set_yscale("log")
