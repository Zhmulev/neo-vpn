from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.db.database import get_db
from app.models.proxy import ProxyConfig
from app.models.server import VPNServer
from app.models.user import User
from app.core.security import generate_proxy_credentials
from app.services.vpn_service import VPNService

router = APIRouter(prefix="/proxy", tags=["proxy"])

@router.post("/create")
async def create_proxy(
    user_id: int,
    server_id: int,
    proxy_type: str = "socks5",
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    server = db.query(VPNServer).filter(VPNServer.id == server_id).first()
    if not server:
        raise HTTPException(status_code=404, detail="Сервер не найден")

    active_proxies = db.query(ProxyConfig).filter(
        ProxyConfig.user_id == user_id,
        ProxyConfig.is_active == True
    ).count()

    if active_proxies >= user.proxy_limit:
        raise HTTPException(
            status_code=400,
            detail=f"Лимит прокси ({user.proxy_limit}) исчерпан"
        )

    login, password = generate_proxy_credentials()

    # Реальные порты прокси
    socks_port = 1081
    http_port = 1080

    proxy = ProxyConfig(
        user_id=user_id,
        server_id=server_id,
        proxy_type=proxy_type,
        proxy_login=login,
        proxy_password=password,
        local_port=socks_port if proxy_type == "socks5" else http_port,
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
                "proxy_string": await VPNService.create_proxy_user(
                    server_ip=server.ip_address,
                    proxy_type=proxy_type,
                    login=login,
                    password=password,
                    port=proxy.local_port
                ),
        "expires_at": proxy.expires_at
    }

@router.get("/my")
async def get_my_proxies(user_id: int, db: Session = Depends(get_db)):
    proxies = db.query(ProxyConfig).filter(
        ProxyConfig.user_id == user_id,
        ProxyConfig.is_active == True
    ).all()
    return proxies

@router.delete("/{proxy_id}")
async def delete_proxy(proxy_id: int, user_id: int, db: Session = Depends(get_db)):
    proxy = db.query(ProxyConfig).filter(
        ProxyConfig.id == proxy_id,
        ProxyConfig.user_id == user_id
    ).first()

    if not proxy:
        raise HTTPException(status_code=404, detail="Прокси не найден")

    proxy.is_active = False
    db.commit()
    return {"status": "ok", "message": "Прокси удалён"}