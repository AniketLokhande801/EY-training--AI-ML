import pika
import logging
from etl.etl_process import run_etl
# consumer.py
import sys
import os

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from etl.etl_process import run_etl


logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

QUEUE_NAME = "etl_queue"

def callback(ch, method, properties, body):
    csv_path = body.decode()
    logging.info(f"Consumer: Received {csv_path}")
    try:
        output_file, _ = run_etl(csv_path, "student_results_using_queue")
        logging.info(f"Consumer: ETL completed {output_file}")
    except Exception as e:
        logging.error(f"Consumer: Error processing {csv_path} - {e}", exc_info=True)
    ch.basic_ack(delivery_tag=method.delivery_tag)

def start_consumer():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback)
    
    logging.info(f"Consumer: Waiting for messages in queue '{QUEUE_NAME}'")
    channel.start_consuming()


