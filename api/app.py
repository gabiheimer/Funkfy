from flask import Flask, request, Response
from pydub import AudioSegment, effects
import pika
import json
import requests
import os

app = Flask(__name__)


@app.route("/")
def main():
    return {
        'message': 'Hellou world!'
    }


@app.route("/songs", methods=["POST"])
def test():
    if request.files and request.files['vocals'] and request.files['accompaniment']:
        vocals = request.files['vocals']
        accompaniment_file = request.files['accompaniment']
        url = "http://song-api:5065/songs"
        r = requests.post(url, files=request.files, headers=request.headers)

        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='rabbitmq'))
        channel = connection.channel()
        channel.queue_declare(queue='split')
        data = {
            "vocals": vocals.filename.split(".")[0],
            "vocal_speed": 1.0,
            "vocal_volume": 1.0,
            "accompaniment": accompaniment_file.filename.split(".")[0],
            "accompaniment_speed": 1.0,
            "accompaniment_valume": 1.0
        }
        channel.basic_publish(exchange='', routing_key='split',
                            body=json.dumps(data))
        print(vocals.filename.split(".")[0])
        return('', 201)
    else:
        return ('Invalid files', 400)


@app.route("/songs", methods=["PUT"])
def update_songs():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='infos', durable=True)
    data = request.json
    channel.basic_publish(
        exchange='',
        routing_key='infos',
        body=json.dumps(data),
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        )
    )
    connection.close()
    return (200)


@app.route("/song/merge", methods=['PATCH'])
def audio():
    body = request.json
    vocals = body['vocals']
    accompaniment = body['accompaniment']
    vocals_file = body['vocals_file']
    accompaniment_file = body['accompaniment_file']
    sound1 = AudioSegment.from_file('/app/api/output/' + vocals + vocals_file)
    sound2 = AudioSegment.from_file(
        '/app/api/output/' + accompaniment + accompaniment_file) - 20

    combined = sound1.overlay(sound2)

    combined.export('/app/api/merged/' + vocals + '-' +
                    accompaniment + '.mp3', format='mp3')
    return {
        'status': 'Created :D'
    }


@app.route('/song/split', methods=['PATCH'])
def split_song():
    body = request.json
    song_title = body['title']
    stems = body['stems']

    os.system('spleeter separate -i /app/api/audio/' + song_title +
              ' -p spleeter:' + str(stems) + 'stems -o /app/api/output')
    return {}


@app.route('/song', methods=['GET'])
def get_song():
    data = open('/app/api/audio/watermelon-sugar.mp3', 'rb')
    return Response(data, mimetype='audio/mp3')


@app.route('/song', methods=['POST'])
def receive_song():
    body = request.data
    newFile = open("request.mp3", "wb")
    newFileByteArray = body
    # logs = open("logs.data", "w")
    # logs.write(newFileByteArray)
    newFile.write(newFileByteArray)
    return ('', 200)


app.run()
