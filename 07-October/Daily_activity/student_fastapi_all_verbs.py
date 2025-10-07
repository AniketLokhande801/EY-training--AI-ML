from fastapi import FastAPI ,HTTPException
from pydantic import BaseModel

app = FastAPI()

class Student(BaseModel):
    id:int
    name: str
    age:int
    course:str

st=[
    {"s_id":1,"name":"aniket","age":22,"course":"AI"},
    {"s_id":2,"name":"yash","age":22,"course":"ml"}
]

@app.get("/students")
def student():
    return {"students":st}

@app.get("/students/{s_id}")
def student(s_id: int):
    for s in st:
        if s["s_id"]==s_id:
            return s
    raise HTTPException(status_code=404,detail="student not found")


@app.post("/students_post", status_code=201)
def new_student(stud: Student):
    st.append(stud.dict())
    return {"message": "Added successfully", "students": st}

@app.put("/student_put/{s_id}",status_code=200)
def update_student(stud: Student,s_id: int):
    for i,d in enumerate(st):
        if d["s_id"]==s_id:
            st[i]=stud.dict()
            return {"message": "Updated successfully", "students": st}
    raise HTTPException(status_code=404,detail="student not found")

@app.delete("/student_delete/{s_id}",status_code=200)
def delete_student(stud: Student,s_id: int):
    for i,d in enumerate(st):
        if d["s_id"]==s_id:
            st.pop(i)
            return {"message": "Deleted successfully", "students": st}
    raise HTTPException(status_code=404,detail="student not found")

