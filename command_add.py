from logger import log, log_error
from telebot.types import ReactionTypeEmoji
import helpers
from helpers import allow_registration,authorized
from common import add_player_if_not_existant, get_player_name, send_random_joke, send_abusive_comment, reply_registration_not_allowed, reply_to_unauthorized, add_player_if_not_existant_with_params
import database
import constants

def execute(message, bot):
    #pin message
    #tb = telebot.TeleBot(api_bot)
    #message = tb.send_message(group_id, 'Test!')
    #tb.pin_chat_message(group_id, message.message_id)
    user_message_text = ""
    #try:
    player = add_player_if_not_existant(message.from_user.first_name,
                                        message.from_user.last_name,
                                        message.from_user.username,
                                        message.from_user.id)
    
    #player_new = add_player_if_not_existant_with_params(message.text,
    #                                        message.from_user.first_name,
    #                                        message.from_user.last_name,
    #                                       message.from_user.username,
    #                                        message.from_user.id)

    #log(player_new)

    if (allow_registration()):
        if (authorized(message.chat.id)):
            matchday = database.find_registraion_player_matchday(helpers.get_next_matchday(), message.from_user.id)
            matchday_player_count = database.get_matchday_players_count(helpers.get_next_matchday())
            if matchday is None:
                if (matchday_player_count < 12):
                    database.register_player_matchday(helpers.get_next_matchday(), constants.TYPE_ADD, player[0])
                    user_message_text = helpers.fill_template("✍️ {name}, ты добавлен в состав на игру {date}.",
                        name=get_player_name(player),
                        date=helpers.get_next_matchday_formatted())
                    log(user_message_text)
                else:
                    user_message_text = helpers.fill_template("🪑 {name}, на игру {date} больше нет мест. Садим тебя в очередь на стульчик.", name=get_player_name(player),date=helpers.get_next_matchday_formatted())
                    log(user_message_text)
                    database.register_player_matchday(helpers.get_next_matchday(), constants.TYPE_CHAIR, player[0])
            else:
                if matchday[2] == constants.TYPE_ADD:
                    user_message_text = helpers.fill_template("{name}, ты ж уже записался!",name=get_player_name(player))
                else:
                    if (matchday_player_count < 12):
                        user_message_text = helpers.fill_template("✍️ {name}, окей, переносим тебя в основной состав на игру {date}.", name=get_player_name(player),date=helpers.get_next_matchday_formatted())
                        log(user_message_text)
                        database.update_registraion_player_matchday(helpers.get_next_matchday(), constants.TYPE_ADD, player[0])
                    else:
                        user_message_text = helpers.fill_template("🪑 {name}, на игру {date} больше нет мест! Садим тебя на стульчик.", name=get_player_name(player),date=helpers.get_next_matchday_formatted())
                        log(user_message_text)
                        database.update_registraion_player_matchday(helpers.get_next_matchday(), constants.TYPE_CHAIR, player[0])
    
            bot_message = bot.reply_to(message, user_message_text)
            bot.set_message_reaction(message.chat.id,
                                    message.message_id,
                                    [ReactionTypeEmoji('✍️')],
                                    is_big=True)
            
            matchday_player_count = 12 - database.get_matchday_players_count(helpers.get_next_matchday())
            if (matchday_player_count <= 3 and matchday_player_count > 0):
                bot.reply_to(message, helpers.fill_template("⚠️ Внимание, осталось мест: {free_spots_count}",free_spots_count=matchday_player_count))
            send_random_joke(bot, message)
            send_abusive_comment(bot, bot_message, user_message_text)
        else:
            reply_to_unauthorized(bot, message, player)
    else:
        reply_registration_not_allowed(bot, message, player)
    #except Exception as e:
    #    bot.reply_to(message, constants.UNHANDLED_EXCEPTION_MESSAGE)
    #    log_error(e)