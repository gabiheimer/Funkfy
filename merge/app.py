from flask import Flask, request, Response
import pika, sys, os

app = Flask(__name__)

port = 5080
baseUrl = "http://song-api/" 

def get_vocal_url():
  return baseUrl+ "songs/:nomeDaMusica/vocals/"+port

def get_accompaniment_url():
  return baseUrl+ "songs/:nomeDaMusica/:nomeDoAcompanhamento"+port

def get_merge_url():
  return baseUrl+ "songs/:nomeDaMusica/result"+port

# Salvar música merge
def audio():
  url = get_merge_url
  body = request.json

  sound1 =  request.get(get_vocal_url, headers=headers)
  fileSound1 = open("/song-api/" + title + "/" + part + ".mp3", "wb")
  fileSound1.write(sound1)

  sound2 =  request.get(get_accompaniment_url, headers=headers) - 20
  fileSound2 = open("/song-api/" + title + "/" + part + ".mp3", "wb")
  fileSound2.write(sound2)

  combined = fileSound1.overlay(fileSound2)

  combined.export('/app/api/merged/' + vocals + '-' + accompaniment + '.mp3', format='mp3')
  return {
    'status': 'Merged :D'
  }

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    channel.queue_declare(queue='split')

    def callback(ch, method, properties, body):
      newFile = open("request.mp3", "wb")
      newFile.write(body["vocals"])

    channel.basic_consume(queue='split', on_message_callback=callback, auto_ack=True)

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