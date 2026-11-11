import os
import requests
import llmf
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- CONFIGURATION ---
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
FOOTBALL_API_KEY = os.environ.get("FOOTBALL_API_KEY")

# --- FONCTION PRINCIPALE DU BOT ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texte = update.message.text
    
    # On vérifie que le message contient bien "vs" ou "-"
    if "vs" not in texte.lower() and "-" not in texte:
        await update.message.reply_text("Envoie-moi les équipes comme ceci : PSG vs OM")
        return

    await update.message.reply_text("⏳ Analyse du match en cours... (cela prend quelques secondes)")

    # 1. Préparation des données (on simplifie pour que ça marche de suite)
    data_match = f"Données pour le match {texte}."
    
    # 2. Demander à l'IA gratuite d'analyser et de rédiger
    prompt = f"""
    Tu es un expert en football et un community manager.
    Voici les données du match : {data_match}
    Le match demandé est : {texte}
    
    Fais une analyse courte pour dire qui est le favori (donne un pourcentage).
    Ensuite, rédige 3 textes de publication prêts à copier-coller :
    1. Pour Instagram (avec des emojis et des hashtags)
    2. Pour X/Twitter (moins de 280 caractères)
    3. Pour Facebook (un peu plus long)
    """
    
    try:
        # Appel à l'IA gratuite (llmf)
        analyse_ia = llmf.chat(prompt)
        
        # 3. Renvoyer le résultat sur Telegram
        await update.message.reply_text(analyse_ia)
        
    except Exception as e:
        await update.message.reply_text(f"Erreur de l'IA : {str(e)}")

# --- LANCEMENT DU BOT ---
def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Le bot est en ligne !")
    application.run_polling()

if __name__ == '__main__':
    main()
