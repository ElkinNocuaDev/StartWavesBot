from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters, ConversationHandler

LANGUAGE, FLOW, SUPPORT = range(3)
user_language = {}

# Mensaje de bienvenida
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_keyboard = [['Español', 'English']]
    await update.message.reply_text(
        "👋 ¡Bienvenido a Start Waves Bot!\nPlease choose your language / Por favor elige tu idioma:",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, 
            one_time_keyboard=True,
            resize_keyboard=True
        )
    )
    return LANGUAGE

# Selección de idioma
async def select_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = update.message.text
    user_language[update.effective_user.id] = lang

    if lang == 'Español':
        await update.message.reply_text(
            "Has seleccionado Español. Por favor escribe 'soporte' si necesitas ayuda. 🚀",
            reply_markup=ReplyKeyboardMarkup.from_button(
                KeyboardButton("soporte"),
                resize_keyboard=True,
                one_time_keyboard=True
            )
        )
    else:
        await update.message.reply_text(
            "You selected English. Please type 'support' if you need help. 🚀",
            reply_markup=ReplyKeyboardMarkup.from_button(
                KeyboardButton("support"),
                resize_keyboard=True,
                one_time_keyboard=True
            )
        )

    return FLOW

# Manejo de flujo según idioma
async def flow_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.lower()
    lang = user_language.get(update.effective_user.id, 'English')
    
    if (lang == 'Español' and user_input == 'soporte') or (lang == 'English' and user_input == 'support'):
        if lang == 'Español':
            await update.message.reply_text("Un agente de soporte se pondrá en contacto contigo pronto. ⏳")
        else:
            await update.message.reply_text("A support agent will contact you soon. ⏳")
        return ConversationHandler.END
    else:
        if lang == 'Español':
            await update.message.reply_text("Por favor escribe 'soporte' para contactar con un agente.")
        else:
            await update.message.reply_text("Please type 'support' to contact an agent.")
        return FLOW

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