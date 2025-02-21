from fastapi import APIRouter
import requests

router = APIRouter()

@router.get("/users/{user_id}")
def get_user(user_id: int):
    response = requests.get(f"http://user_service:8001/users/{user_id}")
    return response.json()

@router.get("/batteries/{battery_id}")
def get_battery(battery_id: str):
    response = requests.get(f"http://battery_service:8002/batteries/{battery_id}")
    return response.json()
