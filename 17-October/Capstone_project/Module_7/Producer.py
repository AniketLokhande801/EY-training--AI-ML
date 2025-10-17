from fastapi import FastAPI, UploadFile, File
import shutil
import os
import pika

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def send_to_queue(file_path):
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()
    channel.queue_declare(queue="marks_ETL_queue", durable=True)
    channel.basic_publish(
        exchange="",
        routing_key="marks_ETL_queue",
        body=file_path
    )
    connection.close()


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        file_location = os.path.join(UPLOAD_DIR, file.filename)

        with open(file_location, "wb") as f:
            shutil.copyfileobj(file.file, f)

        send_to_queue(file_location)

        return {"message": f"File '{file.filename}' uploaded and sent to queue."}

    except Exception as e:
        return {"error": str(e)}
