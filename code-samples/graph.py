import matplotlib.pyplot as plt
import librosa
import librosa.display
import numpy as np
# Compute local onset autocorrelation
# y, sr = librosa.load('./output/funk/accompaniment.wav', duration=60)
y, sr = librosa.load('./ws-a.mp3', duration=60)
hop_length = 512
oenv = librosa.onset.onset_strength(y=y, sr=sr, hop_length=hop_length)
tempogram = librosa.feature.tempogram(onset_envelope=oenv, sr=sr,
                                      hop_length=hop_length)
# Compute global onset autocorrelation
ac_global = librosa.autocorrelate(oenv, max_size=tempogram.shape[0])
ac_global = librosa.util.normalize(ac_global)
# Estimate the global tempo for display purposes
tempo = librosa.beat.tempo(onset_envelope=oenv, sr=sr,
                           hop_length=hop_length)[0]

fig, ax = plt.subplots(nrows=1, figsize=(40, 15))
times = librosa.times_like(oenv, sr=sr, hop_length=hop_length)
ax.plot(times, oenv, label='Onset strength')
ax.plot(times, oenv, label='Onset strength')
ax.label_outer()
ax.legend(frameon=True)

# y, sr = librosa.load('./output/recairei/vocals.wav', duration=60)
y, sr = librosa.load('./ws-v.mp3', duration=60)
hop_length = 512
oenv = librosa.onset.onset_strength(y=y, sr=sr, hop_length=hop_length)
tempogram = librosa.feature.tempogram(onset_envelope=oenv, sr=sr,
                                      hop_length=hop_length)
# Compute global onset autocorrelation
ac_global = librosa.autocorrelate(oenv, max_size=tempogram.shape[0])
ac_global = librosa.util.normalize(ac_global)
# Estimate the global tempo for display purposes
tempo = librosa.beat.tempo(onset_envelope=oenv, sr=sr,
                           hop_length=hop_length)[0]

times = librosa.times_like(oenv, sr=sr, hop_length=hop_length)
ax.plot(times, oenv, 'C2',label='Onset strength')
ax.plot(times, oenv, 'C2',label='Onset strength')
ax.label_outer()
ax.legend(frameon=True)




# librosa.display.specshow(tempogram, sr=sr, hop_length=hop_length,
#                          x_axis='time', y_axis='tempo', cmap='magma',
#                          ax=ax[1])
# ax[1].axhline(tempo, color='w', linestyle='--', alpha=1,
#             label='Estimated tempo={:g}'.format(tempo))
# ax[1].legend(loc='upper right')
# ax[1].set(title='Tempogram')


# x = np.linspace(0, tempogram.shape[0] * float(hop_length) / sr,
#                 num=tempogram.shape[0])
# ax[2].plot(x, np.mean(tempogram, axis=1), label='Mean local autocorrelation')
# ax[2].plot(x, ac_global, '--', alpha=0.75, label='Global autocorrelation')
# ax[2].set(xlabel='Lag (seconds)')
# ax[2].legend(frameon=True)
# freqs = librosa.tempo_frequencies(tempogram.shape[0], hop_length=hop_length, sr=sr)
# ax[3].semilogx(freqs[1:], np.mean(tempogram[1:], axis=1),
#              label='Mean local autocorrelation', basex=2)
# ax[3].semilogx(freqs[1:], ac_global[1:], '--', alpha=0.75,
#              label='Global autocorrelation', basex=2)
# ax[3].axvline(tempo, color='black', linestyle='--', alpha=.8,
#             label='Estimated tempo={:g}'.format(tempo))
# ax[3].legend(frameon=True)
# ax[3].set(xlabel='BPM')
# ax[3].grid(True)
plt.savefig('./graph/teste.png')