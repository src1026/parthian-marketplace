from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .database import get_db
from .models import Order
from event_bus.publisher import publish_event

router = APIRouter()


@router.post("/orders/")
def place_order(order_data: dict, db: Session = Depends(get_db)):
    order = Order(**order_data)
    db.add(order)
    db.commit()

    publish_event("OrderPlaced", {"orderId": order.id, "batteryId": order.battery_id})
    return {"message": "Order placed successfully"}
