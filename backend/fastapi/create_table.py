from database import Base, Engine
from models import User, Category, Product, Delivery, Order,  Cart, CartProduct


def migrate():
    Base.metadata.create_all(bind=Engine)