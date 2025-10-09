from fastapi import FastAPI,HTTPException
from pydantic import BaseModel

class Employee(BaseModel):
    id:int
    name:str
    department:str
    salary:float

e=[
    {"id":1,"name":"aniket","department":"it","salary":10000},
    # {"id":2,"name":"soham","department":"hr","salary":20000},
    # {"id":3,"name":"yash","department":"it","salary":30000},
    # {"id":4,"name":"raviraj","department":"hr","salary":10000},
    # {"id":5,"name":"rohit","department":"hr","salary":15000}
]

app=FastAPI()

@app.get("/employees")
def get_all():
    return e

@app.get("/employees/{id}")
def get_employee(id:int):
    for i in e:
        if i["id"] == id:
            return i
    raise HTTPException(status_code=404,detail="employee not found")

@app.post("/employees")
def add_employee(emp:Employee):
    for i in e:
        if i["id"]==emp.id:
            return {"message":"employee already exists"}
    else:
        e.append(emp.dict())
        return emp

@app.put("/employees/{id}")
def update_employee(id:int,emp:Employee):
    for i,j in enumerate(e):
        if j["id"]==id:
            e[i]=emp.dict()
            return e[i]
    raise HTTPException(status_code=404,detail="employee not found")

@app.delete("/employees/{id}")
def delete_employee(id:int):
    for i,j in enumerate(e):
        if j["id"]==id:
            e.pop(i)
            return {"message":"SUCCESS!"}







# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
#
# app = FastAPI()
#
#
# class Employee(BaseModel):
#     id: int
#     name: str
#     department: str
#     Salary: float
#
#
# Employees = [{"id": 1, "name": "Prajakta", "department": "HR", "Salary": 50000}, ]
#
#
# @app.get("/employees")
# def get_all_employee():
#     return Employees
#
#
# @app.post("/employees", status_code=201)
# def add_employee(employee: Employee):
#     Employees.append(employee.dict())
#     return employee
#
#
# @app.get("/employees/{employee_id}")
# def get_employee(employee_id: int):
#     for emp in Employees:
#         if emp["id"] == employee_id:
#             return emp
#     raise HTTPException(status_code=404, detail="Employee not found")