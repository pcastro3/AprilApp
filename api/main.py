from fastapi import Depends, FastAPI, HTTPException, BackgroundTasks
from send_email import send_email_async
from sqlalchemy.orm import Session
from pydantic import BaseModel
import models
from database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://127.0.0.1:3000",
    "http://localhost",
    "http://localhost:3000"
    
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str

class UserModel(UserBase):
    id: int
    
    class Config:
        orm_mode = True


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users/", response_model=UserModel)
def read_users(limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Users).limit(limit).all()
    
@app.get("/users/{email}", response_model=UserModel)
def read_user_by_email(email: str, db: Session = Depends(get_db)):
    result = db.query(models.Users).filter(models.Users.email == email).first()
    if not result:
        raise HTTPException(status_code=404, detail="User Does Not Exist. Try Signing Up.") 
    else:
        return result    

@app.get("/confirm/async/")
async def confirm_email(db: Session = Depends(get_db)):
    await send_email_async('Hello World', '{models.Users.email}', {
        'title': 'Confirm Email', 
        'name': 'John Doe'
    })
    return 'Success'

@app.post("/users/", response_model=UserModel)
def create_user(user: UserBase, db: Session = Depends(get_db)):
    db_user = models.Users(first_name=user.first_name, last_name=user.last_name, email=user.email, password=user.password)
    db_email = db.query(models.Users).filter(models.Users.email == user.email).first()
    if db_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user
