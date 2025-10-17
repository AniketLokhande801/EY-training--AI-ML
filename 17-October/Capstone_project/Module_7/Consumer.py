import pika
import pandas as pd
import logging
import os
import mysql.connector
from Module_3.ETL_Student import run_etl  # Your ETL function

logging.basicConfig(
    filename='Module_4/consumer.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def update_students_table(df):
    conn = None
    try:
        print("Connecting to MySQL database...")
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",
            database="student_capstone",
            use_pure=True
        )
        cursor = conn.cursor()
        print("Connected to database.")

        # No ALTER TABLE here — columns assumed to exist

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
        print("Database updated successfully.")
        logging.info("Database updated successfully.")

    except Exception as e:
        print(f"Error updating DB: {e}")
        logging.error(f"DB update failed: {e}")

    finally:
        if conn:
            conn.close()


def callback(ch, method, properties, body):
    file_path = body.decode()
    print(f"Received file path: {file_path}")
    logging.info(f"Received file path from queue: {file_path}")

    if os.path.exists(file_path):
        try:
            print("Starting ETL...")
            df = run_etl(file_path)  # ETL returns DataFrame
            print("ETL done, updating database...")
            update_students_table(df)
            print("Database update complete. Sending acknowledgment to queue.")
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            print(f"Error during ETL or DB update: {e}")
            logging.error(f"Error during ETL or DB update: {e}")
            # You may choose NOT to ack here so message retries
    else:
        print(f"File not found: {file_path}")
        logging.error(f"File not found: {file_path}")
        ch.basic_ack(delivery_tag=method.delivery_tag)


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='marks_ETL_queue', durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='marks_ETL_queue', on_message_callback=callback)

    logging.info("Consumer waiting for messages...")
    print("Waiting for messages... Press CTRL+C to exit.")
    channel.start_consuming()


if __name__ == "__main__":
    main()
