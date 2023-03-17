from typing import Union
from fastapi import FastAPI, Request, Form, Depends, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from schemas import BookUpdate


templates = Jinja2Templates(directory="templates")

from sqlalchemy.orm import Session

import models
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.mount('/static', StaticFiles(directory="static"), name="static")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home(request: Request, db: Session = Depends(get_db)):
    all_book_db = db.query(models.Book).all()
    context = {
            "request": request,
            "all_book": all_book_db,

    }
    return templates.TemplateResponse("index.html",  context)

@app.post('/add')
def add(request: Request, book_name: str = Form(...), book_author: str = Form(...), db: Session = Depends(get_db)):
    newbook = models.Book(book_name=book_name, book_author=book_author)
    db.add(newbook)
    db.commit()
    url = app.url_path_for("home")
    return RedirectResponse(url=url, status_code=status.HTTP_302_FOUND)


@app.get("/delete/{book_id}")
def delete(request: Request, book_id: int, db: Session = Depends(get_db)):
    singlebook = db.query(models.Book).filter(models.Book.id == book_id).first()
    db.delete(singlebook)
    db.commit()
 
    url = app.url_path_for("home")
    return RedirectResponse(url=url, status_code=status.HTTP_302_FOUND)

@app.get("/updatedata/{book_id}/")
def updatedata(request: Request, book_id: int, db: Session = Depends(get_db)):
    singlebook = db.query(models.Book).filter(models.Book.id == book_id).first()
    book_name_update = singlebook.book_name
    book_author_update = singlebook.book_author
        
    context = {
            "request": request,
            "book_name": book_name_update,
            "book_author": book_author_update,
            "book_id": singlebook.id

    }
    return templates.TemplateResponse("update.html",  context)

@app.post("/update/{book_id}")
def update(request: Request, book_id: int, book_update: BookUpdate = Depends(BookUpdate.as_form), db: Session = Depends(get_db)):
    singlebook = db.query(models.Book).filter(models.Book.id == book_id).first()
    if singlebook is None:
        return {"error": "Book not found."}
    singlebook.book_name = book_update.book_name
    singlebook.book_author = book_update.book_author
    db.commit()
    url = app.url_path_for("home")
    return RedirectResponse(url=url, status_code=status.HTTP_302_FOUND)