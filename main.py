from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from uuid import uuid4
from datetime import datetime
import math
import os

app = FastAPI()

receipts = {}

class Item(BaseModel):
    shortDescription: str
    price: str

class Receipt(BaseModel):
    retailer: str
    purchaseDate: str
    purchaseTime: str
    items: list[Item]
    total: str

@app.get("/openapi.yaml", include_in_schema=False)
def get_openapi_yaml():
    yaml_path = os.path.join(os.path.dirname(__file__), "api.yml")
    if not os.path.exists(yaml_path):
        raise HTTPException(status_code=404, detail="OpenAPI file not found")
    return FileResponse(yaml_path, media_type="text/yaml")

def calculate_points(receipt: Receipt) -> int:
    points = 0
    points += sum(c.isalnum() for c in receipt.retailer)

    total_price = float(receipt.total)
    if total_price.is_integer():
        points += 50

    if total_price % 0.25 == 0:
        points += 25

    points += (len(receipt.items) // 2) * 5
    
    for item in receipt.items:
        description = item.shortDescription.strip()
        if len(description) % 3 == 0:
            item_price = float(item.price)
            points += math.ceil(item_price * 0.2)

    purchase_day = int(receipt.purchaseDate.split("-")[-1])
    if purchase_day % 2 == 1:
        points += 6

    purchase_time = datetime.strptime(receipt.purchaseTime, "%H:%M")
    if 14 <= purchase_time.hour < 16:
        points += 10

    return points

@app.post("/receipts/process")
def process_receipt(receipt: Receipt):
    receipt_id = str(uuid4())
    points = calculate_points(receipt)
    receipts[receipt_id] = points
    return {"id": receipt_id}

@app.get("/receipts/{id}/points")
def get_points(id: str):
    if id not in receipts:
        raise HTTPException(status_code=404, detail="Receipt not found")
    return {"points": receipts[id]}
