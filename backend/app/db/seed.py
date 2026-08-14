from app.db.database import SessionLocal
from app.models.server import VPNServer

def seed_servers():
    db = SessionLocal()

    # Проверяем, есть ли уже серверы
    existing = db.query(VPNServer).first()
    if existing:
        print("Серверы уже добавлены, пропускаем.")
        db.close()
        return

    servers = [
        {
            "name": "NL-Amsterdam-01",
            "country": "Нидерланды",
            "city": "Амстердам",
            "ip_address": "1.2.3.4",
            "port": 51820,
            "endpoint": "nl1.yourvpn.com",
            "public_key": "PLACEHOLDER_KEY_NL",
        },
        {
            "name": "US-NewYork-01",
            "country": "США",
            "city": "Нью-Йорк",
            "ip_address": "5.6.7.8",
            "port": 51820,
            "endpoint": "us1.yourvpn.com",
            "public_key": "PLACEHOLDER_KEY_US",
        },
        {
            "name": "SG-Singapore-01",
            "country": "Сингапур",
            "city": "Сингапур",
            "ip_address": "9.10.11.12",
            "port": 51820,
            "endpoint": "sg1.yourvpn.com",
            "public_key": "PLACEHOLDER_KEY_SG",
        },
    ]

    for s in servers:
        server = VPNServer(**s)
        db.add(server)

    db.commit()
    db.close()
    print(f"Добавлено {len(servers)} тестовых серверов!")

if __name__ == "__main__":
    seed_servers()