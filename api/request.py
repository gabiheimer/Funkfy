import requests

url = "http://affectionate_grothendieck:3000/song"
data = open('/app/api/audio/watermelon-sugar.mp3', 'rb')   
headers = {'content-type': 'audio/mp3'}

r = requests.post(url, data=data, headers=headers)

print(r)
print(r.text)    