from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
import logging

app=FastAPI()


logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class Student(BaseModel):
    StudentID:int
    Name:str
    Age:int
    Course:str


student=[
    {'StudentID': 101, 'Name': 'Neha', 'Age': 21, 'Course': 'AI'},
    {'StudentID': 102, 'Name': 'Arjun', 'Age': 22, 'Course': 'ML'},
    {'StudentID': 103, 'Name': 'Sophia', 'Age': 20, 'Course': 'Data Science'},
    {'StudentID': 104, 'Name': 'Ravi', 'Age': 23, 'Course': 'AI'},
    {'StudentID': 105, 'Name': 'Meena', 'Age': 21, 'Course': 'ML'}
]

@app.get("/students")
def get_all_students():
    try:
        logging.info("GET /students called")
        return {"message": "Success! GET request for all students", "Students": student}
    except Exception as e:
        logging.error(f"Error in GET /students: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post("/students")
def add_student(st: Student):
    try:
        for i in student:
            if i['StudentID'] == st.StudentID:
                logging.warning(f"POST /students - Duplicate StudentID: {st.StudentID}")
                raise HTTPException(status_code=400, detail="Student ID exists")
        student.append(st.dict())
        logging.info(f"POST /students - Added student: {st.StudentID}")
        return {"message": "Success! POST request for students", "Students": student}
    except HTTPException as he:
        raise he  # Let FastAPI handle 400 errors
    except Exception as e:
        logging.error(f"Error in POST /students: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.put("/students/{sid}")
def update_student(sid: int, st: Student):
    try:
        for i, j in enumerate(student):
            if j['StudentID'] == sid:
                student[i] = st.dict()
                logging.info(f"PUT /students/{sid} - Updated student")
                return {"message": "Success! PUT request for students", "Students": student}
        logging.warning(f"PUT /students/{sid} - Student ID not found")
        raise HTTPException(status_code=400, detail="Student ID does not exist")
    except HTTPException as he:
        raise he
    except Exception as e:
        logging.error(f"Error in PUT /students/{sid}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.delete("/students/{sid}")
def delete_student(sid: int):
    try:
        for i, j in enumerate(student):
            if j['StudentID'] == sid:
                student.pop(i)
                logging.info(f"DELETE /students/{sid} - Deleted student")
                return {"message": "Success! DELETE request for students", "Students": student}
        logging.warning(f"DELETE /students/{sid} - Student ID not found")
        raise HTTPException(status_code=400, detail="Student ID does not exist")
    except HTTPException as he:
        raise he
    except Exception as e:
        logging.error(f"Error in DELETE /students/{sid}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")





