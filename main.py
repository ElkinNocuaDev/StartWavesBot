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
        'airdrop': "🎁 ¡Participa en el Airdrop de SWC!\n\nStart Waves se complace en anunciar el lanzamiento de nuestro AIRDROP del token SWC. Como parte de nuestra misión de cerrar la brecha financiera en América Latina y más allá, ¡estamos ofreciendo 50 tokens SWC GRATIS a quienes completen un simple formulario!\n\n💡 Cómo reclamar tus 50 SWC:\n1. Haz clic en el botón para ir al formulario TypeForm.\n2. Completa tus datos y envía el formulario.\n3. ¡Recibe 50 tokens SWC directamente en tu wallet!\n\nAsegúrate de tener una wallet Ethereum preparada, ya que los tokens SWC están basados en el estándar ERC20.",
        'token': "💎 Aprende más sobre el token SWC.",
        'back': "Volver al menú"
    },
    'en': {
        'selected': "You have selected English 🇬🇧\n👇 Choose an option:",
        'support': "🔧 A support agent will be with you shortly.",
        'airdrop': "🎁 Join the SWC Airdrop!\n\nStart Waves is excited to announce the launch of our SWC token AIRDROP! As part of our mission to bridge the financial gap in Latin America and beyond, we're offering 50 SWC tokens for FREE to anyone who completes a simple form. Join the future of decentralized finance today!\n\n💡 How to Claim Your 50 SWC:\n1. Go to the Airdrop Form on TypeForm.\n2. Fill in your details and submit the form.\n3. Receive 50 SWC tokens directly in your wallet!\n\nMake sure you have an Ethereum wallet ready, as the SWC tokens are based on the ERC20 standard on the Ethereum blockchain.",
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

    message = TEXTS[lang].get(action, "Opción no válida / Invalid option")

    # Si es Airdrop, agregar botón con link
    if action == 'airdrop':
        buttons = [
            [InlineKeyboardButton("🔗 Ir al formulario / Go to Form", url="https://bit.ly/3ARNopE")],
            [InlineKeyboardButton(TEXTS[lang]['back'], callback_data=f'lang_{lang}')]
        ]
    else:
        buttons = [
            [InlineKeyboardButton(TEXTS[lang]['back'], callback_data=f'lang_{lang}')]
        ]

    reply_markup = InlineKeyboardMarkup(buttons)
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
