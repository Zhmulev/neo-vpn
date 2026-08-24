from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.models.server import VPNServer
from app.services.vpn_service import VPNService
import uuid

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
            if server.v2ray_config:
                config_str = server.v2ray_config
            else:
                # Генерируем новый конфиг через сервис (Этап 2: Провижининг)
                user_email = f"user-{uuid.uuid4().hex[:8]}"
                config_str = await VPNService.create_vless_user(
                    server_ip=server.endpoint,
                    port=server.port,
                    server_name=server.name,
                    user_email=user_email
                )
            return {
                "server_name": server.name,
                "country": server.country,
                "city": server.city,
                "protocol": protocol,
                "config": config_str
            }
    else:
        raise HTTPException(status_code=400, detail="Неверный протокол")