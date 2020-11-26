import pika, sys, os, json, requests

baseUrl = "http://song-api:5065/" 

def get_vocal_url(songName):
  return baseUrl + '/songs/{}/vocals'.format(songName)

def get_accompaniment_url(songName):
  return baseUrl + '/songs/{}/accompaniment'.format(songName)

def get_merge_url(songName,accompaniment):
  return baseUrl + "songs/{}/{}".format(songName,accompaniment)

# Salvar música merge
def merge(vocal_music_name, accompaniment_music_name):
  url = get_merge_url(vocal_music_name, accompaniment_music_name)
  
  sound1 =  requests.get(get_vocal_url(vocal_music_name))
  print("POSSIVL ERRO AQUI")
  fileSound1 = open("/song-api/" + vocal_music_name  + ".mp3", "wb") 
  fileSound1.write(sound1.content)

  sound2 =  requests.get(get_accompaniment_url(accompaniment_music_name))
  print("POSSIVL ERRO AQUI")
  fileSound2 = open("/song-api/" + accompaniment_music_name  + ".mp3", "wb")
  fileSound2.write(sound2.content)

  combined = fileSound1.overlay(fileSound2)


  MERGED_PATH = '/app/api/merged/' + vocal_music_name + '-' + accompaniment_music_name + '.mp3'
  combined.export(MERGED_PATH, format='mp3')

  print("TALVES ERRO DE PATH AQUI")
  data = open(MERGED_PATH, 'rb')
  headers = {'content-type': 'audio/mp3'}
  r = requests.post(url, data=data, headers=headers)
  print(r.content)
  os.remove(MERGED_PATH)
  return {
    'status': 'Merged :D'
  }
