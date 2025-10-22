from fastapi import FastAPI, HTTPException, Form, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from DB.database import get_connection, init_db
from etl.etl_process import run_etl
import pandas as pd
from datetime import datetime
from msg_queue.producer import send_csv_to_queue
import os
import logging
import asyncio


logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


app = FastAPI()
templates = Jinja2Templates(directory="crud/templates")




@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})


@app.get("/students_html", response_class=HTMLResponse)
def students_html(request: Request):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students")
        data = cursor.fetchall()
        conn.close()
        logging.info("GET /students_html - Fetched all students")

        html = "<h3>All Students</h3><table border='1'><tr><th>ID</th><th>Name</th><th>Age</th><th>Course</th></tr>"
        for s in data:
            html += f"<tr><td>{s[0]}</td><td>{s[1]}</td><td>{s[2]}</td><td>{s[3]}</td></tr>"
        html += "</table>"
        return HTMLResponse(content=html)
    except Exception as e:
        logging.error(f"Error in /students_html: {e}", exc_info=True)
        return HTMLResponse(f"<h3>Error: {e}</h3>")

@app.get("/students_ai_html", response_class=HTMLResponse)
def students_ai_html(request: Request):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students WHERE Course='AI'")
        data = cursor.fetchall()
        conn.close()
        logging.info("GET /students_ai_html - Fetched AI students")

        html = "<h3>AI Students</h3><table border='1'><tr><th>ID</th><th>Name</th><th>Age</th><th>Course</th></tr>"
        for s in data:
            html += f"<tr><td>{s[0]}</td><td>{s[1]}</td><td>{s[2]}</td><td>{s[3]}</td></tr>"
        html += "</table>"
        return HTMLResponse(content=html)
    except Exception as e:
        logging.error(f"Error in /students_ai_html: {e}", exc_info=True)
        return HTMLResponse(f"<h3>Error: {e}</h3>")


@app.post("/students")
def add_student(StudentID : int =Form(...),name: str = Form(...), age: int = Form(...), course: str = Form(...)):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO students (StudentID,Name, Age, Course) VALUES (%s,%s,%s,%s)", (StudentID,name, age, course))
        conn.commit()
        conn.close()
        logging.info(f"Added student {name}")
        return HTMLResponse(f"<h3>Student '{name}' added successfully!</h3>")
    except Exception as e:
        logging.error(f"Error in add_student: {e}", exc_info=True)
        return HTMLResponse(f"<h3>Error: {e}</h3>")

@app.post("/students_update")
def update_student_form(student_id: int = Form(...), name: str = Form(None), age: int = Form(None), course: str = Form(None)):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = "UPDATE students SET "
        values = []
        if name: query += "Name=%s, "; values.append(name)
        if age: query += "Age=%s, "; values.append(age)
        if course: query += "Course=%s, "; values.append(course)
        query = query.rstrip(", ") + " WHERE StudentID=%s"
        values.append(student_id)
        cursor.execute(query, tuple(values))
        conn.commit()
        if cursor.rowcount == 0:
            conn.close()
            return HTMLResponse(f"<h3>Student ID {student_id} not found!</h3>")
        conn.close()
        logging.info(f"Updated student {student_id}")
        return HTMLResponse(f"<h3>Student ID {student_id} updated successfully!</h3>")
    except Exception as e:
        logging.error(f"Error in update_student_form: {e}", exc_info=True)
        return HTMLResponse(f"<h3>Error: {e}</h3>")

@app.post("/students_delete")
def delete_student_form(student_id: int = Form(...)):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM students WHERE StudentID=%s", (student_id,))
        conn.commit()
        if cursor.rowcount == 0:
            conn.close()
            return HTMLResponse(f"<h3>Student ID {student_id} not found!</h3>")
        conn.close()
        logging.info(f"Deleted student {student_id}")
        return HTMLResponse(f"<h3>Student ID {student_id} deleted successfully!</h3>")
    except Exception as e:
        logging.error(f"Error in delete_student_form: {e}", exc_info=True)
        return HTMLResponse(f"<h3>Error: {e}</h3>")

@app.get("/etl_results", response_class=HTMLResponse)
def etl_results():
    try:
        output_file, df = run_etl("data/marks.csv", "student_results")
        
        # Convert to HTML table
        html = f"<h3>ETL Results - {output_file}</h3>"
        html += "<table border='1'><tr>"
        for col in df.columns:
            html += f"<th>{col}</th>"
        html += "</tr>"
        for _, row in df.iterrows():
            html += "<tr>" + "".join([f"<td>{row[col]}</td>" for col in df.columns]) + "</tr>"
        html += "</table>"
        return HTMLResponse(content=html)
    except Exception as e:
        return HTMLResponse(f"<h3>Error: {e}</h3>")



@app.get("/etl_queue_results", response_class=HTMLResponse)
def etl_queue_results():
    try:
        output_file = "data/student_results_using_queue.csv"

        if not os.path.exists(output_file):
            return HTMLResponse("<h3>ETL is still processing. Please try again in a few seconds.</h3>")

        df = pd.read_csv(output_file)

        # Convert to HTML table
        html = "<h3>ETL Results (from Queue)</h3><table border='1'><tr>"
        for col in df.columns:
            html += f"<th>{col}</th>"
        html += "</tr>"
        for _, row in df.iterrows():
            html += "<tr>"
            for col in df.columns:
                html += f"<td>{row[col]}</td>"
            html += "</tr>"
        html += "</table>"

        return HTMLResponse(content=html)
    except Exception as e:
        logging.error(f"Error displaying ETL queue results: {e}", exc_info=True)
        return HTMLResponse(f"<h3>Error: {e}</h3>")


from fastapi import UploadFile
import os

@app.post("/upload_marks_csv", response_class=HTMLResponse)
async def upload_marks_csv(file: UploadFile):
    try:
        # Ensure filename keeps extension
        base, ext = os.path.splitext(file.filename)
        fname = f"{base}_uploaded{ext}"
        save_path = f"data/{fname}"

        with open(save_path, "wb") as f:
            f.write(await file.read())
        
        logging.info(f"Uploaded CSV saved at {save_path}")

        # Send to RabbitMQ ETL queue
        send_csv_to_queue(save_path)
        logging.info(f"CSV {save_path} sent to RabbitMQ ETL queue")

        return HTMLResponse(f"<h3>CSV uploaded and sent to ETL queue successfully!</h3>")

    except Exception as e:
        logging.error(f"Error in /upload_marks_csv: {e}", exc_info=True)
        return HTMLResponse(f"<h3>Error: {e}</h3>")


@app.get("/students_etl_html", response_class=HTMLResponse)
def students_etl_html():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT StudentID, Name, Age, Course, Maths, Python, ML, TotalMarks, Percentage, Result
            FROM students
        """)
        data = cursor.fetchall()
        conn.close()

        html = "<h3>ETL Results - Students (DB)</h3>"
        html += "<table border='1'><tr>"
        headers = ["StudentID", "Name", "Age", "Course", "Maths", "Python", "ML", "TotalMarks", "Percentage", "Result"]
        for h in headers:
            html += f"<th>{h}</th>"
        html += "</tr>"

        for row in data:
            html += "<tr>"
            for col in row:
                html += f"<td>{col}</td>"
            html += "</tr>"
        html += "</table>"

        return HTMLResponse(html)

    except Exception as e:
        logging.error(f"Error in /students_etl_html: {e}", exc_info=True)
        return HTMLResponse(f"<h3>Error: {e}</h3>")

from analytics.final_analytics import run_final_analytics
from fastapi.responses import HTMLResponse

@app.get("/final_analytics", response_class=HTMLResponse)
def final_analytics_endpoint():
    try:
        merged_df, top3_df, avg_marks_series = run_final_analytics(
            "data/marks.csv", "data/student_results.csv"
        )

        html = "<h3>Final Analytics - Merged Students & Marks</h3>"
        html += "<h4>Top 3 Students by Percentage</h4>"
        html += top3_df.to_html(index=False, border=1)

        html += "<h4>Average Marks per Subject</h4>"
        html += avg_marks_series.to_frame(name="Average Marks").to_html(border=1)

        return HTMLResponse(content=html)

    except Exception as e:
        logging.error(f"Error in /final_analytics: {e}", exc_info=True)
        return HTMLResponse(f"<h3>Error: {e}</h3>")





