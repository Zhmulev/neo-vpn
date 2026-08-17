#!/bin/bash

# ============================================
# NEO VPN - Установка Xray (VLESS + WebSocket)
# Запуск: bash install_xray.sh
# ============================================

set -e

echo "======================================"
echo "  NEO VPN - Установка Xray"
echo "======================================"

# 1. Обновление системы
echo "[1/6] Обновление системы..."
apt update -y && apt upgrade -y

# 2. Установка зависимостей
echo "[2/6] Установка зависимостей..."
apt install -y curl wget unzip nginx

# 3. Установка Xray
echo "[3/6] Установка Xray..."
bash -c "$(curl -L https://github.com/XTLS/Xray-install/raw/main/install-release.sh)" @ install

# 4. Генерация UUID
echo "[4/6] Генерация UUID..."
UUID=$(cat /proc/sys/kernel/random/uuid)
echo "UUID: $UUID"

# 5. Создание конфигурации
echo "[5/6] Создание конфигурации..."
cat > /usr/local/etc/xray/config.json << EOF
{
  "inbounds": [
    {
      "port": 443,
      "protocol": "vless",
      "settings": {
        "clients": [
          {
            "id": "$UUID",
            "flow": "xtls-rprx-vision"
          }
        ],
        "decryption": "none"
      },
      "streamSettings": {
        "network": "ws",
        "security": "tls",
        "wsSettings": {
          "path": "/neo"
        },
        "tlsSettings": {
          "serverName": "neo.example.com",
          "alpn": ["http/1.1"]
        }
      }
    }
  ],
  "outbounds": [
    {
      "protocol": "freedom",
      "tag": "direct"
    }
  ]
}
EOF

# 6. Перезапуск Xray
echo "[6/6] Перезапуск Xray..."
systemctl restart xray
systemctl enable xray

# Итог
echo ""
echo "======================================"
echo "  Установка завершена!"
echo "======================================"
echo ""
echo "UUID: $UUID"
echo "Порт: 443"
echo "Протокол: VLESS"
echo "Сеть: WebSocket"
echo "Путь: /neo"
echo ""
echo "Строка подключения:"
echo "vless://$UUID@ВАШ_IP:443?encryption=none&security=tls&type=ws&path=%2Fneo&sni=neo.example.com#NEO-VPN"
echo ""
echo "Замените ВАШ_IP на IP сервера"
echo "Замените neo.example.com на ваш домен (или IP)"
echo ""