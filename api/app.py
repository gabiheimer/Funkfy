from flask import Flask, request
from pydub import AudioSegment, effects
import os

app = Flask(__name__)

@app.route("/")
def main():
    return {
      'message': 'Hellou world!'
    }

@app.route("/song/merge", methods=['PATCH'])
def audio():
  body = request.json
  vocals = body['vocals']
  accompaniment = body['accompaniment']
  sound1 =  AudioSegment.from_file('/app/api/output/' + vocals + '/vocals.wav')
  sound2 = AudioSegment.from_file('/app/api/output/' + accompaniment + '/accompaniment.wav') - 8

  combined = sound1.overlay(sound2)

  combined.export('/app/api/merged/' + vocals + '-' + accompaniment + '.mp3', format='mp3')
  return {
    'status': 'Created :D'
  }

@app.route('/song/split', methods=['PATCH'])
def split_song():
  body = request.json
  song_title = body['title']
  stems = body['stems']

  os.system('spleeter separate -i /app/api/audio/' + song_title + ' -p spleeter:' + str(stems) + 'stems -o /app/api/output')
  return {}