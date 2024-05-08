from fastapi import Depends, FastAPI, HTTPException
import os
import smtplib
from email.mime.text import MIMEText
from sqlalchemy.orm import Session
from pydantic import BaseModel
import models
import webbrowser
from database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
load_dotenv('.env')

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://127.0.0.1",
    "0.0.0.0",
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
    is_confirmed: int
    
    class Config:
        orm_mode = True

class UserLoginModel(BaseModel):
    email: str
    password: str

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"Hello": "World"}

@app.get("/confirm/redirect/{id}")
def confirmation_path(id: int, db: Session = Depends(get_db)):
    # Redirect
    webbrowser.open('http://localhost:3000/login')
    # Find user and change confirmation state
    db_user = db.query(models.Users).filter(models.Users.id == id).first()
    db_user.is_confirmed = 1
    db.commit()
    

@app.post("/users/", response_model=UserModel)
def create_user(user: UserBase, db: Session = Depends(get_db)):
    db_user = models.Users(first_name=user.first_name, last_name=user.last_name, email=user.email, password=user.password)
    db_email = db.query(models.Users).filter(models.Users.email == user.email).first()
    
    ####### CHECK IF EMAIL ALREADY EXISTS
    if db_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    db.add(db_user)
    db.commit() 
    db.refresh(db_user)
    confirm_url = 'http://127.0.0.1:8000/confirm/redirect/' + repr(db_user.id)
    
    ############# Email Template And Send ############################

    title = 'Confirm Your Email Here!'
    msg_content = '<p><a href="{confirm_url}" onclick="send_confirmation">{title}</a></p>'.format(title=title, confirm_url=confirm_url)
    message = MIMEText(msg_content, 'html')
    
    message['From'] = os.getenv('MAIL_FROM')
    message['To'] = user.email
    message['Subject'] = 'Please Confirm Your Email Here =)!'
    
    msg_full = message.as_string()
    
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(os.getenv('MAIL_FROM'), os.getenv('MAIL_PASSWORD'))
    server.sendmail(os.getenv('MAIL_FROM'), user.email, msg_full)
    server.quit()
    
    return db_user

@app.post("/users/login/")
def login_user(user: UserLoginModel, db: Session = Depends(get_db)):
    db_user = db.query(models.Users).filter(models.Users.email == user.email).first()
    
    if db_user.email == user.email and db_user.password == user.password and db_user.is_confirmed == True:
        webbrowser.open('http://localhost:3000/landing')
    else:
        print('Invalid Credentials. Please Try Again')    
