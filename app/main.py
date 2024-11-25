from fastapi import FastAPI, status
from pydantic import BaseModel, Field
from typing import List, Dict
import uuid

# Init App
app = FastAPI(
  title="Receipt Processor Webservice",
  description="A simple receipt processor",
  vesrion="1.0.0",
)

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
          )
def processReceipt(receipt: Receipt):


  # Generate a Unique Id
  receipt_id = str(uuid.uuid4())

  # Return response
  return {"id": receipt_id}