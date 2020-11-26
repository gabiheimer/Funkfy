import pika, sys, os, json
import requests
from graph import plotGraph
import numpy
from scipy.io import wavfile
from IPython.display import Audio
import warnings

# global vars
port = ':5060'
baseUrl = 'http://song-api'+port
songType = '.mp3'

def getVocalsUrl(songName):
    return '/songs/{}/vocals'.format(songName)

def getBeatsUrl(songName):
    return '/songs/{}/accompaniment'.format(songName)

def postGraphUrl(vocalsName, beatsName):
    return '/graphs/{}/{}'.format(vocalsName, beatsName)

def getVocals(songName):
    vocalsUrl = baseUrl + getVocalsUrl(songName)
    response = requests.get(vocalsUrl)
    return response.data

def getBeats(songName):
    beatsUrl = baseUrl + getBeatsUrl(songName)
    response = requests.get(beatsUrl)
    return response.data

def speedUpVocals(songName, speed):
    fileName = './originalVocals/{}'.format(songName) + songType
    resultFileName = './spedUpVocals/{}'.format(songName) + songType
    song_data = wavfile.read(fileName)
    wavfile.write(resultFileName, int(speed*112/107), song_data)

def speedUpBeats(songName, speed):
    fileName = './originalBeats/{}'.format(songName) + songType
    resultFileName = './spedUpBeats/{}'.format(songName) + songType
    song_data = wavfile.read(fileName)
    wavfile.write(resultFileName, int(speed*112/107), song_data)

def postGraph(vocalsName, beatsName):
    graphUrl = postGraphUrl(vocalsName, beatsName)
    fileName = './graphs/{}-{}.png'.format(vocalsName, beatsName)
    files = {'file': open(fileName, 'rb')}
    response = requests.post(graphUrl, files=files)

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
        getBeats = getBeats(beatsName)

        # save vocals file
        vocalsFileName = './originalVocals/{}'.format(vocalsName) + songType
        vocalsFile = open(vocalsFileName, 'wb')
        vocalsFile.write(vocals)

        # save beats file
        beatsFileName = './originalBeats/{}'.format(beatsName) + songType
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
        graphFileName = './graphs/{}-{}'.format(vocalsName, beatsName)
        spedUpVocalsFileName = './spedUpBeats/{}'.format(vocalsName) + songType
        spedUpBeatsFileName = './spedUpBeats/{}'.format(beatsName) + songType

        os.remove(vocalsFileName)
        os.remove(beatsFileName)
        os.remove(spedUpVocalsFileName)
        os.remove(spedUpBeatsFileName)
        os.remove(graphFileName)


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
