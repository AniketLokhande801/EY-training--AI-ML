from fastapi import FastAPI

app=FastAPI()

st=[
    {"s_id":1,"name":"aniket","age":22,"course":"AI"},
    {"s_id":2,"name":"yash","age":22,"course":"ml"},
    {"s_id":3,"name":"Soham","age":22,"course":"ml"},
    {"s_id":4,"name":"rohit","age":22,"course":"AI"},
    {"s_id":5,"name":"raviraj","age":22,"course":"ml"},
]

@app.get("/Show all")
def show_all():
    return {"message":"SUCCESS!","data":st}
