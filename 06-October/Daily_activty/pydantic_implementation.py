from pydantic import BaseModel

class Student(BaseModel):
    name: str
    age : int
    email : str
    isactive : bool

data={"name":"Aniket","age":22,"email":"asl@gmail.com","isactive":True}

student = Student(**data)

print(student)
print(student.age)