import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler

BOT_TOKEN = os.getenv("BOT_TOKEN")

TEXTS = {
    'es': {
        'welcome': "¡Bienvenido a Start Waves! 🌊\nSelecciona tu idioma para comenzar:",
        'menu': "Selecciona una opción:",
        'support': "🛎️ Un agente de soporte se conectará contigo en breve.",
        'airdrop': ("🎉 ¡Start Waves lanza el AIRDROP de nuestro token SWC!\n"
                    "Como parte de nuestra misión de cerrar la brecha financiera en América Latina, ¡estamos regalando 50 tokens SWC GRATIS a quienes completen un formulario!\n\n"
                    "🚀 Cómo reclamar tus 50 SWC:\n"
                    "1. Ve al formulario de Airdrop en TypeForm.\n"
                    "2. Completa tus datos y envíalo.\n"
                    "3. ¡Recibe 50 SWC directamente en tu wallet!\n\n"
                    "Asegúrate de tener una wallet Ethereum lista, ya que los tokens SWC están basados en ERC20."),
        'token': ("💎 El token SWC es el corazón del ecosistema financiero de Start Waves. Diseñado bajo el estándar ERC20 en Ethereum, permite participar en nuestra plataforma DeFi, recibir recompensas, realizar pagos y acceder a servicios financieros innovadores para América Latina y más allá."),
        'back': "⬅️ Volver al menú"
    },
    'en': {
        'welcome': "Welcome to Start Waves! 🌊\nSelect your language to begin:",
        'menu': "Select an option:",
        'support': "🛎️ A support agent will connect with you shortly.",
        'airdrop': ("🎉 Start Waves is excited to announce the launch of our SWC token AIRDROP!\n"
                    "As part of our mission to bridge the financial gap in Latin America and beyond, we're offering 50 SWC tokens for FREE to anyone who completes a simple form.\n\n"
                    "🚀 How to Claim Your 50 SWC:\n"
                    "1. Go to the Airdrop Form on TypeForm.\n"
                    "2. Fill in your details and submit the form.\n"
                    "3. Receive 50 SWC tokens directly in your wallet!\n\n"
                    "Make sure you have an Ethereum wallet ready, as the SWC tokens are based on the ERC20 standard on the Ethereum blockchain."),
        'token': ("💎 The SWC token is the core of Start Waves' financial ecosystem. Built on the ERC20 Ethereum standard, it enables participation in our DeFi platform, access to rewards, payments, and innovative financial services across Latin America and beyond."),
        'back': "⬅️ Back to menu"
    }
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("Español 🇪🇸", callback_data='lang_es'),
            InlineKeyboardButton("English 🇺🇸", callback_data='lang_en')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(TEXTS['en']['welcome'], reply_markup=reply_markup)

async def language_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    lang = query.data.split('_')[1]
    keyboard = [
        [InlineKeyboardButton("🛎️ Soporte" if lang == 'es' else "🛎️ Support", callback_data=f'{lang}_support')],
        [InlineKeyboardButton("🎁 Airdrop", callback_data=f'{lang}_airdrop')],
        [InlineKeyboardButton("💎 SWC Token", callback_data=f'{lang}_token')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(TEXTS[lang]['menu'], reply_markup=reply_markup)

async def menu_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    lang, action = data.split('_', 1)

    message = TEXTS[lang].get(action, "Opción no válida / Invalid option")

    if action == 'airdrop':
        buttons = [
            [InlineKeyboardButton("🔗 Ir al formulario / Go to Form", url="https://bit.ly/3ARNopE")],
            [InlineKeyboardButton(TEXTS[lang]['back'], callback_data=f'lang_{lang}')]
        ]
    elif action == 'token':
        buttons = [
            [InlineKeyboardButton("🔎 Ver en Etherscan / View on Etherscan", url="https://etherscan.io/token/0x6c9D9D1e1f6ceC71d94abfAe45A62Bc6D30379ED")],
            [InlineKeyboardButton(TEXTS[lang]['back'], callback_data=f'lang_{lang}')]
        ]
    else:
        buttons = [
            [InlineKeyboardButton(TEXTS[lang]['back'], callback_data=f'lang_{lang}')]
        ]

    reply_markup = InlineKeyboardMarkup(buttons)
    await query.edit_message_text(message, reply_markup=reply_markup)

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(CallbackQueryHandler(language_selection, pattern=r'^lang_'))
    app.add_handler(CallbackQueryHandler(menu_selection, pattern=r'^(es|en)_(support|airdrop|token)$'))

    print("Bot is running...")
    app.run_polling()
