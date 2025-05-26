from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from models import User
from db import SessionLocal, init_db
from producer import publish_user_created
from cache import get_user_from_cache, save_user_to_cache
from pydantic import BaseModel

app = FastAPI()
init_db()

class UserCreate(BaseModel):
    name: str
    email: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users")
def create_user(user: UserCreate, session: Session = Depends(get_db)):
    new_user = User(name=user.name, email=user.email)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    publish_user_created({
        "id": new_user.id,
        "name": new_user.name,
        "email": new_user.email
    })

    return {"message": "User created", "user": {"id": new_user.id, "name": new_user.name}}

@app.get("/users/{user_id}")
def read_user(user_id: int, session: Session = Depends(get_db)):
    cached = get_user_from_cache(user_id)
    if cached:
        print("Данные из кэша", flush=True)
        return {"source": "cache", "user": cached}

    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        return {"error": "User not found"}

    user_data = {"id": user.id, "name": user.name, "email": user.email}
    save_user_to_cache(user.id, user_data)

    print("Данные из базы и сохранены в кэш", flush=True)
    return {"source": "db", "user": user_data}
