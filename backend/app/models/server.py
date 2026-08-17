from sqlalchemy import Column, Integer, String, Boolean, Float, Text
from app.db.database import Base

class VPNServer(Base):
    __tablename__ = "vpn_servers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    country = Column(String)
    city = Column(String)
    ip_address = Column(String)
    port = Column(Integer, default=51820)
    public_key = Column(String)
    endpoint = Column(String)
    protocol = Column(String, default="wireguard")  # wireguard, vless, vmess
    v2ray_config = Column(Text, nullable=True)  # JSON с V2Ray конфигурацией
    is_active = Column(Boolean, default=True)
    load = Column(Float, default=0.0)
    max_users = Column(Integer, default=100)