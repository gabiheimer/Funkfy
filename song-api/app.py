from flask import Flask, request, Response
import os

app = Flask(__name__)

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