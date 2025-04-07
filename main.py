import os
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    ConversationHandler,
    filters,
)

# Estados de la conversación
SELECTING_LANGUAGE = 0

# Configurar logs
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_keyboard = [['Español', 'English']]
    
    await update.message.reply_text(
        '👋 ¡Bienvenido a Start Waves Bot!\nPlease choose your language / Por favor elige tu idioma:',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard,
            one_time_keyboard=True,
            resize_keyboard=True
        )
    )

    return SELECTING_LANGUAGE

# Handler de idioma
async def language_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_language = update.message.text

    if user_language == 'Español':
        await update.message.reply_text("Has seleccionado Español 🇪🇸")
    elif user_language == 'English':
        await update.message.reply_text("You have selected English 🇬🇧")
    else:
        await update.message.reply_text("Idioma no reconocido / Language not recognized.")

    return ConversationHandler.END

# Cancelar conversación
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Conversación cancelada. ¡Hasta luego!')
    return ConversationHandler.END

if __name__ == '__main__':
    # Cargar token desde variable de entorno
    TOKEN = os.environ["BOT_TOKEN"]

    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            SELECTING_LANGUAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, language_selected)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    app.add_handler(conv_handler)

    print("Bot corriendo... 🚀")
    app.run_polling()
