import pika, sys, os, json

baseUrl = "http://song-api:5065/" 

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
  channel.queue_declare(queue='merge')

  def callback(ch, method, properties, body):
    oi = json.loads(body)
    vocals_file = oi['vocals']
    vocal_speed = oi['vocal_speed']
    vocal_volume = oi['vocal_volume']
    accompaniment_file = oi['accompaniment']
    accompaniment_speed = oi['accompaniment_speed']
    accompaniment_volume = oi['accompaniment_volume']

  channel.basic_consume(queue='merge', on_message_callback=callback, auto_ack=True)

  print(' [*] Waiting for messages. To exit press CTRL+C')
  channel.start_consuming()

if __name__ == '__main__':
  print('hai')
  main()
print('oi', __name__)