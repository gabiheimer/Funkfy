from flask import Flask, request, Response, send_file
from flask_cors import CORS
import pika
import json
import requests
import os

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})


@app.route("/", methods=["GET"])
def hello():
	return Response('dale', 200)

@app.route("/songs", methods=["POST"])
def upload_songs():
    if request.files and request.files['vocals'] and request.files['accompaniment']:
        vocals = request.files['vocals']
        accompaniment_file = request.files['accompaniment']
        vocals.save(vocals.filename)
        accompaniment_file.save(accompaniment_file.filename)
        url = "http://song-api:5065/songs"
        vc = open(vocals.filename, 'rb')
        ac = open(accompaniment_file.filename, 'rb')
        r = requests.post(url + "/" + vocals.filename , data=vc)
        r = requests.post(url + "/" + accompaniment_file.filename, data=ac)
        os.remove(vocals.filename)
        os.remove(accompaniment_file.filename)

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
    data = request.json
    channel.basic_publish(
        exchange='',
        routing_key='infos',
        body=json.dumps(data)
    )
    connection.close()
    return Response('',201)

@app.route("/songs", methods=["PATCH"])
def merge_songs():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()
    data = request.json
    channel.basic_publish(
        exchange='',
        routing_key='merge',
        body=json.dumps(data)
    )
    connection.close()
    return Response('',200)


@app.route("/graphs/<vocals>/<accompaniment>", methods=["GET"])
def get_graph(vocals, accompaniment):
    url = "http://song-api:5065/graphs/" + vocals.replace('.mp3', '') + "/" + accompaniment.replace('.mp3', '')  # CHECK URL
    r = requests.get(url)
    if r.status_code > 400:
        return Response('', 404)
    return Response(r.content, mimetype='image/png')


@app.route("/results/<vocals>/<accompaniment>", methods=["GET"])
def get_result(vocals, accompaniment):
    url = "http://song-api:5065/songs/" + vocals + "/" + accompaniment  # CHECK URL
    r = requests.get(url)
    if r.status_code > 400:
        return Response('', 404)
    return Response(r.content, mimetype='audio/mp3')

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
