from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
import datetime

class Bill(Base):
    __tablename__ = "bills"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String, index=True)
    customer_phone = Column(String)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    total_amount = Column(Float)
    discount = Column(Float, default=0.0)
    status = Column(String, default="Unpaid")
    payment_mode = Column(String, nullable=True)

    items = relationship("BillItem", back_populates="bill", cascade="all, delete-orphan")

class BillItem(Base):
    __tablename__ = "bill_items"

    id = Column(Integer, primary_key=True, index=True)
    bill_id = Column(Integer, ForeignKey("bills.id"))
    item_name = Column(String)
    price = Column(Float)
    quantity = Column(Integer)
    item_total = Column(Float)

    bill = relationship("Bill", back_populates="items")
