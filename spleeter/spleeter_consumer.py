import pika, sys, os, json
from spleeterBo import process_json
from spleeter_publisher import send_to_info_queue

def start_consumer():
    """start split queue"""
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    channel.queue_declare(queue='split')

    def callback(ch, method, properties, body):
        json_as_dict = json.loads(body)
        process_json(json_as_dict)
        send_to_info_queue(body)
    
    channel.basic_consume(queue='split', on_message_callback=callback, auto_ack=True)
    print(' [*] Split Queue is active???')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        start_consumer()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
