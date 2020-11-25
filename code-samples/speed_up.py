import numpy
from scipy.io import wavfile
from IPython.display import Audio
import warnings

speech_rate, speech_data = wavfile.read('./output/funk/accompaniment.wav')

wavfile.write('./fast/accompaniment.wav', int(speech_rate*112/107), speech_data)

# Estimated tempo vocals: 123.05 beats per minute
# Estimated tempo accompaniment: 112.35 beats per minute
# Estimated tempo watermelon: 95.70 beats per minute
# Estimated tempo funk: 86.13 beats per minute
