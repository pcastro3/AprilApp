from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "mssql+pyodbc://sa:YourStrong0Passw0rd@localhost:1433/april?driver=ODBC+Driver+17+for+SQL+Server"
# who does docker say the host is (in the logs)? take that info and replace localhost in the alchemy url?
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()