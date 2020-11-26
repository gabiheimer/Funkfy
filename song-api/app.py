from flask import Flask, request, Response
import os
from pathlib import Path

app = Flask(__name__)

@app.route('/graphs/<vocals>/<accompaniment>', methods=['GET'])
def get_graphs_result(vocals, accompaniment):
  my_file = Path('/song-api/files/graphs/' + vocals.replace('.mp3','') + accompaniment.replace('.mp3','') + '.png')
  if my_file.is_file():
    song = open('/song-api/files/graphs/' + vocals.replace('.mp3','') + accompaniment.replace('.mp3','') + '.png', 'rb')
    return Response(song, mimetype='image/png')
  else:
    return Response('', 404)

@app.route('/graphs/<vocals>/<accompaniment>', methods=['POST'])
def receive_graphs_result(vocals, accompaniment):
  song = request.data
  my_file = Path("/song-api/files/graphs/" + vocals.replace('.mp3','') + accompaniment.replace('.mp3','') + '.png')
  if my_file.is_file():
    os.remove("/song-api/files/graphs/" + vocals.replace('.mp3','') + accompaniment.replace('.mp3','') + '.png')
  os.makedirs(os.path.dirname("/song-api/files/graphs/" + vocals.replace('.mp3','') + accompaniment.replace('.mp3','') + '.png'), exist_ok=True)
  newFile = open("/song-api/files/graphs/" + vocals.replace('.mp3','') + accompaniment.replace('.mp3','') + '.png', "wb")
  newFile.write(song)
  return('', 201)

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
  song = open('/song-api/files/songs/' + vocals.replace('.mp3','') + accompaniment.replace('.mp3',''), 'rb')
  return Response(song, mimetype='audio/mp3')

# @app.route('/songs', methods=['POST'])
# def receive_song():
#   vocals = request.files['vocals']
#   song = open('./oi', 'wt')
#   song.write('oi!')
#   vocals.save('./vocals.mp3')
#   accompaniment_file = request.files['accompaniment']
#   vocals_path = "/song-api/files/" + vocals.filename.replace('.mp3','') + "/song.mp3"
#   accompaniment_path = "/song-api/files/" + accompaniment_file.filename.replace('.mp3','') + "/song.mp3"
#   os.makedirs(os.path.dirname(vocals_path), exist_ok=True)
#   os.makedirs(os.path.dirname(accompaniment_path), exist_ok=True)
#   vocals.save(vocals_path)
#   vocals.save('./teste.mp3')
#   accompaniment_file.save(accompaniment_path)
#   return Response('', 201)


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
  filename = "/song-api/files/songs/" + vocals.replace('.mp3','') + accompaniment.replace('.mp3','')
  os.makedirs(os.path.dirname(filename), exist_ok=True)
  newFile = open(filename, "wb")
  newFile.write(song)
  return('', 201)

def save_song(song, title, part):
  filename = "/song-api/files/" + title.replace('.mp3','') + "/" + part + ".mp3"
  os.makedirs(os.path.dirname(filename), exist_ok=True)
  newFile = open(filename, "wb")
  newFile.write(song)
  return('', 201)

def open_song(title, part):
  filename = '/song-api/files/' + title.replace('.mp3','') + '/' + part + '.mp3'
  return open(filename, 'rb')
