# app/crud.py
from sqlalchemy.orm import Session
from app import models

def get_products(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Product).offset(skip).limit(limit).all()

def get_product_by_id(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def create_product(db: Session, name: str, category: str, description: str, product_image: str, sku: str, unit_of_measure: str, lead_time: int):
    db_product = models.Product(
        name=name,
        category=category,
        description=description,
        product_image=product_image,
        sku=sku,
        unit_of_measure=unit_of_measure,
        lead_time=lead_time,
        created_date=datetime.datetime.utcnow()
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(db: Session, product_id: int, name: str, category: str, description: str, product_image: str, sku: str, unit_of_measure: str, lead_time: int):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product:
        db_product.name = name
        db_product.category = category
        db_product.description = description
        db_product.product_image = product_image
        db_product.sku = sku
        db_product.unit_of_measure = unit_of_measure
        db_product.lead_time = lead_time
        db.commit()
        db.refresh(db_product)
    return db_product
