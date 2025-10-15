from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.auth_utils import get_current_user
from app.models.user import User

router = APIRouter(prefix="/api/payments", tags=["payments"])

class PaymentIntent(BaseModel):
    amount: float
    currency: str = "usd"

class SubscriptionRequest(BaseModel):
    plan: str

@router.post("/create-intent")
def create_payment_intent(payload: PaymentIntent, current_user: User = Depends(get_current_user)):
    return {
        "client_secret": "mock_client_secret_123",
        "amount": payload.amount,
        "currency": payload.currency,
        "user_id": current_user.id
    }

@router.post("/subscribe")
def create_subscription(payload: SubscriptionRequest, current_user: User = Depends(get_current_user)):
    return {
        "subscription_id": "sub_mock_123",
        "plan": payload.plan,
        "status": "active",
        "user_id": current_user.id
    }

@router.get("/status")
def get_payment_status(current_user: User = Depends(get_current_user)):
    return {
        "user_id": current_user.id,
        "has_active_subscription": False,
        "payment_methods": []
    }
