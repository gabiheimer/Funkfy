import pika
import json

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='rabbitmq'))
channel = connection.channel()

channel.queue_declare(queue='split')
# data = open('/processor/watermelon-sugar.mp3', 'rb') 
data = 'Oie!!'
channel.basic_publish(exchange='', routing_key='split', body=json.dumps({'data': data}))
print(" [x] Sent 'Hello World!'")
connection.close()
