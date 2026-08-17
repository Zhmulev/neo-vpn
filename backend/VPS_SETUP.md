# Инструкция по настройке VPS для NEO VPN

## 1. Купить VPS
- Vultr: https://www.vultr.com (от $2.5/мес)
- Hetzner: https://www.hetzner.com (от €3.5/мес)

## 2. Подключиться к серверу
ssh root@ВАШ_IP

## 3. Скачать скрипт
Загрузить install_xray.sh на сервер

## 4. Запустить
bash install_xray.sh

## 5. Получить строку подключения
Скрипт выдаст vless://... строку

## 6. Добавить в базу
UPDATE vpn_servers SET protocol='vless', v2ray_config='vless://...' WHERE id=1;

## 7. Подключиться с телефона
- Android: v2rayNG
- iOS: Shadowrocket