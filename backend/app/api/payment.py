from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.db.database import get_db
from app.models.user import User
from app.schemas.user import BalanceTopUp, SubscribeRequest

router = APIRouter(prefix="/payment", tags=["payment"])

# Тарифная сетка
PRICES = {
    "basic": {
        "day": 5,
        "week": 29,
        "month": 99,
        "three_months": 249,
        "six_months": 449,
    },
    "pro": {
        "day": 9,
        "week": 59,
        "month": 199,
        "three_months": 499,
        "six_months": 899,
    }
}

PERIOD_DAYS = {
    "day": 1,
    "week": 7,
    "month": 30,
    "three_months": 90,
    "six_months": 180,
}

@router.post("/topup")
async def topup_balance(data: BalanceTopUp, db: Session = Depends(get_db)):
    """Пополнение баланса"""
    user = db.query(User).filter(User.id == data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    user.balance += data.amount
    db.commit()
    db.refresh(user)
    return {"balance": user.balance, "message": f"Баланс пополнен на {data.amount}₽"}

@router.get("/balance/{user_id}")
async def get_balance(user_id: int, db: Session = Depends(get_db)):
    """Проверить баланс"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return {"balance": user.balance, "auto_renew": user.auto_renew}

@router.post("/subscribe")
async def subscribe(data: SubscribeRequest, db: Session = Depends(get_db)):
    """Активировать подписку"""
    user = db.query(User).filter(User.id == data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    if data.plan not in PRICES:
        raise HTTPException(status_code=400, detail="Неверный тариф")

    if data.period not in PERIOD_DAYS:
        raise HTTPException(status_code=400, detail="Неверный период")

    price = PRICES[data.plan][data.period]
    days = PERIOD_DAYS[data.period]

    if user.balance < price:
        raise HTTPException(status_code=400, detail=f"Недостаточно средств. Нужно {price}₽, на балансе {user.balance}₽")

    user.balance -= price
    user.subscription_plan = data.plan
    user.auto_renew = data.auto_renew

    # Продлеваем подписку
    now = datetime.utcnow()
    if user.subscription_end and user.subscription_end > now:
        user.subscription_end = user.subscription_end + timedelta(days=days)
    else:
        user.subscription_end = now + timedelta(days=days)

    db.commit()
    db.refresh(user)
    return {
        "message": f"Подписка {data.plan} активирована на {days} дней",
        "balance": user.balance,
        "subscription_end": user.subscription_end,
        "plan": user.subscription_plan,
    }

@router.get("/prices")
async def get_prices():
    """Тарифная сетка"""
    return PRICES