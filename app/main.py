from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app import database, models
from app.database import SessionLocal, create_tables
from app.models import ProductCreate, ProductUpdate, ProductResponse
from datetime import datetime

# Create tables on startup
create_tables()

# Initialize FastAPI app
app = FastAPI()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Helper function to convert datetime to string
def datetime_to_str(product):
    if product.created_date:
        product.created_date = product.created_date.isoformat()
    if product.updated_date:
        product.updated_date = product.updated_date.isoformat()
    return product

# API: List all products with pagination
@app.get("/product/list", response_model=List[ProductResponse])
def list_products(skip: int = Query(0, ge=0), limit: int = Query(10, le=100), db: Session = Depends(get_db)):
    products = db.query(database.Product).offset(skip).limit(limit).all()
    products = [datetime_to_str(product) for product in products]
    return products

# API: View product info by ID
@app.get("/product/{pid}/info", response_model=ProductResponse)
def get_product(pid: int, db: Session = Depends(get_db)):
    product = db.query(database.Product).filter(database.Product.id == pid).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    product = datetime_to_str(product)
    return product

# API: Add a new product
@app.post("/product/add", response_model=ProductResponse)
def add_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = database.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    db_product = datetime_to_str(db_product)  # Convert datetime fields
    return db_product

# API: Update an existing product
@app.put("/product/{pid}/update", response_model=ProductResponse)
def update_product(pid: int, product: ProductUpdate, db: Session = Depends(get_db)):
    db_product = db.query(database.Product).filter(database.Product.id == pid).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    for key, value in product.dict(exclude_unset=True).items():
        setattr(db_product, key, value)
    
    db.commit()
    db.refresh(db_product)
    db_product = datetime_to_str(db_product)  # Convert datetime fields
    return db_product
