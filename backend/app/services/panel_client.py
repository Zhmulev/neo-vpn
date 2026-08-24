import httpx
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

class XrayPanelClient:
    """
    Клиент для взаимодействия с API панели 3x-ui.
    """
    def __init__(self):
        self.base_url = settings.PANEL_URL.rstrip('/')
        self.username = settings.PANEL_USERNAME
        self.password = settings.PANEL_PASSWORD
        self._cookies = None

    async def _ensure_auth(self):
        if not self._cookies:
            await self.login()

    async def login(self):
        async with httpx.AsyncClient() as client:
            resp = await client.post(f"{self.base_url}/login", data={
                "username": self.username,
                "password": self.password
            })
            if resp.status_code == 200 and resp.json().get("success"):
                self._cookies = resp.cookies
                logger.info("Successfully logged into 3x-ui panel")
                return True
            logger.error("Failed to login to 3x-ui panel")
            return False

    async def add_client(self, inbound_id: int, email: str, uuid: str, flow: str = ""):
        await self._ensure_auth()
        async with httpx.AsyncClient(cookies=self._cookies) as client:
            payload = {
                "id": inbound_id,
                "settings": {
                    "clients": [
                        {
                            "id": uuid,
                            "flow": flow,
                            "email": email,
                            "limitIp": 0,
                            "totalGB": 0,
                            "expiryTime": 0,
                            "enable": True,
                            "tgId": "",
                            "subId": ""
                        }
                    ]
                }
            }
            resp = await client.post(f"{self.base_url}/panel/api/inbounds/addClient", json=payload)
            data = resp.json()
            if data.get("success"):
                logger.info(f"Client {email} added to inbound {inbound_id}")
            else:
                logger.error(f"Failed to add client {email}: {data.get('msg')}")
            return data

    async def delete_client(self, inbound_id: int, uuid: str):
        await self._ensure_auth()
        async with httpx.AsyncClient(cookies=self._cookies) as client:
            resp = await client.post(f"{self.base_url}/panel/api/inbounds/{inbound_id}/delClient", json={"uuid": uuid})
            return resp.json()

panel_client = XrayPanelClient()