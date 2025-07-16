from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from yookassa import Payment, Configuration
import uuid
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Настройка ЮKassa
Configuration.account_id = os.getenv("YOOKASSA_SHOP_ID")
Configuration.secret_key = os.getenv("YOOKASSA_SECRET_KEY")

class PaymentRequest(BaseModel):
    amount: float
    currency: str = "RUB"
    description: str

@app.post("/payment")
async def create_payment(payment: PaymentRequest):
    idempotence_key = str(uuid.uuid4())
    try:
        response = Payment.create({
            "amount": {
                "value": f"{payment.amount:.2f}",
                "currency": payment.currency
            },
            "confirmation": {
                "type": "redirect",
                "return_url": "https://your-redirect-url.com"
            },
            "capture": True,
            "description": payment.description
        }, idempotence_key)
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Hello World"}