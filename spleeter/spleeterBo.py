from pydub import AudioSegment
import requests, os

PATH_TO_AUDIO = '/spleeter/audio/'
PATH_TO_AUDIO_OUTPUT = '/spleeter/audio/output/'

def send_to_songs_api(vocals_path, accompaniment_path, music_name):
    """send vocals and accompaniment to songs_api"""

    url = f"http://song-api:5065/songs/{music_name}/accompaniment"
    data = open(accompaniment_path, 'rb')   
    headers = {'content-type': 'audio/mp3'}
    r = requests.post(url, data=data, headers=headers)

    url = f"http://song-api:5065/songs/{music_name}/vocals"
    data = open(vocals_path, 'rb')
    headers = {'content-type': 'audio/mp3'}
    r = requests.post(url, data=data, headers=headers)

def (PATH_TO_AUDIO, music_name):
    """get entire music from songs api"""

    url = f"http://song-api:5065/songs/{music_name}"
    r = requests.get(url, data=None, headers=None)
    
    #TODO: possivel erro abaixo
    file_name = PATH_TO_AUDIO + music_name + '.mp3'
    file_obj = open(file_name, 'wb')
    file_obj.write(r.data)

def compress(vocals_path, accompaniment_path):
    """transform wav to mp3"""
    v = AudioSegment.from_wav(vocals_path)
    v.export(vocals_path.replace('.mp3','.wav'), format='mp3')

    a = AudioSegment.from_wav(accompaniment_path)
    a.export(accompaniment_path.replace('.mp3','.wav'), format='mp3')

def split_in_two(music_name, stems = 2):
    """use spleeter and generate .wavs"""
    get_music_from_songs_api(PATH_TO_AUDIO, music_name)
    FINAL_PATH = PATH_TO_AUDIO_OUTPUT + music_name
    os.system('spleeter separate -i '+ PATH_TO_AUDIO + music_name + '.mp3' + ' -p spleeter:' + str(stems) + 'stems -o '+ FINAL_PATH)
    return (FINAL_PATH + 'vocals.wav', FINAL_PATH + 'accompaniment.wav')

def process_json(body):
    """get two musics from songs api, process them and sends the results to songs api"""
    music_name = body['vocals']
    vocals_path, accompaniment_path = split_in_two(music_name)
    compress(vocals_path, accompaniment_path)
    send_to_songs_api(vocals_path, accompaniment_path, music_name)

    music_name = body['accompaniment']
    vocals_path, accompaniment_path = split_in_two(music_name)
    compress(vocals_path, accompaniment_path)
    send_to_songs_api(vocals_path, accompaniment_path, music_name)