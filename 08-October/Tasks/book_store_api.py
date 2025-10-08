from fastapi import FastAPI,HTTPException,Query
from pydantic import BaseModel,Field
from typing import Optional

class Book(BaseModel):
    id:int
    title:str
    author:str
    price:float=(Field(gt=0))
    in_stock:bool


books=[
{"id": 1, "title": "Deep Learning", "author": "Ian Goodfellow", "price": 1200, "in_stock": True},
{"id": 2, "title": "Artificial Intelligence", "author": "Stuart Russell", "price": 950, "in_stock": False},
{"id": 3, "title": "Pattern Recognition", "author": "Christopher M. Bishop", "price": 1100, "in_stock": True},
{"id": 4, "title": "Machine Learning", "author": "Aurélien Géron", "price": 850, "in_stock": True},
{"id": 5, "title": "Reinforcement Learning", "author": "Richard S. Sutton", "price": 1050, "in_stock": False}]

app=FastAPI()

@app.get("/books")
def get_books():
    return {"message":"SUCCESS! GET req for all emp ","employees":books}

@app.get("/books/search")
def search_books(author: Optional[str] = Query(None), max_price: Optional[float] = Query(None)):
    filtered_books = books  # start with all books

    if author:
        for book in filtered_books :
            if author.lower() in book["author"].lower():
                dummy1=[]
                dummy1.append(book)
                filtered_books = dummy1

    if max_price is not None:
        for book in filtered_books :
            if book["price"] <= max_price:
                dummy1 = []
                dummy1.append(book)
                filtered_books = dummy1

    return {"message": "SUCCESS! Search results", "results": filtered_books}

@app.get("/books/available")
def books_available():
    available = []
    for i,j in enumerate(books):
        if j["in_stock"]==True:
            available.append(books[i])
            return {"message": "SUCCESS! Book available", "books": available}
    raise HTTPException(status_code=404,detail="book not found")

@app.get("/books/count")
def books_count():
    return {"message": "SUCCESS", "total count of books": len(books)}

@app.get("/books/{id}")
def get_employee(id:int):
    for i in books:
        i["id"] = id
        return {"message":"SUCCESS! GET req for specific book ","book":i}
    raise HTTPException(status_code=404,detail="employee not found")

@app.post("/books")
def add_employee(bk:Book):
    for i in books:
        if i["id"]==bk.id:
            return {"message":"employee already exists"}
    else:
        books.append(bk.dict())
        return {"message":"SUCCESS! POST req for adding Book","books":books}



@app.put("/books/{id}")
def update_employee(id:int,bk:Book):
    for i,j in enumerate(books):
        if j["id"]==id:
            books[i]=bk.dict()
            return {"message": "SUCCESS! PUT req for updating book", "books": books}
    raise HTTPException(status_code=404,detail="employee not found")

@app.delete("/books/{id}")
def delete_employee(id:int):
    for i,j in enumerate(books):
        if j["id"]==id:
            books.pop(i)
            return {"message": "SUCCESS! DELETE req for books ","books": books}
    raise HTTPException(status_code=404,detail="employee not found")

