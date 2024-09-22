from fastapi import APIRouter, HTTPException, status
from database import Base, Engine, Session
from fastapi.encoders import jsonable_encoder
from models import Delivery, Order, Product
from schemas import DeliveryCreateSchema, DeliveryUpdateSchema



session = Session(bind=Engine)

delivery_person_router = APIRouter(prefix="/delivery_person", tags=["delivery_person"])


@delivery_person_router.get('/')
async def get_delivery_person():
    delivery_person = session.query(Delivery).all()
    if not delivery_person:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No delivery")
    else:
        data = {
            "status": 200,
            "delivery_person": delivery_person
        }
    return jsonable_encoder(data)


@delivery_person_router.post('/create')
async def create_delivery_person(delivery_person: DeliveryCreateSchema):
    try:
        new_delivery_person = Delivery(
            name=delivery_person.name,
            delivery_category=delivery_person.delivery_category,
        )
        session.add(new_delivery_person)
        session.commit()
        data = {
            "status": 201,
            "message": "DeliveryPerson created"
        }
        return jsonable_encoder(data)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad Request")


@delivery_person_router.put('/{delivery_person_slug}')
async def update_delivery_person(deliv : DeliveryUpdateSchema, delivery_person_slug):
    try:
        person = session.query(Delivery).filter(Delivery.slug == delivery_person_slug).first()
        if person:
            for key, value in deliv.__dict__.items():
                setattr(person, key, value)
                session.commit()
                data = {
                    "status": 200,
                    "message": "DeliveryPerson updated"
                }
                return jsonable_encoder(data)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No delivery")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad Request")


@delivery_person_router.delete('/{delivery_person_slug}')
async def delete_delivery_person(delivery_person_slug: str):
    try:
        delivery_person = session.query(Delivery).filter(Delivery.slug == delivery_person_slug).first()
        if delivery_person:
            session.delete(delivery_person)
            session.commit()
            data = {
                "status": 200,
                "message": "DeliveryPerson deleted"
            }
            return jsonable_encoder(data)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No delivery")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad Request")


@delivery_person_router.get('/orders/{delivery_person_slug}')
async def get_delivery_person_orders(delivery_person_slug: str):
    try:
        order = session.query(Order).filter(Order.delivery_person == delivery_person_slug).first()
        if order:
            data = {
                "status": 200,
                "order": order
            }
            return jsonable_encoder(data)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No order")

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad Request")