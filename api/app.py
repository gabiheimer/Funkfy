from flask import Flask
from pydub import AudioSegment

app = Flask(__name__)

@app.route("/")
def main():
    return {
      'message': 'Hellou world!'
    }

@app.route("/audio")
def audio():
  sound1 = AudioSegment.from_file("/app/acucar-de-melancia-mto-doido copy.mp3")
  sound2 = AudioSegment.from_file("/app/teste.mp3")

  combined = sound1.overlay(sound2)

  combined.export("/app/combined.wav", format='wav')