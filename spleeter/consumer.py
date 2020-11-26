import pika, sys, os, json
from pydub import AudioSegment
import requests

PATH_TO_AUDIO = '/spleeter/audio/'
PATH_TO_AUDIO_OUTPUT = '/spleeter/audio/output/'

def send_to_songs_api(vocals_path, accompaniment_path, music_name):
    """send vocals and accompaniment to songs_api"""

    url = f"/songs/{music_name}/accompaniment" #TODO: conferir
    data = open(accompaniment_path, 'rb')   
    headers = {'content-type': 'audio/mp3'}
    r = requests.post(url, data=data, headers=headers)

    url = f"/songs/{music_name}/vocals" #TODO: conferir
    data = open(vocals_path, 'rb')
    headers = {'content-type': 'audio/mp3'}
    r = requests.post(url, data=data, headers=headers)


def get_music_from_songs_api(PATH_TO_AUDIO, music_name):
    """get entire music from songs api"""

    url = f"/songs/{music_name}"
    headers = {'content-type': 'audio/mp3'}
    r = requests.get(url, data=None, headers=headers)
    #TODO: save at PATH_TO_AUDIO+music_name + '.mp3'
    
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

def send_to_info_queue(body):
    """send body back to infos queue"""
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    channel.queue_declare(queue='infos')
    data = body
    channel.basic_publish(exchange='', routing_key='split', body=json.dumps({'data': data})) # TODO: conferir esse dumps, (colocar body=body se der ruim)
    print(" [x] {body} to infos queue")
    connection.close()

def start_consumer():
    """start split queue"""
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    channel.queue_declare(queue='split')

    def callback(ch, method, properties, body):
      json_as_dict = json.loads(body)
      process_json(json_as_dict)
      send_to_info_queue(body)
    
    channel.basic_consume(queue='split', on_message_callback=callback, auto_ack=True)
    print(' [*] Split Queue is active???')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        start_consumer()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
