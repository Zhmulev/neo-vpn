from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.db.database import get_db
from app.models.proxy import ProxyConfig
from app.models.server import VPNServer
from app.models.user import User
from app.core.security import generate_proxy_credentials

router = APIRouter(prefix="/proxy", tags=["proxy"])

@router.post("/create")
async def create_proxy(
    user_id: int,
    server_id: int,
    proxy_type: str = "socks5",
    db: Session = Depends(get_db)
):
    """Создать прокси для пользователя"""
    # Проверяем пользователя
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    # Проверяем сервер
    server = db.query(VPNServer).filter(VPNServer.id == server_id).first()
    if not server:
        raise HTTPException(status_code=404, detail="Сервер не найден")

    # Проверяем лимит прокси
    active_proxies = db.query(ProxyConfig).filter(
        ProxyConfig.user_id == user_id,
        ProxyConfig.is_active == True
    ).count()

    if active_proxies >= user.proxy_limit:
        raise HTTPException(
            status_code=400,
            detail=f"Лимит прокси ({user.proxy_limit}) исчерпан"
        )

    # Генерируем учетные данные
    login, password = generate_proxy_credentials()

    proxy = ProxyConfig(
        user_id=user_id,
        server_id=server_id,
        proxy_type=proxy_type,
        proxy_login=login,
        proxy_password=password,
        local_port=1080 + user_id,  # Уникальный порт для пользователя
        expires_at=datetime.utcnow() + timedelta(days=30)
    )

    db.add(proxy)
    db.commit()
    db.refresh(proxy)

    return {
        "id": proxy.id,
        "proxy_type": proxy.proxy_type,
        "server": server.name,
        "country": server.country,
        "proxy_address": f"{server.ip_address}:{proxy.local_port}",
        "proxy_login": login,
        "proxy_password": password,
        "proxy_string": f"{proxy_type}://{login}:{password}@{server.ip_address}:{proxy.local_port}",
        "expires_at": proxy.expires_at
    }

@router.get("/my")
async def get_my_proxies(user_id: int, db: Session = Depends(get_db)):
    """Список прокси пользователя"""
    proxies = db.query(ProxyConfig).filter(
        ProxyConfig.user_id == user_id,
        ProxyConfig.is_active == True
    ).all()
    return proxies

@router.delete("/{proxy_id}")
async def delete_proxy(proxy_id: int, user_id: int, db: Session = Depends(get_db)):
    """Удалить прокси"""
    proxy = db.query(ProxyConfig).filter(
        ProxyConfig.id == proxy_id,
        ProxyConfig.user_id == user_id
    ).first()

    if not proxy:
        raise HTTPException(status_code=404, detail="Прокси не найден")

    proxy.is_active = False
    db.commit()
    return {"status": "ok", "message": "Прокси удалён"}