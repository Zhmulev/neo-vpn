import uuid
import logging
from app.services.panel_client import panel_client
from app.core.config import settings

logger = logging.getLogger(__name__)

class VPNService:
    """
    Абстракция над VPN/Proxy инфраструктурой.
    В будущем здесь будет вызов API панели (3x-ui / Marzban).
    """

    @staticmethod
    async def create_proxy_user(server_ip: str, proxy_type: str, login: str, password: str, port: int) -> str:
        """
        Создает пользователя прокси на сервере.
        Возвращает строку подключения.
        """
        # TODO: Интеграция с реальным API (3x-ui / Xray)
        if proxy_type == "socks5":
            return f"socks5://{login}:{password}@{server_ip}:{port}"
        elif proxy_type == "http":
            return f"http://{login}:{password}@{server_ip}:{port}"
        return f"{proxy_type}://{login}:{password}@{server_ip}:{port}"

    @staticmethod
    async def create_vless_user(server_ip: str, port: int, server_name: str, user_email: str = None) -> str:
        """
        Создает VLESS пользователя на сервере через API панели и возвращает конфиг.
        """
        new_uuid = str(uuid.uuid4())
        email = user_email or f"neo-{new_uuid[:8]}"

        try:
            inbound_id = settings.DEFAULT_VLESS_INBOUND_ID
            await panel_client.add_client(inbound_id=inbound_id, email=email, uuid=new_uuid)
        except Exception as e:
            logger.error(f"Failed to provision VLESS user on panel: {e}")
            # Fallback: возвращаем конфиг, но на панели юзера может не быть

        config = f"vless://{new_uuid}@{server_ip}:{port}?encryption=none&security=none&type=ws&path=%2Fneo#NEO-VPN-{server_name}"
        return config