from fastapi import APIRouter, HTTPException
from database import battery_table, s3_client, S3_BUCKET
from models import Battery
from boto3.dynamodb.conditions import Attr
from fastapi import File, UploadFile
import boto3

router = APIRouter()

@router.get("/batteries", response_model=list)
def list_all_batteries():
    response = battery_table.scan()
    return response.get("Items", [])

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

@router.get("/batteries/{batteryId}", response_model=Battery)
def get_battery(batteryId: str):
    response = battery_table.get_item(Key={"batteryId": batteryId})
    if "Item" not in response:
        raise HTTPException(status_code=404, detail="Battery not found")
    return response["Item"]

@router.post("/batteries", response_model=dict)
def create_battery(battery: Battery):
    try:
        battery_table.put_item(Item=battery.dict())
        return {"message": "Battery added successfully", "batteryId": battery.batteryId}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/batteries/{battery_id}/upload-image")
async def upload_image(battery_id: str, file: UploadFile = File(...)):
    import uuid
    try:
        file_extension = file.filename.split(".")[-1]
        s3_key = f"batteries/{battery_id}/{uuid.uuid4()}.{file_extension}"

        s3_client.upload_fileobj(file.file, S3_BUCKET, s3_key)
        print(boto3.client("sts").get_caller_identity())
        file_url = f"https://{S3_BUCKET}.s3.amazonaws.com/{s3_key}"

        battery_table.update_item(
            Key={"batteryId": battery_id},
            UpdateExpression="SET imageUrl = :url",
            ExpressionAttributeValues={":url": file_url}
        )

        return {"message": "Upload successful", "url": file_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")
