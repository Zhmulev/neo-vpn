from app.db.database import SessionLocal
from app.models.server import VPNServer

def seed_servers():
    db = SessionLocal()

    existing = db.query(VPNServer).first()
    if existing:
        print("Серверы уже добавлены. Удаляю старые...")
        db.query(VPNServer).delete()
        db.commit()

    servers = [
        {
            "name": "NL-Amsterdam-01",
            "country": "Нидерланды",
            "city": "Амстердам",
            "ip_address": "91.132.57.27",
            "port": 443,
            "endpoint": "91.132.57.27",
            "public_key": "2172b1eb-7113-467c-b5d7-a9db71ea0f77",
            "protocol": "vless",
            "v2ray_config": "vless://2172b1eb-7113-467c-b5d7-a9db71ea0f77@91.132.57.27:443?encryption=none&security=none&type=ws&path=%2Fneo#NEO-VPN-Amsterdam",
        },
    ]

    for s in servers:
        server = VPNServer(**s)
        db.add(server)

    db.commit()
    db.close()
    print(f"Добавлено {len(servers)} серверов!")

if __name__ == "__main__":
    seed_servers()