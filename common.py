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
    if (player[11] is None):
        return str(player[7]) + " " + str(player[8]) + " (" + str(
            player[9]) + ")"
    else:
        return str(player[11]) + " " + str(player[12])

def get_player_name(player):
    if (player[5] is None):
        return str(player[1]) + " " + str(player[2]) + " (" + str(
            player[3]) + ")"
    else:
        return str(player[7])

def get_player_name_formal(player):
    if (player[5] is None):
        return str(player[1]) + " " + str(player[2]) + " (" + str(
            player[3]) + ")"
    else:
        return str(player[5]) + " " + str(player[6])
    
def send_random_joke(bot, message):
    if (random.random() < 0.20):
        response = deepseek.send_request(constants.RANDOM_MAKSIM_JOKE_PROMPT_DEEPSEEK, 1.5)
        bot.send_message(message.chat.id, response)
        log("Random joke sent")

def send_abusive_comment(bot, message, bot_message):
    if (random.random() < 0.20):
        abusive_message = deepseek.send_request(fill_template(constants.ABUSIVE_COMMENT_DEEPSEEK, bot_message = bot_message), 1.5)
        bot.reply_to(message, abusive_message)
        log(fill_template("Abusive comment sent in response to: \'{bot_message}\'", bot_message=bot_message))

def reply_registration_not_allowed(bot, message, player):
    bot.reply_to(
        message,
        fill_template("{player_name}, eще рано. Регистрация на {date} открывается в понедельник.",
            date=get_next_matchday_formatted(),
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
    if (allow_registration()):
        if (authorized(chat_id)):
            if player is not None:
                access = True
            else:
                reply_no_player_found(bot, message, get_arguments(message.text))
        else:
            reply_to_unauthorized(bot, message, player)
    else:
        reply_registration_not_allowed(bot, message, player)

    return access

def validate_CEO_zone(telegram_id, arguments):
    return ((is_CEO(telegram_id) is False) and (arguments is None)) or (is_CEO(telegram_id) is True)