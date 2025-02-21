from fastapi import APIRouter, HTTPException
from .database import battery_table
from .models import Battery
from boto3.dynamodb.conditions import Attr

router = APIRouter()

@router.post("/batteries", response_model=dict)
def create_battery(battery: Battery):
    try:
        battery_table.put_item(Item=battery.dict())
        return {"message": "Battery added successfully", "batteryId": battery.batteryId}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/batteries/{batteryId}", response_model=Battery)
def get_battery(batteryId: str):
    response = battery_table.get_item(Key={"batteryId": batteryId})
    if "Item" not in response:
        raise HTTPException(status_code=404, detail="Battery not found")
    return response["Item"]

@router.get("/batteries/search", response_model=list)
def search_batteries(capacity: float = None, voltage: float = None):
    filters = []
    if capacity:
        filters.append(Attr("capacity").gte(capacity))
    if voltage:
        filters.append(Attr("voltage").eq(voltage))

    filter_expression = None
    if filters:
        filter_expression = filters[0]
        for condition in filters[1:]:
            filter_expression &= condition

    response = battery_table.scan(FilterExpression=filter_expression) if filters else battery_table.scan()
    return response.get("Items", [])
