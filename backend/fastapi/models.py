from sqlalchemy import Column, String, DateTime, ForeignKey, Integer, func
from sqlalchemy.orm import relationship
from slugify import slugify
from database import Base


class User(Base):
    __tablename__ = 'users'

    slug = Column(String, unique=True, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    phone_number = Column(String(12), nullable=False)
    password = Column(String(250), nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now())

    orders = relationship("Order", back_populates="user")
    cart = relationship("Cart", back_populates="user")

    def __init__(self, username, phone_number, password):
        self.username = username
        self.phone_number = phone_number
        self.password = password
        self.slug = slugify(username)


class Category(Base):
    __tablename__ = 'categories'

    slug = Column(String, primary_key=True, unique=True)
    name = Column(String(50), nullable=False)
    products = relationship("Product", back_populates="category")

    def __init__(self, name):
        self.name = name
        self.slug = slugify(name)


class Product(Base):
    __tablename__ = 'products'

    slug = Column(String, primary_key=True, unique=True)
    name = Column(String(50), unique=True, nullable=False)
    category_slug = Column(String, ForeignKey('categories.slug'))
    price = Column(Integer, nullable=False)

    category = relationship("Category", back_populates="products")

    def __init__(self, name, price):
        self.name = name
        self.price = price
        self.slug = slugify(name)


class Delivery(Base):
    __tablename__ = 'deliveries'

    slug = Column(String, primary_key=True, unique=True)
    name = Column(String(50), unique=True, nullable=False)
    delivery_category = Column(String(50), nullable=False)  # bike, car, vehicle

    order = relationship("Order", back_populates="delivery")

    def __init__(self, name, delivery_category):
        self.name = name
        self.delivery_category = delivery_category
        self.slug = slugify(name)

class Order(Base):
    __tablename__ = 'orders'

    slug = Column(String, primary_key=True, unique=True)
    user_slug = Column(String, ForeignKey('users.slug'), nullable=False)
    product_slug = Column(String, ForeignKey('products.slug'), nullable=False)
    quantity = Column(Integer, nullable=False)
    delivery_category = Column(String, nullable=True)
    delivery_person = Column(String, ForeignKey('deliveries.slug'), nullable=True)
    address = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now())

    user = relationship("User", back_populates="orders")
    delivery = relationship("Delivery", back_populates="order")

    def __init__(self,  user_slug, product_slug, quantity, delivery_category, delivery_person, address):
        self.user_slug = user_slug
        self.product_slug = product_slug
        self.quantity = quantity
        self.delivery_category = delivery_category
        self.delivery_person = delivery_person
        self.address = address
        self.slug=slugify(user_slug)


class Cart(Base):
    __tablename__ = 'carts'

    user_slug = Column(String, ForeignKey('users.slug'), primary_key=True)
    products = relationship("CartProduct", back_populates="cart")

    user = relationship("User", back_populates="cart")


class CartProduct(Base):
    __tablename__ = 'cart_products'

    cart_user_slug = Column(String, ForeignKey('carts.user_slug'), primary_key=True)
    product_slug = Column(String, ForeignKey('products.slug'), primary_key=True)
    quantity = Column(Integer, nullable=False)

    cart = relationship("Cart", back_populates="products")
    product = relationship("Product")
