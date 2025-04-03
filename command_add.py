from logger import log, log_error
from telebot.types import ReactionTypeEmoji
import helpers
from helpers import get_arguments
from common import get_player_name, send_random_joke, send_abusive_comment, add_player_if_not_existant_with_params, validate_access, reply_only_CEO_can_do_it, validate_CEO_zone
import database
import constants

def execute(message, bot):
    #pin message
    #tb = telebot.TeleBot(api_bot)
    #message = tb.send_message(group_id, 'Test!')
    #tb.pin_chat_message(group_id, message.message_id)
    user_message_text = ""
    try:
        player = add_player_if_not_existant_with_params(message.text,
                                                        message.from_user.first_name,
                                                        message.from_user.last_name,
                                                        message.from_user.username,
                                                        message.from_user.id)

        if validate_access(message.chat.id, player, bot, message):
            player_telegram_id = player[4]
            player_id = player[0]
            if validate_CEO_zone(message.from_user.id,get_arguments(message.text)):
                matchday = database.find_registraion_player_matchday(helpers.get_next_matchday(), player_telegram_id)
                matchday_player_count = database.get_matchday_players_count(helpers.get_next_matchday())
                if matchday is None:
                    if (matchday_player_count < 12):
                        database.register_player_matchday(helpers.get_next_matchday(), constants.TYPE_ADD, player_id)
                        user_message_text = helpers.fill_template("✍️ {name}, ты добавлен в состав на игру {date}.",
                            name=get_player_name(player),
                            date=helpers.get_next_matchday_formatted())
                        log(user_message_text)
                    else:
                        user_message_text = helpers.fill_template("🪑 {name}, на игру {date} больше нет мест. Садим тебя в очередь на стульчик.", name=get_player_name(player),date=helpers.get_next_matchday_formatted())
                        log(user_message_text)
                        database.register_player_matchday(helpers.get_next_matchday(), constants.TYPE_CHAIR, player_id)
                else:
                    if matchday[2] == constants.TYPE_ADD:
                        user_message_text = helpers.fill_template("{name}, ты ж уже записался!",name=get_player_name(player))
                        log(user_message_text)
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
                reply_only_CEO_can_do_it(bot, message, player)

    except Exception as e:
        bot.reply_to(message, constants.UNHANDLED_EXCEPTION_MESSAGE)
        log_error(e)