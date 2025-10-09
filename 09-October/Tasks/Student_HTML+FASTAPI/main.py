from fastapi import FastAPI,Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
app=FastAPI()

templates = Jinja2Templates(directory="templates")

st=[
    {"s_id":1,"name":"aniket","age":22,"course":"AI"},
    {"s_id":2,"name":"yash","age":22,"course":"ml"},
    {"s_id":3,"name":"Soham","age":22,"course":"ml"},
    {"s_id":4,"name":"rohit","age":22,"course":"AI"},
    {"s_id":5,"name":"raviraj","age":22,"course":"ml"},
]

@app.get("/",response_class=HTMLResponse)
def show_index(req:Request):
    return templates.TemplateResponse("index.html",{"request":req})

@app.get("/student",response_class=HTMLResponse)
def show_students(req:Request):
    return templates.TemplateResponse("student.html",{"request":req,"students":st})


