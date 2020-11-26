import matplotlib.pyplot as plt
import librosa
import librosa.display
import numpy as np
import os, time

def plotGraph(vocalsName, beatsName):
    vocalsFile = './spedUpVocals/{}'.format(vocalsName) + '.mp3'
    beatsFile = './spedUpBeats/{}'.format(beatsName) + '.mp3'

    # Compute local onset autocorrelation
    # y, sr = librosa.load('./output/funk/accompaniment.wav', duration=60)
    # musica1
    y, sr = librosa.load(vocalsFile, duration=60)
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

    fig, ax = plt.subplots(nrows=1, figsize=(120, 15))
    times = librosa.times_like(oenv, sr=sr, hop_length=hop_length)
    # ax.plot(times, oenv, label='Onset strength')
    ax.plot(times, oenv, label='Vocal')
    ax.label_outer()
    ax.legend(frameon=True)

    # y, sr = librosa.load('./output/recairei/vocals.wav', duration=60)
    # musica2
    y, sr = librosa.load(beatsFile, duration=60)
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
    ax.plot(times, oenv, 'C2',label='Accompaniment')
    # ax.plot(times, oenv, 'C2',label='Onset strength')
    ax.label_outer()
    ax.legend(frameon=True)

    graphFileName = './graphs/{}-{}'.format(vocalsName, beatsName)
    os.makedirs(os.path.dirname(graphFileName), exist_ok=True)
    plt.savefig(graphFileName)
    plt.close()