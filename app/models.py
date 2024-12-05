from app import db
from flask_login import UserMixin
from sqlalchemy import Column, ForeignKey, Integer, Float, String, Table
from sqlalchemy.orm import relationship

Wishlist = Table(
    "Wishlist",
    db.Model.metadata,
    Column("customer_id", ForeignKey("customer.id"), primary_key=True),
    Column("lego_id", ForeignKey("lego.id"), primary_key=True)
)

class Customer(db.Model, UserMixin):
    __tablename__ = "customer"
    id = Column(Integer, primary_key=True)
    firstname = Column(String(20), nullable=False)
    surname = Column(String(20), nullable=False)
    email = Column(String(50), nullable=False)
    password = Column(String(80), nullable=False)
    legos = relationship("Lego", secondary=Wishlist, backref="customers")

class Lego(db.Model):
    __tablename__ = "lego"
    id = Column(Integer, primary_key=True)
    product_name = Column(String(500))
    category = Column(String(500))
    description = Column(String(1500))
    final_price = Column(Float)
    age_range = Column(String(5))
    image_urls = Column(String(2000))
    stock_quantity = Column(Integer)
    


