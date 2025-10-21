import pika
import logging

logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

def send_csv_to_queue(csv_path: str, queue_name: str = "etl_queue"):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue=queue_name, durable=True)
        
        channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            body=csv_path,
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
            )
        )
        logging.info(f"Producer: Sent {csv_path} to queue '{queue_name}'")
        connection.close()
    except Exception as e:
        logging.error(f"Producer: Error sending {csv_path} to queue - {e}", exc_info=True)
