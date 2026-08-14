from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from datetime import datetime, timedelta
from app.db.database import Base

class ProxyConfig(Base):
    __tablename__ = "proxy_configs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    server_id = Column(Integer, ForeignKey("vpn_servers.id"))
    proxy_type = Column(String, default="socks5")  # socks5 или http
    proxy_login = Column(String)
    proxy_password = Column(String)
    local_port = Column(Integer)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, default=lambda: datetime.utcnow() + timedelta(days=30))