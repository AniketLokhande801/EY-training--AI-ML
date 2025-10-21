import pika
import pandas as pd
import logging
import os
from etl.etl_process import run_etl
from DB.database import get_connection

# ---------------- Logging Setup ----------------
logging.basicConfig(
    filename='logs/upload_consumer.log',
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'
)

QUEUE_NAME = "marks_upload_queue"

# ---------------- Database Update ----------------
def update_students_table(df):
    """
    Update MySQL students table with ETL results.
    Assumes columns Maths, Python, ML, TotalMarks, Percentage, Result exist.
    """
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        for _, row in df.iterrows():
            cursor.execute("""
                UPDATE students
                SET Maths = %s,
                    Python = %s,
                    ML = %s,
                    TotalMarks = %s,
                    Percentage = %s,
                    Result = %s
                WHERE StudentID = %s
            """, (
                int(row["Maths"]), int(row["Python"]), int(row["ML"]),
                int(row["TotalMarks"]), float(row["Percentage"]), row["Result"],
                int(row["StudentID"])
            ))

        conn.commit()
        logging.info("Database updated successfully from uploaded CSV")
        print("Database updated successfully from uploaded CSV")

    except Exception as e:
        logging.error(f"DB update failed: {e}", exc_info=True)
        print(f"DB update failed: {e}")
    finally:
        if conn:
            conn.close()

# ---------------- RabbitMQ Callback ----------------
def callback(ch, method, properties, body):
    file_path = body.decode()
    logging.info(f"Received file path from queue: {file_path}")
    print(f"Received file path: {file_path}")

    if os.path.exists(file_path):
        try:
            # Run ETL
            output_file, df = run_etl(file_path, output_prefix="student_upload")
            logging.info(f"ETL completed: {output_file}")
            print(f"ETL completed: {output_file}")

            # Update database
            update_students_table(df)

            # Acknowledge message
            ch.basic_ack(delivery_tag=method.delivery_tag)
            logging.info("Message acknowledged")
        except Exception as e:
            logging.error(f"Error during ETL or DB update: {e}", exc_info=True)
            print(f"Error during ETL or DB update: {e}")
            # Do not ack to allow retry
    else:
        logging.error(f"File not found: {file_path}")
        print(f"File not found: {file_path}")
        ch.basic_ack(delivery_tag=method.delivery_tag)

# ---------------- Start Consumer ----------------
def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback)

    logging.info(f"Consumer waiting for messages on queue '{QUEUE_NAME}'")
    print(f"Waiting for messages on queue '{QUEUE_NAME}'... Press CTRL+C to exit.")
    channel.start_consuming()

if __name__ == "__main__":
    main()
