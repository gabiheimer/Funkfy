import pika, sys, os, json
import requests
from graph import plotGraph
import numpy
import numpy as np
from scipy.io import wavfile
from IPython.display import Audio
import warnings
import pydub

# global vars
port = ':5065'
baseUrl = 'http://song-api'+port
songType = '.mp3'

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

def write(f, sr, x, normalized=False):
    """numpy array to MP3"""
    channels = 2 if (x.ndim == 2 and x.shape[1] == 2) else 1
    if normalized:  # normalized array - each item should be a float in [-1, 1)
        y = np.int16(x * 2 ** 15)
    else:
        y = np.int16(x)
    song = pydub.AudioSegment(y.tobytes(), frame_rate=sr, sample_width=2, channels=channels)
    song.export(f, format="mp3", bitrate="320k")

def getVocalsUrl(songName):
    return '/songs/{}/vocals'.format(songName)

def getBeatsUrl(songName):
    return '/songs/{}/accompaniment'.format(songName)

def postGraphUrl(vocalsName, beatsName):
    return '/graphs/{}/{}'.format(vocalsName, beatsName)

def getVocals(songName):
    vocalsUrl = baseUrl + getVocalsUrl(songName)
    response = requests.get(vocalsUrl)
    return response.content

def getBeats(songName):
    beatsUrl = baseUrl + getBeatsUrl(songName)
    response = requests.get(beatsUrl)
    return response.content

def speedUpVocals(songName, speed):
    fileName = './originalVocals/{}'.format(songName) + songType
    resultFileName = './spedUpVocals/{}'.format(songName) + songType
    os.makedirs(os.path.dirname(resultFileName), exist_ok=True)
    sr, x = read(fileName)
    write(resultFileName, int(sr*speed), x)

def speedUpBeats(songName, speed):
    fileName = './originalBeats/{}'.format(songName) + songType
    resultFileName = './spedUpBeats/{}'.format(songName) + songType
    os.makedirs(os.path.dirname(resultFileName), exist_ok=True) 
    sr, x = read(fileName)
    write(resultFileName, int(sr*speed), x)

def postGraph(vocalsName, beatsName):
    graphUrl = postGraphUrl(vocalsName, beatsName)
    fileName = './graphs/{}-{}.png'.format(vocalsName, beatsName)
    files = open(fileName, 'rb')
    response = requests.post(baseUrl + graphUrl, data=files)

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    channel.queue_declare(queue='infos')

    def callback(ch, method, properties, bodyStr):
        body = json.loads(bodyStr)
        vocalsName = body['vocals']
        beatsName = body['accompaniment']
        vocalsSpeed = body['vocal_speed']
        beatsSpeed = body['accompaniment_speed']

        # get song files
        vocals = getVocals(vocalsName)
        beats = getBeats(beatsName)

        # save vocals file
        vocalsFileName = './originalVocals/{}'.format(vocalsName) + songType
        os.makedirs(os.path.dirname(vocalsFileName), exist_ok=True)
        vocalsFile = open(vocalsFileName, 'wb')
        vocalsFile.write(vocals)

        # save beats file
        beatsFileName = './originalBeats/{}'.format(beatsName) + songType
        os.makedirs(os.path.dirname(beatsFileName), exist_ok=True)
        beatsFile = open(beatsFileName, 'wb')
        beatsFile.write(beats)

        # speed up vocals and beats
        speedUpVocals(vocalsName, vocalsSpeed)
        speedUpBeats(beatsName, beatsSpeed)

        # plot graph
        plotGraph(vocalsName, beatsName)

        # send graph to api
        postGraph(vocalsName, beatsName)

        # delete saved data
        graphFileName = './graphs/{}-{}'.format(vocalsName, beatsName) + '.png'
        spedUpVocalsFileName = './spedUpVocals/{}'.format(vocalsName) + songType
        spedUpBeatsFileName = './spedUpBeats/{}'.format(beatsName) + songType
        os.makedirs(os.path.dirname(graphFileName), exist_ok=True)

        os.remove(vocalsFileName)
        os.remove(beatsFileName)
        os.remove(spedUpVocalsFileName)
        os.remove(spedUpBeatsFileName)
        # os.remove(graphFileName)


    channel.basic_consume(queue='infos', on_message_callback=callback, auto_ack=True)
        #coisas q vou fazer

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
