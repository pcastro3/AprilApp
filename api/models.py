from sqlalchemy import Column, Integer, String, Boolean

from database import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    password = Column(String)
    is_confirmed = Column(Boolean, nullable=False, default=0)
