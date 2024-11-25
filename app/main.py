from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict
import uuid
from math import ceil
from datetime import datetime

# Init App
app = FastAPI(
  title="Receipt Processor Webservice",
  description="A simple receipt processor",
  vesrion="1.0.0",
)

# In-Memory Store for receipts -> use a dictionary/map with Uid as key & receipt as value
receipt_store: Dict[str, dict] = {}

# Define Data Classes
class Item(BaseModel):
  shortDescription: str = Field(..., example="Mountain Dew 12PK")
  price: str = Field(..., example="6.49")

class Receipt(BaseModel):
  retailer: str = Field(..., example="Target")
  purchaseDate: str = Field(..., example="2022-01-01")
  purchaseTime: str = Field(..., example="13:01")
  items: List[Item]
  total: str = Field(..., example="35.35")

class ReceiptResponse(BaseModel):
  id: str = Field(..., example="adb6b560-0eef-42bc-9d16-df48f30e89b2")


# Endpoints
@app.post("/receipts/process",
          response_model=ReceiptResponse,
          summary="Submits a receipt for processing",
          description="Submits a receipt for processing",
          status_code=status.HTTP_200_OK,
          responses={
        400: {
            "description": "The receipt is invalid",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "detail": {"type": "string", "example": "Invalid receipt data"}
                        },
                    }
                }
            },
        }
    }
          )
def processReceipt(receipt: Receipt):

  # Basic validation -> If the no (retailer name or purchase date or purchase time) or no items -> throw Ex -> Send 400
  try:
    #for char in retailer_name:
    if not receipt.retailer:
      raise ValueError("No retailer name")
    if not receipt.purchaseDate:
      raise ValueError("No purchase date")
    if not receipt.purchaseTime:
      raise ValueError("No purchase time")
    if len(receipt.items)==0:
      raise ValueError("No items in request")
  except ValueError as e:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail="Invalid request data: " + str(e),
    )

  # Generate a Unique Id
  receipt_id = str(uuid.uuid4())

  # Store generated receipt in memory
  receipt_store[receipt_id] = receipt.dict()

  #print(receipt_store)

  # Return response
  return {"id": receipt_id}

@app.get(
  "/receipts/{id}/points",
  summary="Get points for a receipt",
  description="Looks up the receipt by ID and returns the number of points awarded.",
  status_code=status.HTTP_200_OK,
  responses={
        404: {
            "description": "Receipt not found",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "detail": {"type": "string", "example": "Receipt not found"}
                        },
                    }
                }
            },
        }
    },
  )
def getPoints(id: str):
  # If receipt is not present in receipt store -> throw error and send 404 status code
  try:
    receipt = receipt_store.get(id)
    if not receipt:
      raise ValueError("Invalid retailer name")
  except ValueError as e:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="Receipt not found with Id: " + id,
    )
  points = calculatePoints(receipt)

  return {"points": points}

def calculatePoints(receipt):
  points = 0
  # 1. One point for every alphanumeric character in the retailer name.
  points += sum(1 for char in receipt["retailer"] if char.isalnum())


  # 2. 50 points if the total is a round dollar amount with no cents.
  total = float(receipt["total"])
  if total.is_integer():
    points += 50

  # 3. 25 points if the total is a multiple of 0.25.
  if total % 0.25 == 0:
    points += 25

  # 4. 5 points for every two items on the receipt.
  points += (len(receipt["items"]) // 2) * 5

  # 5. Points based on the item description length.
  for item in receipt["items"]:
    trimmed_length = len(item["shortDescription"].strip())
    if trimmed_length % 3 == 0:
      price_points = ceil(float(item["price"]) * 0.2)
      points += price_points

  # 6. 6 points if the day in the purchase date is odd.
  purchase_date = datetime.strptime(receipt["purchaseDate"], "%Y-%m-%d")
  if purchase_date.day % 2 == 1:
    points += 6

  # 7. 10 points if the purchase time is between 2:00pm and 4:00pm.
  purchase_time = datetime.strptime(receipt["purchaseTime"], "%H:%M").time()
  if purchase_time >= datetime.strptime("14:00", "%H:%M").time() and purchase_time < datetime.strptime("16:00", "%H:%M").time():
    points += 10

  return points
