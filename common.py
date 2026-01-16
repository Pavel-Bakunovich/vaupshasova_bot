import constants
import deepseek
import random
import datetime, calendar
import database
from telebot.types import ReactionTypeEmoji
from logger import log, log_error
from helpers import fill_template, get_next_matchday_formatted, get_next_matchday,get_today_minsk_time, allow_registration,authorized,is_CEO,get_arguments
from PIL import Image, ImageDraw, ImageFont
  
def add_player_if_not_existant(first_name, last_name, username, telegram_id):
  player = database.find_player(telegram_id)
  if player is None:
      return database.create_player(first_name, last_name, username, telegram_id)
  else:
      return player

def add_player_if_not_existant_with_params(input_text, first_name, last_name, username, telegram_id):
    parts = input_text.split(' ', 1)
    if len(parts) > 1:
        input_player_name = parts[1].split()
        input_first_name = None
        input_last_name = None
        if len(input_player_name) == 1:
            input_last_name = input_player_name[0]
        else:
            if len(input_player_name) >= 2:
                input_first_name =input_player_name[0] 
                input_last_name = input_player_name[1]
        player = database.find_player_by_name(input_first_name, input_last_name)
    else:
        player = add_player_if_not_existant(first_name, last_name, username, telegram_id)
    
    return player

def get_player_name_extended(player):
    Telegram_First_Name = str(player[3])
    Telegram_Last_Name = str(player[4])
    Telegram_Login = str(player[5])
    Friendly_First_Name = str(player[7])
    Friendly_Last_Name = str(player[8])
    Informal_Friendly_First_Name = str(player[9])
    if (Friendly_First_Name is None):
        return f"{Telegram_First_Name} {Telegram_Last_Name} ({Telegram_Login})"
    else:
        return f"{Friendly_First_Name} {Friendly_Last_Name}"

def get_player_name(player):
    Telegram_First_Name = str(player[0])
    Telegram_Last_Name = str(player[1])
    Telegram_Login = str(player[2])
    Friendly_First_Name = str(player[4])
    Friendly_Last_Name = str(player[5])
    Informal_Friendly_First_Name = str(player[6])
    if (Friendly_First_Name is None):
        return f"{Telegram_First_Name} {Telegram_Last_Name} ({Telegram_Login})"
    else:
        return Informal_Friendly_First_Name

def get_player_name_formal(player):
    Telegram_First_Name = str(player[0])
    Telegram_Last_Name = str(player[1])
    Telegram_Login = str(player[2])
    Friendly_First_Name = str(player[4])
    Friendly_Last_Name = str(player[5])
    Informal_Friendly_First_Name = str(player[6])
    if (Friendly_First_Name is None):
        return f"{Telegram_First_Name} {Telegram_Last_Name} ({Telegram_Login})"
    else:
        return f"{Friendly_First_Name} {Friendly_Last_Name}"

def get_next_monday(hour=8, minute=0):
    now = get_today_minsk_time()
    days_ahead = (calendar.MONDAY - now.weekday()) % 7
    next_monday = now + datetime.timedelta(days=days_ahead)
    next_monday = next_monday.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if next_monday <= now:
        next_monday += datetime.timedelta(days=7)
    return next_monday

def reply_registration_not_allowed(bot, message, player):
    date_now = get_today_minsk_time()
    date_next_monday = get_next_monday()
    # Calculate time difference in days, hours and minutes
    delta = date_next_monday - date_now
    total_seconds = int(delta.total_seconds())
    days = total_seconds // 86400
    hours = (total_seconds % 86400) // 3600
    minutes = (total_seconds % 3600) // 60
    remaining = f"{days} дней, {hours} часов, {minutes} минут"

    bot.reply_to(message, f"{get_player_name(player)}, еще рано. Регистрация на следующую игру ({get_next_matchday_formatted()}) открывается в понедельник в 8:00 по минскому времени.\nДо открытия регистрации осталось {remaining}.")
    bot.set_message_reaction(message.chat.id,
                             message.message_id, [ReactionTypeEmoji('🤬')],
                             is_big=True)
    log(fill_template("Too early for registration message sent to {name}", name=get_player_name_formal(player)))

def reply_to_unauthorized(bot, message, player):
    bot.reply_to(message,"Вам нельзя пользоваться этим ботом. Он предназначается эксклюзивно для Лиги Ваупшасова.")
    bot.set_message_reaction(message.chat.id,
                             message.message_id, [ReactionTypeEmoji('🤬')],
                             is_big=True)
    log(fill_template("Unauthorized message sent: \'{name}\', (id: {id})", name=get_player_name_formal(player),id=message.from_user.id))

def reply_no_player_found(bot, message, player_name):
    bot.reply_to(message,fill_template("Не нашлось такого игрока: \'{name}\'", name=player_name))
    bot.set_message_reaction(message.chat.id,
                             message.message_id, [ReactionTypeEmoji('🤬')],
                             is_big=True)
    log(fill_template("No player found: \'{name}\'", name=player_name))

def reply_only_CEO_can_do_it(bot, message):
    bot.reply_to(message,"Это может делать только Директор.")
    bot.set_message_reaction(message.chat.id,
                             message.message_id, [ReactionTypeEmoji('🤬')],
                             is_big=True)
    log("Access restriction: Only CEO can do it")

def validate_access(chat_id, player, bot, message):
    access = False
    if player is not None:
        if (allow_registration()):
            if (authorized(chat_id)):    
                access = True
            else:
                reply_to_unauthorized(bot, message, player)
        else:
            reply_registration_not_allowed(bot, message, player)
    else:
        reply_no_player_found(bot, message, get_arguments(message.text))
    return access

def validate_access_no_game_registration_needed(chat_id, player, bot, message):
    access = False
    if player is not None:
        if (authorized(chat_id)):    
            access = True
        else:
            reply_to_unauthorized(bot, message, player)
    else:
        reply_no_player_found(bot, message, get_arguments(message.text))
    return access

def validate_CEO_zone(telegram_id, arguments):
    return ((is_CEO(telegram_id) is False) and (arguments is None)) or (is_CEO(telegram_id) is True)

def validate_CEO_zone_no_arguments(telegram_id):
    return is_CEO(telegram_id) is True


def text_to_image(text, font_size=15, image_size=(900, 600), 
                  bg_color=(255, 255, 255), text_color=(0, 0, 0)):
 
    # Create a blank image with the specified background color
    image = Image.new("RGB", image_size, bg_color)
    draw = ImageDraw.Draw(image)
    
    try:
        # Try to use arial font (common on Windows)
        font = ImageFont.truetype("PTMono.ttf", font_size)
    except:
        try:
            # Try to use arial font (common on Mac)
            font = ImageFont.truetype("Arial Unicode.ttf", font_size)
        except:
            try:
                # Try to use DejaVuSans (common on Linux)
                font = ImageFont.truetype("DejaVuSans.ttf", font_size)
            except:
                # Fall back to default font
                font = ImageFont.load_default()
                log("Warning: Using default font which may not support all characters")
    
    # Calculate text position (centered) - modern method
    # Get text bounding box
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # Calculate position to center text
    x = (image_size[0] - text_width) / 2
    y = (image_size[1] - text_height) / 2
    
    # Draw the text on the image
    draw.text((x, y), text, font=font, fill=text_color)

    return image

def fill_records_template(template, replace_to, replace_with):
    return template.replace("{"+replace_to+"}", str(replace_with))