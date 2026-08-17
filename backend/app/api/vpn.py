from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.models.server import VPNServer

router = APIRouter(prefix="/vpn", tags=["vpn"])

@router.get("/servers")
async def get_servers(db: Session = Depends(get_db)):
    servers = db.query(VPNServer).filter(VPNServer.is_active == True).all()
    return servers

@router.get("/config/{server_id}")
async def get_config(server_id: int, protocol: str = "wireguard", db: Session = Depends(get_db)):
    server = db.query(VPNServer).filter(VPNServer.id == server_id).first()
    if not server:
        raise HTTPException(status_code=404, detail="Сервер не найден")

    if protocol == "wireguard":
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
            "protocol": "wireguard",
            "config": config
        }
    elif protocol == "vless" or protocol == "vmess":
        if not server.v2ray_config:
            raise HTTPException(status_code=404, detail="V2Ray конфиг не настроен для этого сервера")
        return {
            "server_name": server.name,
            "country": server.country,
            "city": server.city,
            "protocol": protocol,
            "config": server.v2ray_config
        }
    else:
        raise HTTPException(status_code=400, detail="Неверный протокол")