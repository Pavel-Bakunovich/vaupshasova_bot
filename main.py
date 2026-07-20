import os
import command_add
import command_remove
import command_chair
import command_maybe
import command_squad
import command_split
import command_talk
import command_wakeup
import command_register_lineups
import command_print_lineups
import command_season_stats
import command_alltime_stats
import command_balance
import command_how_much_we_owe
import command_my_balance
import command_my_stats
import command_register_game_stats
import command_register_money
import command_register_pitch_payment
import command_register_score
import command_score
import command_records
import alerts
import dotenv
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram import Update
from logger import log
from logger import log_error

dotenv.load_dotenv()
API_KEY = os.environ['TELEGRAM_API_TOKEN']
log("Environment variables loaded.")

# Create a wrapper class to maintain compatibility with command modules
class BotWrapper:
    def __init__(self, app):
        self.app = app
        self.bot = app.bot
    
    async def send_message(self, chat_id, text, **kwargs):
        return await self.bot.send_message(chat_id=chat_id, text=text, **kwargs)
    
    async def reply_to(self, message, text, **kwargs):
        return await message.reply_text(text, **kwargs)
    
    async def delete_message(self, chat_id, message_id):
        return await self.bot.delete_message(chat_id=chat_id, message_id=message_id)
    
    async def edit_message_text(self, text, chat_id, message_id, **kwargs):
        return await self.bot.edit_message_text(text=text, chat_id=chat_id, message_id=message_id, **kwargs)
    
    async def pin_chat_message(self, chat_id, message_id):
        return await self.bot.pin_chat_message(chat_id=chat_id, message_id=message_id)
    
    async def set_message_reaction(self, chat_id, message_id, reactions, **kwargs):
        return await self.bot.set_message_reaction(chat_id=chat_id, message_id=message_id, reaction=reactions, **kwargs)
    
    async def send_photo(self, chat_id, photo, **kwargs):
        # Handle PIL Image objects by converting to BytesIO
        from io import BytesIO
        try:
            from PIL.Image import Image as PILImage
        except ImportError:
            PILImage = None
        
        if PILImage and isinstance(photo, PILImage):
            # Convert PIL Image to BytesIO
            photo_bytes = BytesIO()
            photo.save(photo_bytes, format='PNG')
            photo_bytes.seek(0)
            photo = photo_bytes
        
        return await self.bot.send_photo(chat_id=chat_id, photo=photo, **kwargs)

async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await command_add.execute(update.message, bot_wrapper)
    except Exception as e:
        log_error(e)

async def remove(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await command_remove.execute(update.message, bot_wrapper)
    except Exception as e:
        log_error(e)

async def chair(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await command_chair.execute(update.message, bot_wrapper)
    except Exception as e:
        log_error(e)

async def maybe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await command_maybe.execute(update.message, bot_wrapper)
    except Exception as e:
        log_error(e)

async def squad(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await command_squad.execute(update.message, bot_wrapper)
    except Exception as e:
        log_error(e)

async def split(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await command_split.execute(update.message, bot_wrapper)
    except Exception as e:
        log_error(e)

async def talk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await command_talk.execute(update.message, bot_wrapper)
    except Exception as e:
        log_error(e)

async def wakeup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await command_wakeup.execute(update.message, bot_wrapper)
    except Exception as e:
        log_error(e)

async def register_lineups(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await command_register_lineups.execute(update.message, bot_wrapper)
    except Exception as e:
        log_error(e)

async def print_lineups(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await command_print_lineups.execute(update.message, bot_wrapper)
    except Exception as e:
        log_error(e)

async def season_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await command_season_stats.execute(update.message, bot_wrapper)
    except Exception as e:
        log_error(e)

async def alltime_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await command_alltime_stats.execute(update.message, bot_wrapper)
    except Exception as e:
        log_error(e)

async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await command_balance.execute(update.message, bot_wrapper)
    except Exception as e:
        log_error(e)

async def how_much_we_owe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await command_how_much_we_owe.execute(update.message, bot_wrapper)
    except Exception as e:
        log_error(e)

async def my_balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await command_my_balance.execute(update.message, bot_wrapper)
    except Exception as e:
        log_error(e)

async def my_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await command_my_stats.execute(update.message, bot_wrapper)
    except Exception as e:
        log_error(e)

async def register_game_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await command_register_game_stats.execute(update.message, bot_wrapper)
    except Exception as e:
        log_error(e)

async def register_money(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await command_register_money.execute(update.message, bot_wrapper)
    except Exception as e:
        log_error(e)

async def register_pitch_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await command_register_pitch_payment.execute(update.message, bot_wrapper)
    except Exception as e:
        log_error(e)

async def register_score(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await command_register_score.execute(update.message, bot_wrapper)
    except Exception as e:
        log_error(e)

async def score(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await command_score.execute(update.message, bot_wrapper)
    except Exception as e:
        log_error(e)

async def records(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await command_records.execute(update.message, bot_wrapper)
    except Exception as e:
        log_error(e)

def main():
    global bot_wrapper
    
    app = Application.builder().token(API_KEY).build()
    bot_wrapper = BotWrapper(app)
    log("Bot object initialized.")
    
    # Add command handlers
    app.add_handler(CommandHandler("add", add))
    app.add_handler(CommandHandler("remove", remove))
    app.add_handler(CommandHandler("chair", chair))
    app.add_handler(CommandHandler("maybe", maybe))
    app.add_handler(CommandHandler("squad", squad))
    app.add_handler(CommandHandler("split", split))
    app.add_handler(CommandHandler("talk", talk))
    app.add_handler(CommandHandler("wakeup", wakeup))
    app.add_handler(CommandHandler("register_lineups", register_lineups))
    app.add_handler(CommandHandler("print_lineups", print_lineups))
    app.add_handler(CommandHandler("season_stats", season_stats))
    app.add_handler(CommandHandler("alltime_stats", alltime_stats))
    app.add_handler(CommandHandler("balance", balance))
    app.add_handler(CommandHandler("how_much_we_owe", how_much_we_owe))
    app.add_handler(CommandHandler("my_balance", my_balance))
    app.add_handler(CommandHandler("my_stats", my_stats))
    app.add_handler(CommandHandler("register_game_stats", register_game_stats))
    app.add_handler(CommandHandler("register_money", register_money))
    app.add_handler(CommandHandler("register_pitch_payment", register_pitch_payment))
    app.add_handler(CommandHandler("register_score", register_score))
    app.add_handler(CommandHandler("score", score))
    app.add_handler(CommandHandler("records", records))
    
    # Schedule alerts (synchronous setup)
    alerts.schedule_alerts(app)
    log("Alerts scheduled.")
    log("Started polling.")
    log("Bot is up and running.")

    # Run the bot with blocking polling
    app.run_polling()

if __name__ == '__main__':
    main()
