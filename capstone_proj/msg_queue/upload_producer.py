import pika
import logging

QUEUE_NAME = "marks_upload_queue"

logging.basicConfig(
    filename="logs/upload_producer.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

def send_csv_to_queue(file_path: str):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
        channel = connection.channel()
        channel.queue_declare(queue=QUEUE_NAME, durable=True)

        channel.basic_publish(
            exchange="",
            routing_key=QUEUE_NAME,
            body=file_path,
            properties=pika.BasicProperties(delivery_mode=2)  # make message persistent
        )

        logging.info(f"Producer: Sent {file_path} to queue {QUEUE_NAME}")
        connection.close()
    except Exception as e:
        logging.error(f"Producer error: {e}", exc_info=True)
        raise e
