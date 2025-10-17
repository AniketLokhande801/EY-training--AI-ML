import pika
from Module_3.ETL_Student import run_etl
import logging
import os

logging.basicConfig(
    filename='module_4/consumer.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'

)

def callback(ch, method, properties, body):
    file_path = body.decode()
    print(f"Received file path: {file_path}")
    print(f"File exists? {os.path.exists(file_path)}")

    if os.path.exists(file_path):
        try:

            run_etl(file_path)
            print("ETL processing complete.")
            logging.info("ETL process DONE.")
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            print(f"Error during ETL: {e}")
            logging.error(e)

    else:
        print(f"File not found: {file_path}")
        logging.error("File not found.")
        ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    logging.info('connection created')

    channel.basic_qos(prefetch_count=1)
    channel.queue_declare(queue='marks_ETL_queue', durable=True)
    logging.info("Declare queue")
    channel.basic_consume(queue='marks_ETL_queue', on_message_callback=callback)
    logging.info("Consume queue")

    print("Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()

if __name__ == "__main__":
    main()
