from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/items/", response_model=schemas.ToDoItem)
def create_todo_item(todo: schemas.ToDoItemCreate, db: Session = Depends(get_db)):
    return crud.create_todo_item(db=db, todo=todo)

@app.get("/items/", response_model=list[schemas.ToDoItem])
def read_todo_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    todos = crud.get_todos(db, skip=skip, limit=limit)
    return todos

@app.get("/items/{item_id}", response_model=schemas.ToDoItem)
def read_todo_item(item_id: int, db: Session = Depends(get_db)):
    db_todo = crud.get_todo_by_id(db, todo_id=item_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="ToDo item not found")
    return db_todo

@app.put("/items/{item_id}", response_model=schemas.ToDoItem)
def update_todo_item(item_id: int, todo: schemas.ToDoItemCreate, db: Session = Depends(get_db)):
    db_todo = crud.update_todo_item(db, todo_id=item_id, todo=todo)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="ToDo item not found")
    return db_todo

@app.delete("/items/{item_id}", response_model=schemas.ToDoItem)
def delete_todo_item(item_id: int, db: Session = Depends(get_db)):
    db_todo = crud.delete_todo_item(db, todo_id=item_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="ToDo item not found")
    return db_todo