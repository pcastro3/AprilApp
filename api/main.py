from fastapi import Depends, FastAPI, HTTPException
import os
import smtplib
from email.mime.text import MIMEText
from sqlalchemy.orm import Session
from pydantic import BaseModel
import models
from database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
load_dotenv('.env')

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
    is_confirmed: int
    
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
    
@app.get("/confirm/{email}", response_model=UserModel)
def confirm_email(email: str, db: Session = Depends(get_db)):
    db_user = db.query(models.Users).filter(models.Users.email == email).first()
    db_user.is_confirmed = 1
    db.commit()
    
    print(db_user.id)
    print(db_user.is_confirmed)
    
    return db_user   

@app.get("/confirm/{url}", response_model=UserModel)
def confirmation_path(url: str, db: Session = Depends(get_db)):
    # url - strip email (or id) from end
    # pass email to confirm_email(), which updates db that email has been confirmed
    # confirm_email(email)
    # this function will redirect user to the login page
    # modify code so that it takes user id instead of the email in the confirmation link
    print("Hello")


@app.put("/confirm/async/{email}", response_model=UserModel)
async def confirm_email(email: str, is_confirmed: UserModel, db: Session = Depends(get_db)):
    db_user = db.query(models.Users).filter(models.Users.email == email).first()
    db_user.is_confirmed = 1
    db.commit()
    
    print(db_user.is_confirmed)
    
    return db_user

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
    token = user.email
    confirm_url = 'http://127.0.0.1:8000/confirm/' + user.email
    
    ############# Email Template And Send ############################

    # def send_confirmation():
        
    
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

