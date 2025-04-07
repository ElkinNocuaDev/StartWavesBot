import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler,
)

# Configurar logs
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🇪🇸 Español", callback_data='lang_es')],
        [InlineKeyboardButton("🇬🇧 English", callback_data='lang_en')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        '👋 ¡Bienvenido a Start Waves Bot!\nPlease choose your language / Por favor elige tu idioma:',
        reply_markup=reply_markup
    )

# Callback del botón
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    lang = query.data
    if lang == 'lang_es':
        await query.edit_message_text("Has seleccionado Español 🇪🇸")
    elif lang == 'lang_en':
        await query.edit_message_text("You have selected English 🇬🇧")
    else:
        await query.edit_message_text("Idioma no reconocido / Language not recognized.")

# /cancel opcional
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Conversación cancelada. ¡Hasta luego!')

# Iniciar bot
if __name__ == '__main__':
    TOKEN = os.environ["BOT_TOKEN"]
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(CommandHandler('cancel', cancel))

    print("Bot corriendo... 🚀")
    app.run_polling()
