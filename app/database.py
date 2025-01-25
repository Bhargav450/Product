from sqlalchemy import create_engine, Column, Integer, String, Enum, Text, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from datetime import datetime
import mysql.connector
import os

# MySQL connection string
DATABASE_URL = "mysql+mysqlconnector://root:@localhost/flask"

# Create a SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=True)

# Create a session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Product Table Model
class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    category = Column(Enum('finished', 'semi-finished', 'raw', name='category_enum'), nullable=False)
    description = Column(String(250), nullable=True)
    product_image = Column(Text, nullable=True)
    sku = Column(String(100), nullable=True)
    unit_of_measure = Column(Enum('mtr', 'mm', 'ltr', 'ml', 'cm', 'mg', 'gm', 'unit', 'pack', name='uom_enum'), nullable=False)
    lead_time = Column(Integer, nullable=False)
    created_date = Column(TIMESTAMP, default=datetime.utcnow)
    updated_date = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

# Create the tables in the database
def create_tables():
    Base.metadata.create_all(bind=engine)

