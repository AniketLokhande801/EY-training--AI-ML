from fastapi import FastAPI,HTTPException
from pydantic import BaseModel

class Employee(BaseModel):
    id:int
    name:str
    department:str
    salary:float

e=[
    {"id":1,"name":"aniket","department":"it","salary":10000},
    {"id":2,"name":"soham","department":"hr","salary":20000},
    {"id":3,"name":"yash","department":"it","salary":30000},
    {"id":4,"name":"raviraj","department":"hr","salary":10000},
    {"id":5,"name":"rohit","department":"hr","salary":15000}
]

app=FastAPI()

@app.get("/employees")
def get_all():
    return {"message":"SUCCESS! GET req for all emp ","employees":e}

@app.get("/employees/{id}")
def get_employee(id:int):
    for i in e:
        i["id"] = id
        return {"message":"SUCCESS! GET req for specific emp ","employees":i}
    raise HTTPException(status_code=404,detail="employee not found")

@app.post("/employees")
def add_employee(emp:Employee):
    for i in e:
        if i["id"]==emp.id:
            return {"message":"employee already exists"}
    else:
        e.append(emp.dict())
        return {"message":"SUCCESS! POST req for adding emp ","employees":e}

@app.put("/employees/{id}")
def update_employee(id:int,emp:Employee):
    for i,j in enumerate(e):
        if j["id"]==id:
            e[i]=emp.dict()
            return {"message": "SUCCESS! PUT req for updating emp", "employees": e}
    raise HTTPException(status_code=404,detail="employee not found")

@app.delete("/employees/{id}")
def delete_employee(id:int):
    for i,j in enumerate(e):
        if j["id"]==id:
            e.pop(i)
            return {"message": "SUCCESS! DELETE req for emp ","employees": e}
    raise HTTPException(status_code=404,detail="employee not found")

@app.get("/employees_count")
def employees_count():
    return {"message":"SUCCESS","total count of employees":len(e)}