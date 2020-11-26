from flask import Flask, request, Response
from flask_cors import CORS
import pika
import json
import requests
import os

app = Flask(__name__)
CORS(app)


@app.route("/", methods=["GET"])
def hello():
	return Response('dale', 200)

@app.route("/songs", methods=["POST"])
def upload_songs():
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
        return(vocals.filename.split(".")[0], 201)
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
        body=json.dumps(data)
    )
    connection.close()
    return (201)


@app.route("/graphs/<vocals>/<accompaniment>", methods=["GET"])
def get_graph(vocals, accompaniment):
    url = "http://song-api:5065/graphs/" + vocals.replace('.mp3', '') + "/" + accompaniment.replace('.mp3', '')  # CHECK URL
    r = requests.get(url)
    if r.status_code > 400:
        return Response('', 404)
    return r.content


@app.route("/result", methods=["get"])
def get_result():
    url = "http://song-api:5065/graphs"  # CHECK URL
    r = requests.get(url, body=request.body, headers=request.headers)
    return r.content

@app.route('/song', methods=['GET'])
def get_song():
    data = open('/app/api/audio/watermelon-sugar.mp3', 'rb')
    return Response(data, mimetype='audio/mp3')


@app.route('/song', methods=['POST'])
def receive_song():
    body = request.data
    newFile = open("request.mp3", "wb")
    newFileByteArray = body
    newFile.write(newFileByteArray)
    return ('', 200)
