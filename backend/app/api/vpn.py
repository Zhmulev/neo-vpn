from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.models.server import VPNServer

router = APIRouter(prefix="/vpn", tags=["vpn"])

@router.get("/servers")
async def get_servers(db: Session = Depends(get_db)):
    """Список всех активных VPN-серверов"""
    servers = db.query(VPNServer).filter(VPNServer.is_active == True).all()
    return servers

@router.get("/config/{server_id}")
async def get_config(server_id: int, db: Session = Depends(get_db)):
    """Получить WireGuard конфиг для сервера"""
    server = db.query(VPNServer).filter(VPNServer.id == server_id).first()
    if not server:
        raise HTTPException(status_code=404, detail="Сервер не найден")

    config = f"""# {server.name} - {server.country}, {server.city}
[Interface]
PrivateKey = ВСТАВЬ_СВОЙ_ПРИВАТНЫЙ_КЛЮЧ
Address = 10.0.0.2/24
DNS = 1.1.1.1, 8.8.8.8

[Peer]
PublicKey = {server.public_key}
Endpoint = {server.endpoint}:{server.port}
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25
"""
    return {
        "server_name": server.name,
        "country": server.country,
        "city": server.city,
        "config": config
    }