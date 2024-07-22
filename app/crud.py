from sqlalchemy.orm import Session
from . import models, schemas

def get_todos(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.ToDoItem).offset(skip).limit(limit).all()

def get_todo_by_id(db: Session, todo_id: int):
    return db.query(models.ToDoItem).filter(models.ToDoItem.id == todo_id).first()

def create_todo_item(db: Session, todo: schemas.ToDoItemCreate):
    db_todo = models.ToDoItem(**todo.dict())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def update_todo_item(db: Session, todo_id: int, todo: schemas.ToDoItemCreate):
    db_todo = db.query(models.ToDoItem).filter(models.ToDoItem.id == todo_id).first()
    if db_todo:
        db_todo.title = todo.title
        db_todo.description = todo.description
        db.commit()
        db.refresh(db_todo)
        return db_todo
    return None

def delete_todo_item(db: Session, todo_id: int):
    db_todo = db.query(models.ToDoItem).filter(models.ToDoItem.id == todo_id).first()
    if db_todo:
        db.delete(db_todo)
        db.commit()
        return db_todo
    return None
