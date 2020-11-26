import pika, sys, os, json, requests
import pydub
import numpy as np

baseUrl = "http://song-api:5065" 

def get_vocal_url(songName):
  return baseUrl + '/songs/{}/vocals'.format(songName)

def get_accompaniment_url(songName):
  return baseUrl + '/songs/{}/accompaniment'.format(songName)

def get_merge_url(songName,accompaniment):
  return baseUrl + "/songs/{}/{}".format(songName,accompaniment)

def getVocals(songName):
    vocalsUrl = get_vocal_url(songName)
    response = requests.get(vocalsUrl)
    return response.content

def getBeats(songName):
    beatsUrl = get_accompaniment_url(songName)
    response = requests.get(beatsUrl)
    return response.content

def read(f, normalized=False):
    """MP3 to numpy array"""
    a = pydub.AudioSegment.from_mp3(f)
    y = np.array(a.get_array_of_samples())
    if a.channels == 2:
        y = y.reshape((-1, 2))
    if normalized:
        return a.frame_rate, np.float32(y) / 2**15
    else:
        return a.frame_rate, y

def write(sr, x, normalized=False):
    """numpy array to MP3"""
    channels = 2 if (x.ndim == 2 and x.shape[1] == 2) else 1
    if normalized:  # normalized array - each item should be a float in [-1, 1)
        y = np.int16(x * 2 ** 15)
    else:
        y = np.int16(x)
    return pydub.AudioSegment(y.tobytes(), frame_rate=sr, sample_width=2, channels=channels)

# Salvar música merge
def merge(ch, method, properties, body):
  oi = json.loads(body)
  vocal_music_name = oi['vocals']
  vocal_speed = oi['vocal_speed']
  vocal_volume = oi['vocal_volume']
  accompaniment_music_name = oi['accompaniment']
  accompaniment_speed = oi['accompaniment_speed']
  accompaniment_volume = oi['accompaniment_volume']
  
  sound1 =  requests.get(get_vocal_url(vocal_music_name))
  fileSound1 = open("/merge/" + vocal_music_name  + ".mp3", "wb") 
  fileSound1.write(sound1.content)

  sound2 =  requests.get(get_accompaniment_url(accompaniment_music_name))
  fileSound2 = open("/merge/" + accompaniment_music_name  + ".mp3", "wb")
  fileSound2.write(sound2.content)

  vsr, vx = read("/merge/" + vocal_music_name  + ".mp3")
  asr, ax = read("/merge/" + accompaniment_music_name  + ".mp3")
  song1 = write(int(vsr*vocal_speed), vx)
  song2 = write(int(asr*accompaniment_speed), ax)

  combined = song1.overlay(song2)
  combined.export('/merge/merged.mp3', format="mp3", bitrate="320k")

  print("TALVES ERRO DE PATH AQUI")
  data = open('/merge/merged.mp3', 'rb')
  headers = {'content-type': 'audio/mp3'}
  url = get_merge_url(vocal_music_name, accompaniment_music_name)
  r = requests.post(url, data=data, headers=headers)
  print(r.content)
  os.remove('/merge/merged.mp3')

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    channel.queue_declare(queue='merge')

    channel.basic_consume(queue='merge', on_message_callback=merge, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
