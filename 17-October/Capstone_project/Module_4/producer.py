import pika
import logging

logging.basicConfig(
    filename='Module_4/Producer.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
def send_file_path(file_path):
    logging.info('connection created Send file path: %s', file_path)
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='marks_ETL_queue', durable=True)
    logging.info("Declare queue")
    channel.basic_publish(
        exchange='',
        routing_key='marks_ETL_queue',
        body=file_path)
    logging.info("Send file to queue")
    print(f"Sent file path to queue: {file_path}")

    connection.close()
    logging.info("Connection closed")

if __name__ == "__main__":
    send_file_path("C:\\Users\\user3\\PycharmProjects\\06-October\\EY-training--AI-ML\\17-October\\Capstone_project\\Module_4\\marks.csv")
