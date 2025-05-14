import constants
import deepseek
import random
import database
from telebot.types import ReactionTypeEmoji
from logger import log, log_error
from helpers import fill_template,get_next_matchday_formatted,allow_registration,authorized,is_CEO,get_arguments
  
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

def send_abusive_comment(bot, message, bot_message):
    if (random.random() < 0.20):
        with open(constants.ABUSIVE_COMMENT_PROMPT_FILENAME,"r") as abusive_comment_prompt_file:
            abusive_comment_prompt = abusive_comment_prompt_file.read()

        abusive_message = deepseek.send_request(fill_template(abusive_comment_prompt, bot_message = bot_message), 1.5)
        bot.reply_to(message, abusive_message)
        log(fill_template("Abusive comment sent in response to: \'{bot_message}\'", bot_message=bot_message))

def reply_registration_not_allowed(bot, message, player):
    bot.reply_to(
        message,
        fill_template("{player_name}, eще рано. Регистрация на следующую игру открывается в понедельник.",
            player_name=get_player_name(player)))
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

def reply_only_CEO_can_do_it(bot, message, player_name):
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

def validate_CEO_zone(telegram_id, arguments):
    return ((is_CEO(telegram_id) is False) and (arguments is None)) or (is_CEO(telegram_id) is True)