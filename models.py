import os
from sqlalchemy import Column, Integer, String, Float, Enum, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import enum

# Check if we are running in test mode (GitHub Actions)
TEST_ENV = os.getenv("TEST_ENV", "false").lower() == "true"

# Use SQLite for testing, PostgreSQL for production
if TEST_ENV:
    DATABASE_URL = "sqlite:///./test.db"
else:
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://sumathikoram:password@db/trade_db")

# Database Engine
if TEST_ENV:
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}, echo=True)
else:
    engine = create_engine(DATABASE_URL, echo=True)

# Session Factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base Model
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

# Create Tables (Only in test mode)
if TEST_ENV:
    Base.metadata.create_all(bind=engine)
