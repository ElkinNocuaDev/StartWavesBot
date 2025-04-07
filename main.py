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

# Diccionario de textos
TEXTS = {
    'es': {
        'selected': "Has seleccionado Español 🇪🇸\n👇 Elige una opción:",
        'support': "🔧 Un agente de soporte se conectará en breve.",
        'airdrop': "🎁 ¡Participa en el Airdrop de SWC!",
        'token': "💎 Aprende más sobre el token SWC.",
        'back': "Volver al menú"
    },
    'en': {
        'selected': "You have selected English 🇬🇧\n👇 Choose an option:",
        'support': "🔧 A support agent will be with you shortly.",
        'airdrop': "🎁 Join the SWC Airdrop!",
        'token': "💎 Learn more about the SWC token.",
        'back': "Back to menu"
    }
}

# Comando /start
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

# Botón de selección de idioma
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    lang = query.data.split('_')[1]
    context.user_data['lang'] = lang  # guardar idioma en sesión del usuario

    await query.edit_message_text(TEXTS[lang]['selected'])

    options = [
        [InlineKeyboardButton("Soporte" if lang == 'es' else "Support", callback_data=f'{lang}_support')],
        [InlineKeyboardButton("Airdrop", callback_data=f'{lang}_airdrop')],
        [InlineKeyboardButton("SWC Token", callback_data=f'{lang}_token')]
    ]
    reply_markup = InlineKeyboardMarkup(options)
    await query.message.reply_text("👇", reply_markup=reply_markup)

# Manejo del menú
async def menu_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    lang, action = data.split('_', 1)

    # Mensaje correspondiente
    message = TEXTS[lang].get(action, "Opción no válida / Invalid option")

    # Botón volver al menú
    back_button = [[InlineKeyboardButton(TEXTS[lang]['back'], callback_data=f'lang_{lang}')]]
    reply_markup = InlineKeyboardMarkup(back_button)

    await query.edit_message_text(message, reply_markup=reply_markup)

# /cancel
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Conversación cancelada. ¡Hasta luego!')

# Iniciar bot
if __name__ == '__main__':
    TOKEN = os.environ["BOT_TOKEN"]
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(CallbackQueryHandler(button, pattern='^lang_'))
    app.add_handler(CallbackQueryHandler(menu_selection, pattern='^(es|en)_(support|airdrop|token)'))
    app.add_handler(CommandHandler('cancel', cancel))

    print("Bot corriendo... 🚀")
    app.run_polling()
