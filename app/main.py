from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict
import uuid

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

  # Basic validation -> If the retailer name doesn't have alpha-numeric characters -> throw Ex -> Send 400
  try:
    retailer_name = receipt.retailer
    for char in retailer_name:
      if not char.isalnum():
        raise ValueError("Invalid retailer name")
  except ValueError as e:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail="Invalid request data: " + str(e),
    )

  # Generate a Unique Id
  receipt_id = str(uuid.uuid4())

  # Store generated receipt in memory
  receipt_store[receipt_id] = receipt.dict()

  print(receipt_store)

  # Return response
  return {"id": receipt_id}

@app.get(
  "/receipts/{id}/points",
  summary="Get points for a receipt",
  description="Looks up the receipt by ID and returns the number of points awarded.",
  status_code=status.HTTP_200_OK,
  )
def getPoints(id: str):
  try:
    receipt = receipt_store.get(id)
    if not receipt:
      raise ValueError("Invalid retailer name")
  except ValueError as e:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="Receipt not found with Id: " + id,
    )
  points = 0
  return {"points": points}