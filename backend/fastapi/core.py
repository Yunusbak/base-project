from fastapi import FastAPI
from fastapi_jwt_auth import AuthJWT
from schemas import Settings
from routers.user.user import user_router
from routers.admin.admin import admin_router
from routers.user.delivery_person import delivery_person_router
app = FastAPI()

@AuthJWT.load_config
def get_config():
    return Settings()

app.include_router(user_router)
app.include_router(admin_router)
app.include_router(delivery_person_router)

@app.get('/')
async def root():
    return {"message" : "Welcome to Store"}