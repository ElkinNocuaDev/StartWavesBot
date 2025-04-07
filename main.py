from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters, ConversationHandler

LANGUAGE, FLOW = range(2)
user_language = {}

# Mensaje de bienvenida
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_keyboard = [['Español', 'English']]

    await update.message.reply_text(
        '👋 ¡Bienvenido a Start Waves Bot!\nPlease choose your language / Por favor elige tu idioma:',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard,
            one_time_keyboard=True,
            resize_keyboard=True  # ✅ importante
        )
    )

    return SELECTING_LANGUAGE

# Selección de idioma
async def select_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = update.message.text
    user_language[update.effective_user.id] = lang

    if lang == 'Español':
        await update.message.reply_text("Has seleccionado Español. ¿Qué deseas hacer ahora? 🚀")
    else:
        await update.message.reply_text("You selected English. What would you like to do next? 🚀")

    return FLOW

# Manejo de flujo según idioma
async def flow_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = user_language.get(update.effective_user.id, 'English')
    if lang == 'Español':
        await update.message.reply_text("Este es el flujo en español 🎯")
    else:
        await update.message.reply_text("This is the English flow 🎯")
    return ConversationHandler.END

# App y handlers
def main():
    import os
    token = os.getenv("BOT_TOKEN")

    app = ApplicationBuilder().token(token).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            LANGUAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, select_language)],
            FLOW: [MessageHandler(filters.TEXT & ~filters.COMMAND, flow_handler)],
        },
        fallbacks=[],
    )

    app.add_handler(conv_handler)
    app.run_polling()

if __name__ == '__main__':
    main()
