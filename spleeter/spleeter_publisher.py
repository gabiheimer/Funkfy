import pika, json

def send_to_info_queue(body):
    """send body back to infos queue"""
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    channel.queue_declare(queue='infos')
    data = body
    channel.basic_publish(exchange='', routing_key='split', body=json.dumps({'data': data})) # TODO: conferir esse dumps, (colocar body=body se der ruim)
    print(" [x] {body} to infos queue")
    connection.close()