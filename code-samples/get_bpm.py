# Beat tracking example
import librosa
import matplotlib.pyplot as plt


# 1. Get the file path to an included audio example
#filename = librosa.example('nutcracker')


# 2. Load the audio as a waveform y
#    Store the sampling rate as sr
y, sr = librosa.load('./output/recairei/vocals.wav')
y2, sr2 = librosa.load('./output/funk/accompaniment.wav')
y3, sr3 = librosa.load('./audio/recairei.mp3')
y4, sr4 = librosa.load('./audio/funk.mp3')

# 3. Run the default beat tracker
tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
tempo2, _ = librosa.beat.beat_track(y=y2, sr=sr2)
tempo3, _ = librosa.beat.beat_track(y=y3, sr=sr3)
tempo4, _ = librosa.beat.beat_track(y=y4, sr=sr4)

print('Estimated tempo vocals: {:.2f} beats per minute'.format(tempo))
print('Estimated tempo accompaniment: {:.2f} beats per minute'.format(tempo2))
print('Estimated tempo watermelon: {:.2f} beats per minute'.format(tempo3))
print('Estimated tempo funk: {:.2f} beats per minute'.format(tempo4))

# 4. Convert the frame indices of beat events into timestamps
# beat_times = librosa.frames_to_time(beat_frames, sr=sr)
# print(beat_times)