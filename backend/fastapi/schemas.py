from pydantic import BaseModel
from typing import Optional
from sqlalchemy import Integer
import os
from dotenv import load_dotenv
load_dotenv()

key = os.getenv('authjwt_secret_key')

class Settings(BaseModel):
    key: str = key


class CheckAdminSchema(BaseModel):
    username: str

# ---------- USER ---------------
class UserRegisterSchema(BaseModel):
    username: str
    phone_number: str
    password: str
    password2: str

class UserLoginSchema(BaseModel):
    username: str
    password: str


class UserUpdateSchema(BaseModel):
    username: str
    phone_number: str

# ----------Category Product-----------

class CategoryCreateSchema(BaseModel):
    name: str

# --------- Product ----------------

class ProductCreateSchema(BaseModel):
    name: str
    category_slug: str
    price: int


class ProductUpdateSchema(BaseModel):
    name: str
    category_slug : str
    price: int


#----------Delivery PERSON --------------

class DeliveryCreateSchema(BaseModel):
    name: str
    delivery_category: str

class DeliveryUpdateSchema(BaseModel):
    delivery_category: str


#---------- Order Product ------------------

class OrderCreateSchema(BaseModel):
    user_slug: str
    product_slug: str
    quantity: int
    delivery_category: str
    delivery_person: str
    address: str

class OrderUpdateSchema(BaseModel):
    quantity: int
    delivery_category: str
    delivery_person: str
    address: str



# ---------Product CART-----------

class CartProductCreateSchema(BaseModel):
    cart_user_slug: str
    product_slug: str
    quantity: int


class CartProductUpdateSchema(BaseModel):
    product_slug: str
    quantity: int
