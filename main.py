from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
import models
from models import SessionLocal, OrderType, Order

app = FastAPI()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class OrderCreate(BaseModel):
    symbol: str
    price: float
    quantity: int
    order_type: OrderType

# Create Order (POST)
@app.post("/orders/")
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    db_order = Order(**order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

# Get Orders (GET)
@app.get("/orders/")
def get_orders(db: Session = Depends(get_db)):
    return db.query(Order).all()
