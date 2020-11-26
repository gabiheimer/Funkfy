from flask import Flask, request, Response
import os

app = Flask(__name__)

@app.route('/songs/<title>', methods=['GET'])
def get_song(title):
  song = open_song(title, 'song')
  return Response(song, mimetype='audio/mp3')

@app.route('/songs/<title>/vocals', methods=['GET'])
def get_song(title):
  song = open_song(title, 'vocals')
  return Response(song, mimetype='audio/mp3')

@app.route('/songs/<title>/accompaniment', methods=['GET'])
def get_song(title):
  song = open_song(title, 'accompaniment')
  return Response(song, mimetype='audio/mp3')

@app.route('/songs/<title>/result', methods=['GET'])
def get_song(title):
  song = open_song(title, 'result')
  return Response(song, mimetype='audio/mp3')

@app.route('/songs/<title>', methods=['POST'])
def receive_song(title):
  song = request.data
  return save_song(title, 'song')

@app.route('/songs/<title>/vocals', methods=['POST'])
def receive_song_vocals(title):
  song = request.data
  return save_song(title, 'vocals')

@app.route('/songs/<title>/accompaniment', methods=['POST'])
def receive_song_accompaniment(title):
  song = request.data
  return save_song(title, 'accompaniment')

@app.route('/songs/<title>/result', methods=['POST'])
def receive_song_result(title):
  song = request.data
  return save_song(title, 'result')

def save_song(title, part):
  song = request.data
  newFile = open("/song-api/" + title + "/" + part + ".mp3", "wb")
  newFile.write(song)
  return('', 201)

def open_song(title, part):
  return open('/song-api/' + title + '/' + part + '.mp3', 'rb')
