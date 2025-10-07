from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def index():
    return {"message":"Hello World!"}
@app.get("/student/{s_id}")
def student(s_id: int):
    return {"student_id":s_id,"name":"aniket","course":"AI"}