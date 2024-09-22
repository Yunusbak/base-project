import datetime
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from schemas import UserRegisterSchema, UserLoginSchema, UserUpdateSchema, CartProductCreateSchema, CartProductUpdateSchema,  OrderCreateSchema, OrderUpdateSchema
from database import Session, Engine
from models import User, Cart, CartProduct, Order, Product
from fastapi.encoders import jsonable_encoder
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi_jwt_auth import AuthJWT

from models import CartProduct


user_router = APIRouter(prefix='/user', tags=['USER PAGE'])


session = Session(bind=Engine)

@user_router.get('/')
async def user_page():
    return {"message" : "User Page"}



@user_router.post('/register')
async def user_register(user: UserRegisterSchema):
    check_user = session.query(User).filter(User.username == user.username).first()

    if check_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User already exists')

    if user.password != user.password2:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Passwords do not match")

    if len(user.phone_number) != 12:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Phone number must be 12 digits")

    new_user = User(
        username=user.username,
        phone_number=user.phone_number,
        password=generate_password_hash(user.password)
    )
    session.add(new_user)
    session.commit()
    data = {
        "status": 201,
        "message": "User Registered"
    }
    return jsonable_encoder(data)

@user_router.post('/login')
async def user_login(user : UserLoginSchema, Authorization : AuthJWT = Depends()):
    check_user = session.query(User).filter(User.username == user.username).first()
    if check_user:
        if check_password_hash(check_user.password, user.password):
            access_token = Authorization.create_access_token(subject=check_user.username, expires_time=datetime.timedelta(minutes=30))
            refresh_token = Authorization.create_refresh_token(subject=check_user.username, expires_time=datetime.timedelta(hours=5))

            data = {
                "status" : 200,
                "message" : "Login Successful",
                "access_token" : access_token,
                "refresh_token" : refresh_token
            }
            return jsonable_encoder(data)
        else:
            data = {
                "status" : 401,
                "message" : "Password Incorrect"
            }
            return jsonable_encoder(data)

    else:
        data = {
            "status" : 401,
            "message" : "User Not Registered"
        }
        return jsonable_encoder(data)


@user_router.put('/{user_slug}')
async def user_put(user_slug: str, user: UserUpdateSchema, Authorization : AuthJWT = Depends()):
    try:
        Authorization.jwt_required()
        check_user = session.query(User).filter(User.username == user_slug).first()
        if check_user:
            for key, value in user.__dict__.items():
                setattr(check_user, key, value)
                session.commit()

            data = {
                "status" : 200,
                "message" : "User Updated"
            }
            return jsonable_encoder(data)
        else:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found")

    except Exception as e:
        return HTTPException(status_code=400, detail="Bad Request")

@user_router.get('/user')
async def user_get(Authorization : AuthJWT = Depends()):
    try:
        Authorization.jwt_required()
        user = session.query(User).filter(User.username == Authorization.get_jwt_subject()).first()

        data = {
            "status" : 200,
            "message" : "User Retrieved",
            "detail" : {
                user
            }
        }
        return jsonable_encoder(data)

    except Exception as e:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bad Request")



@user_router.get('/token-verify')
async def token_verify(Authorization : AuthJWT = Depends()):
    try:
        Authorization.jwt_required()

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")



@user_router.get('/products')
async def user_products(Authorization : AuthJWT = Depends()):
    try:
        # Authorization.jwt_required()
        products = session.query(Product).all()
        if products:
            data = {
                "status" : 200,
                "message" : "Products Retrieved",
                "products": products
            }
            return jsonable_encoder(data)
        else:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Products")
    except Exception as e:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bad Request")


@user_router.get('/products/{product_slug}')
async def user_products(product_slug : str, Authorization: AuthJWT = Depends()):
    try:
        # Authorization.jwt_required()
        product = session.query(Product).filter(Product.slug == product_slug).first()
        if product:
            return jsonable_encoder(product)
        else:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Product")
    except Exception as e:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bad Request")

# ----------------------------------------------------------------------------------------------------




@user_router.post('/create-order')
async def create_order(order: OrderCreateSchema, Authorization: AuthJWT = Depends()):
    try:
        Authorization.jwt_required()
        new_order = Order(
            user_slug=order.user_slug,
            product_slug=order.product_slug,
            delivery_person=order.delivery_person,
            address=order.address,
            quantity=order.quantity,
            delivery_category=order.delivery_category
        )
        session.add(new_order)
        session.commit()

        data = {
            "status": 201,
            "message": "Order created successfully",
            "order": new_order
        }
        return jsonable_encoder(data)
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))



@user_router.get('/orders')
async def list_orders(Authorization : AuthJWT = Depends()):
    Authorization.jwt_required()
    orders = session.query(Order).all()
    if orders:
        data = {
            "status": 200,
            "orders": orders
        }
        return jsonable_encoder(data)
    else:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Orders")





# USER PRODUCT SHOP-------------------------------



@user_router.get('/cart')
async def cart_get(Authorization : AuthJWT = Depends()):
    try:
        Authorization.jwt_required()
        current_user = session.query(User).filter(User.username == Authorization.get_jwt_subject()).first()
        carts = session.query(CartProduct).filter(CartProduct.cart_user_slug == current_user.slug).all()
        if carts:
            data = {
                "status" : 200,
                "message" : "Carts Retrieved",
                "user" : f"This products cart by {current_user.username}",
                "cart" : carts
            }
            return jsonable_encoder(data)
        else:
            return HTTPException(status_code=status.status.HTTP_404_NOT_FOUND, detail="Cart Not Found")
    except Exception as e:
        return HTTPException(status_code=status.status.HTTP_404_NOT_FOUND, detail="Bad Request")


@user_router.post('/create-cart')
async def user_post(cart: CartProductCreateSchema, Authorization: AuthJWT = Depends()):
    try:
        Authorization.jwt_required()
        existing_cart = session.query(Cart).filter_by(user_slug=cart.cart_user_slug).first()
        if not existing_cart:
            new_cart = Cart(user_slug=cart.cart_user_slug)
            session.add(new_cart)
            session.commit()

        existing_cart_product = session.query(CartProduct).filter_by(
            cart_user_slug=cart.cart_user_slug,
            product_slug=cart.product_slug
        ).first()

        if existing_cart_product:
            existing_cart_product.quantity += cart.quantity
        else:
            new_cart_product = CartProduct(
                cart_user_slug=cart.cart_user_slug,
                product_slug=cart.product_slug,
                quantity=cart.quantity,
            )
            session.add(new_cart_product)

        session.commit()

        data = {
            "status": 200,
            "message": "Product added to cart",
        }
        return jsonable_encoder(data)
    except Exception as e:
        session.rollback()
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@user_router.put('/cart/{product_slug}')
async def update_cart_item(product_slug: str, cart_item: CartProductUpdateSchema, Authorization: AuthJWT = Depends()):
    try:
        Authorization.jwt_required()
        current_user = session.query(User).filter(User.username == Authorization.get_jwt_subject()).first()


        cart_product = session.query(CartProduct).filter(
            CartProduct.cart_user_slug == current_user.slug,
            CartProduct.product_slug == product_slug
        ).first()

        if cart_product:
            cart_product.quantity = cart_item.quantity
            session.commit()
            return {"status": 200, "message": "Cart item updated successfully"}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad Request")


@user_router.delete('/cart/{product_slug}')
async def delete_cart_item(product_slug: str, Authorization: AuthJWT = Depends()):
    try:
        Authorization.jwt_required()
        current_user = session.query(User).filter(User.username == Authorization.get_jwt_subject()).first()

        if not current_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        cart_item = session.query(CartProduct).filter(
            CartProduct.cart_user_slug == current_user.slug,
            CartProduct.product_slug == product_slug
        ).first()

        if cart_item:
            session.delete(cart_item)
            session.commit()
            return {"status": 200, "message": "Cart item deleted successfully"}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad Request")
