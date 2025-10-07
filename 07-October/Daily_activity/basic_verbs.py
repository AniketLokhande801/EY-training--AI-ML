from fastapi import FastAPI

app = FastAPI()

@app.get("/students")
def index():
    return {"message":"get request"}

@app.put("/students_put")
def student_put():
    return {"message":"put request"}

@app.post("/students_post")
def student_post():
    return {"message":"post request"}

@app.delete("/students_delete")
def student_del():
    return {"message":"delete request"}