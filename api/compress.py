from pydub import AudioSegment

a = AudioSegment.from_wav("/app/api/output/watermelon-sugar/accompaniment.wav")
v = AudioSegment.from_wav("/app/api/output/watermelon-sugar/vocals.wav")

a.export('/app/api/ws-a.mp3', format='mp3')
v.export('/app/api/ws-v.mp3', format='mp3')