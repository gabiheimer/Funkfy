from flask import Flask, request, Response
import os

app = Flask(__name__)

@app.route('/songs/<title>', methods=['GET'])
def get_song(title):
  song = open_song(title, 'song')
  return Response(song, mimetype='audio/mp3')

@app.route('/songs/<title>/vocals', methods=['GET'])
def get_song_vocals(title):
  song = open_song(title, 'vocals')
  return Response(song, mimetype='audio/mp3')

@app.route('/songs/<title>/accompaniment', methods=['GET'])
def get_song_accompaniment(title):
  song = open_song(title, 'accompaniment')
  return Response(song, mimetype='audio/mp3')

@app.route('/songs/<vocals>/<accompaniment>', methods=['GET'])
def get_song_result(vocals, accompaniment):
  song = open('/song-api/' + vocals + accompaniment, 'rb')
  return Response(song, mimetype='audio/mp3')

@app.route('/songs/<title>', methods=['POST'])
def receive_song(title):
  song = request.data
  return save_song(song, title, 'song')

@app.route('/songs/<title>/vocals', methods=['POST'])
def receive_song_vocals(title):
  song = request.data
  return save_song(song, title, 'vocals')

@app.route('/songs/<title>/accompaniment', methods=['POST'])
def receive_song_accompaniment(title):
  song = request.data
  return save_song(song, title, 'accompaniment')

@app.route('/songs/<vocals>/<accompaniment>', methods=['POST'])
def receive_song_result(vocals, accompaniment):
  song = request.data
  newFile = open("/song-api/" + vocals + accompaniment, "wb")
  newFile.write(song)
  return('', 201)

def save_song(song, title, part):
  newFile = open("/song-api/" + title + "/" + part + ".mp3", "wb")
  newFile.write(song)
  return('', 201)

def open_song(title, part):
  return open('/song-api/' + title + '/' + part + '.mp3', 'rb')
