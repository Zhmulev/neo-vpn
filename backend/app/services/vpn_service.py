import uuid

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
    async def create_vless_user(server_ip: str, port: int, server_name: str) -> str:
        """
        Создает VLESS пользователя и возвращает конфиг.
        """
        # TODO: Интеграция с реальным API
        new_uuid = str(uuid.uuid4())
        config = f"vless://{new_uuid}@{server_ip}:{port}?encryption=none&security=none&type=ws&path=%2Fneo#NEO-VPN-{server_name}"
        return config