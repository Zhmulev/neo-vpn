from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8604844501:AAHnsQQejVVZRPRQBRTea5cwV7mZ7Xq8O6s"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🚀 Бесплатный триал", callback_data="start_trial")],
        [InlineKeyboardButton("💎 Тарифы", callback_data="pricing")],
        [InlineKeyboardButton("🛠 Мои прокси", callback_data="my_proxies")],
        [InlineKeyboardButton("ℹ️ Помощь", callback_data="help")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🛡 *NEO VPN + Proxy Utility*\n\n"
        "Сеть нового поколения.\n"
        "Безопасный интернет и прокси в одном сервисе.\n\n"
        "Попробуй бесплатно 3 дня!\n\n"
        "Выбери действие:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "start_trial":
        await query.edit_message_text(
            "🎁 *Бесплатный триал NEO на 3 дня!*\n\n"
            "Ты получишь:\n"
            "✅ Доступ ко всем VPN-серверам\n"
            "✅ 1 прокси (SOCKS5/HTTP)\n"
            "✅ Безлимитный трафик\n\n"
            "📥 Скачай приложение: [скоро]\n"
            "🔑 Зарегистрируйся и напиши /register"
        )

    elif query.data == "pricing":
        await query.edit_message_text(
            "💎 *Тарифы NEO*\n\n"
            "🔹 *Базовый* — $3.99/мес\n"
            "• Все VPN-серверы\n"
            "• 1 статический прокси\n\n"
            "🔸 *Pro* — $7.99/мес\n"
            "• Все VPN-серверы\n"
            "• 5 прокси с ротацией\n"
            "• Доступ к API\n\n"
            "💳 Оплата: USDT, BTC\n"
            "Для оплаты напиши /buy"
        )

    elif query.data == "my_proxies":
        await query.edit_message_text(
            "🛠 *Мои прокси NEO*\n\n"
            "Напиши /myproxy чтобы увидеть твои активные прокси.\n"
            "Напиши /newproxy чтобы создать новый."
        )

    elif query.data == "help":
        await query.edit_message_text(
            "ℹ️ *Помощь NEO*\n\n"
            "/start — главное меню\n"
            "/register email password — регистрация\n"
            "/login email password — войти\n"
            "/servers — список серверов\n"
            "/newproxy — создать прокси\n"
            "/myproxy — мои прокси\n"
            "/buy — оплатить подписку"
        )

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("NEO Бот запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()