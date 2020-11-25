from pydub import AudioSegment, effects
import io

sound1 =  AudioSegment.from_file('/app/api/audio/toxic.mp3')
watermelon =  AudioSegment.from_file('/app/api/audio/watermelon-sugar.mp3')
audio = watermelon.get_array_of_samples()
# print(sound1.get_array_of_samples())

wow = sound1._spawn(audio)
audio.export('dale.mp3', format='mp3')
