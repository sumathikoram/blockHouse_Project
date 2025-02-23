from sqlalchemy import Column, Integer, String, Float, Enum, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base  # Correct import for SQLAlchemy 2.0
from sqlalchemy import create_engine
#from models import Base  # Ensure models.py defines the Base class
import enum
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://sumathikoram:password@db/trade_db")


# Database Configuration
#DATABASE_URL = "sqlite:///./orders.db"  # Change for PostgreSQL
#DATABASE_URL = "postgresql://sumathikoram:password@localhost/trade_db"


#engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
engine = create_engine(DATABASE_URL,echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Enum for Order Types
class OrderType(str, enum.Enum):
    market = "market"
    limit = "limit"

# Order Model
class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    price = Column(Float)
    quantity = Column(Integer)
    order_type = Column(Enum(OrderType))

# Create Tables
Base.metadata.create_all(bind=engine)
