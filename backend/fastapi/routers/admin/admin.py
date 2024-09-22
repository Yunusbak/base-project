from fastapi import APIRouter, HTTPException, status, Depends
from database import Session, Engine
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder
from schemas import ProductUpdateSchema, ProductCreateSchema, CategoryCreateSchema, CheckAdminSchema
from models import Product, User, Category


session = Session(bind=Engine)
admin_router = APIRouter(prefix="/admin", tags=["ADMIN PAGE"])


def admin_required(admin: AuthJWT):
    admin.jwt_required()
    admin_slug = admin.get_jwt_subject()            # TOKEN ADMINGA TEGISHLI EKANKIGINI TEKSHIRADI
    if admin_slug != 'yunus':
        raise HTTPException(status_code=403, detail="Admin qismini faqat adminlar boshqaradi")

# Admin routes
@admin_router.get("/")
async def admin(admin: AuthJWT = Depends()):
    try:
        admin_required(admin)
        return {"message": "This is the admin page"}
    except Exception as e:
        return {"message": "Faqat admin ko'ra oladi"}



#----------------------------------------------------------

# ADMIN PRODUCT [--CATEGORY--]  MANAGEMENT


@admin_router.post("/create-category")
async def create_category(category: CategoryCreateSchema, admin: AuthJWT = Depends()):
    try:
        admin_required(admin)
        check_category = session.query(Category).filter(Category.name == category.name).first()
        if check_category:
            data = {
                "status": 400,
                "message": "Category already exists"
            }
            return jsonable_encoder(data)

        new_category = Category(name=category.name)
        session.add(new_category)
        session.commit()
        data = {
            "status": 201,
            "message": "Category created"
        }
        return jsonable_encoder(data)

    except Exception as e:
        raise HTTPException(status_code=400, detail="Bad Request")

@admin_router.delete("/category/{category_slug}")
async def delete_category(category_slug: str, admin: AuthJWT = Depends()):
    try:
        admin_required(admin)
        category = session.query(Category).filter(Category.slug == category_slug).first()
        if category:
            session.delete(category)
            session.commit()
            data = {
                "status": 200,
                "message": "Category deleted"
            }
            return jsonable_encoder(data)
        else:
            data = {
                "status": 404,
                "message": "Category not found"
            }
            return jsonable_encoder(data)

    except Exception as e:
        raise HTTPException(status_code=400, detail="Bad Request")

@admin_router.get("/categories")
async def categories(admin: AuthJWT = Depends()):
    try:
        admin_required(admin)
        categories = session.query(Category).all()
        if categories:
            data = {
                "status": 200,
                "message": "Category list",
                "categories": jsonable_encoder(categories)
            }
            return data
        else:
            data = {
                "status": 404,
                "message": "Category not found"
            }
            return jsonable_encoder(data)

    except Exception as e:
        raise HTTPException(status_code=400, detail="Bad Request")


@admin_router.get("/category/{category_slug}")
async def category(category_slug: str, admin: AuthJWT = Depends()):
    try:
        admin_required(admin)
        category = session.query(Category).filter(Category.slug == category_slug).first()
        if category:
            data = {
                "status": 200,
                "message": "Category found",
                "category": jsonable_encoder(category)
            }
            return data
        else:
            data = {
                "status": 404,
                "message": "Category not found"
            }
            return jsonable_encoder(data)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Bad Request")


#---------------------------------------------------------------------------------

# ADMIN MANAGEMENT PRODUCTS

@admin_router.post("/create-product")
async def create_product(product: ProductCreateSchema, admin: AuthJWT = Depends()):
    try:
        admin_required(admin)
        check_product = session.query(Product).filter(Product.name == product.name).first()
        if check_product:
            data = {
                "status": 400,
                "message": "Product already exists"
            }
            return jsonable_encoder(data)

        category = session.query(Category).filter(Category.slug == product.category_slug).first()
        if not category:
            data = {
                "status": 404,
                "message": "Category not found"
            }
            return jsonable_encoder(data)

        new_product = Product(
            name=product.name,
            price=product.price
        )
        new_product.category = category
        session.add(new_product)
        session.commit()

        data = {
            "status": 201,
            "message": "Product created"
        }
        return jsonable_encoder(data)

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad Request")



@admin_router.put("/update-product/{product_slug}")
async def update_product(product_slug: str, product: ProductUpdateSchema, admin: AuthJWT = Depends()):
    try:
        admin_required(admin)
        check_product = session.query(Product).filter(Product.slug == product_slug).first()
        if check_product:
            for key, value in product.__dict__.items():
                setattr(check_product, key, value)
                session.commit()
            data = {
                "status": 200,
                "message": "Product updated"
            }
            return jsonable_encoder(data)
        else:
            return jsonable_encoder({"status": 400, "message": "Product not found"})
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad Request")

@admin_router.get('/product/{product_slug}')
async def product_detail(product_slug: str, admin: AuthJWT = Depends()):
    try:
        admin_required(admin)
        check_product = session.query(Product).filter(Product.slug == product_slug).first()
        if check_product:
            data = {
                "status": 200,
                "message": "Product details",
                "Product": check_product
            }
            return jsonable_encoder(data)
        else:
            return jsonable_encoder({"status": 400, "message": "Product not found"})
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad Request")

@admin_router.delete("/delete-product/{product_slug}")
async def delete_product(product_slug: str, admin: AuthJWT = Depends()):
    try:
        admin_required(admin)
        check_product = session.query(Product).filter(Product.slug == product_slug).first()
        if check_product:
            session.delete(check_product)
            session.commit()
            data = {
                "status": 200,
                "message": "Product deleted"
            }
            return jsonable_encoder(data)
        else:
            return jsonable_encoder({"status": 400, "message": "Product not found"})
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad Request")

@admin_router.get('/products')
async def products(admin: AuthJWT = Depends()):
    try:
        admin.jwt_required()
        products = session.query(Product).all()
        if products:
            data = {
                "status": 200,
                "products": products
            }
            return jsonable_encoder(data)
        else:
            return jsonable_encoder({"status": 404, "message": "No products found"})
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad Request")



# -----------------------------------------------------------------------------------------------



# ADMIN [-- USERS --] MANAGEMENT



@admin_router.get('/users')
async def get_users(admin: AuthJWT = Depends()):
    try:
        admin_required(admin)
        users = session.query(User).all()
        if users:
            data = {
                "status": 200,
                "users": users
            }
            return jsonable_encoder(data)
        else:
            return jsonable_encoder({"status": 400, "message": "Users not found"})
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad Request")


@admin_router.delete('/delete-user/{user_slug}')
async def delete_user(user_slug: str, admin: AuthJWT = Depends()):
    admin_required(admin)
    try:
        check_user = session.query(User).filter(User.slug == user_slug).first()
        if check_user:
            session.delete(check_user)
            session.commit()
            data = {
                "status": 200,
                "message": "User deleted"
            }
            return jsonable_encoder(data)
        else:
            return jsonable_encoder({"status": 400, "message": "User not found"})
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad Request")
