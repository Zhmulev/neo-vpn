from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    is_active: bool
    balance: float
    auto_renew: bool
    subscription_plan: str
    subscription_end: Optional[datetime] = None
    trial_end: Optional[datetime] = None
    proxy_enabled: bool

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: Optional[int] = None
    username: Optional[str] = None
    trial_end: Optional[datetime] = None

class BalanceTopUp(BaseModel):
    user_id: int
    amount: float

class SubscribeRequest(BaseModel):
    user_id: int
    plan: str  # basic, pro
    period: str  # day, week, month, three_months, six_months
    auto_renew: bool = False