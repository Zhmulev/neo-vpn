import sys
import os
import uuid

# Lj,fdkztv rjhtym backend d genm lkz rjhhtrnys[ bvgjhnjd
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from telegram import Update
from telegram.ext import Application, ApplicationBuilder, CommandHandler, ContextTypes
from app.core.config import settings
from app.db.database import SessionLocal
from app.models.user import User
from app.models.server import VPNServer
from app.services.vpn_service import VPNService
from app.core.security import verify_password

TOKEN = settings.TELEGRAM_BOT_TOKEN

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_user_by_telegram_id(db, telegram_id):
    return db.query(User).filter(User.telegram_id == telegram_id).first()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🛡 *NEO VPN Bot*\n\n"
        "Привет! Я твой помощник по управлению VPN и прокси.\n\n"
        "🔹 /bind <email> <password> — привязать аккаунт\n"
        "🔹 /balance — проверить баланс\n"
        "🔹 /servers — список серверов\n"
        "🔹 /vpn <id> — получить VPN конфиг\n"
        "🔹 /proxy — управление прокси",
        parse_mode="Markdown"
    )

async def bind(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text("❌ Использование: /bind <email> <password>")
        return

    email, password = context.args[0], context.args[1]
    telegram_id = update.effective_chat.id

    db = next(get_db())
    try:
        user = db.query(User).filter(User.email == email).first()
        if not user or not verify_password(password, user.hashed_password):
            await update.message.reply_text("❌ Неверный email или пароль.")
            return

        if user.telegram_id and user.telegram_id != telegram_id:
            await update.message.reply_text("⚠️ Этот аккаунт уже привязан к другому Telegram.")
            return

        user.telegram_id = telegram_id
        db.commit()
        await update.message.reply_text(f"✅ Аккаунт успешно привязан!\nДобро пожаловать, {user.username}!")
    finally:
        db.close()

async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = next(get_db())
    try:
        user = get_user_by_telegram_id(db, update.effective_chat.id)
        if not user:
            await update.message.reply_text("❌ Сначала привяжи аккаунт через /bind")
            return
        await update.message.reply_text(f"💰 Твой баланс: *{user.balance}₽*", parse_mode="Markdown")
    finally:
        db.close()

async def servers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = next(get_db())
    try:
        user = get_user_by_telegram_id(db, update.effective_chat.id)
        if not user:
            await update.message.reply_text("❌ Сначала привяжи аккаунт через /bind")
            return

        srvs = db.query(VPNServer).filter(VPNServer.is_active == True).all()
        if not srvs:
            await update.message.reply_text("🌍 Нет доступных серверов.")
            return

        msg = "🌍 *Доступные серверы:*\n\n"
        for s in srvs:
            msg += f"🆔 `{s.id}` — *{s.name}* ({s.country}, {s.city})\n"
        msg += "\nИспользуй `/vpn <id>` для получения конфига."
        await update.message.reply_text(msg, parse_mode="Markdown")
    finally:
        db.close()

async def vpn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Использование: /vpn <server_id>")
        return

    db = next(get_db())
    try:
        user = get_user_by_telegram_id(db, update.effective_chat.id)
        if not user:
            await update.message.reply_text("❌ Сначала привяжи аккаунт через /bind")
            return

        server_id = int(context.args[0])
        server = db.query(VPNServer).filter(VPNServer.id == server_id).first()
        if not server:
            await update.message.reply_text("❌ Сервер не найден.")
            return

        await update.message.reply_text("⏳ Генерирую конфиг...")

        user_email = f"tg-{user.telegram_id}-{uuid.uuid4().hex[:6]}"
        config = await VPNService.create_vless_user(
            server_ip=server.endpoint,
            port=server.port,
            server_name=server.name,
            user_email=user_email
        )

        await update.message.reply_text(f"✅ *{server.name}*\n\n`{config}`", parse_mode="Markdown")
    except ValueError:
        await update.message.reply_text("❌ ID сервера должен быть числом.")
    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка: {str(e)}")
    finally:
        db.close()

async def proxy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = next(get_db())
    try:
        user = get_user_by_telegram_id(db, update.effective_chat.id)
        if not user:
            await update.message.reply_text("❌ Сначала привяжи аккаунт через /bind")
            return

        await update.message.reply_text("🔀 Функция создания прокси через бота находится в разработке. Используй веб-панель!")
    finally:
        db.close()

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("bind", bind))
    app.add_handler(CommandHandler("balance", balance))
    app.add_handler(CommandHandler("servers", servers))
    app.add_handler(CommandHandler("vpn", vpn))
    app.add_handler(CommandHandler("proxy", proxy))

    print("🚀 NEO Telegram Bot запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()
