from logger import log, log_error
from telebot.types import ReactionTypeEmoji
import helpers
from helpers import get_arguments
from common import add_player_if_not_existant_with_params, get_player_name,reply_only_CEO_can_do_it,validate_access,validate_CEO_zone
import database
import constants

def execute(message, bot):
    user_message_text = ""

    try:
        player = add_player_if_not_existant_with_params(message.text,
                                                        message.from_user.first_name,
                                                        message.from_user.last_name,
                                                        message.from_user.username,
                                                        message.from_user.id)
        if validate_access(message.chat.id, player, bot, message):
            player_telegram_id = player[3]
            player_id = player[7]
            if validate_CEO_zone(message.from_user.id,get_arguments(message.text)):
                matchday = database.find_registraion_player_matchday(helpers.get_next_matchday(), player_telegram_id)

                if matchday is None:
                    user_message_text = helpers.fill_template("❌ {name}, тебя и так нету в составе на {date}! Но я тебя все равно помечу ❌, чтобы все знали, что ты не будешь играть.", name=get_player_name(player),date=helpers.get_next_matchday_formatted())
                    database.update_registraion_player_matchday(helpers.get_next_matchday(), constants.TYPE_REMOVE, player_id)
                else:
                    player_registration_type = matchday[1]
                    if player_registration_type == constants.TYPE_REMOVE:
                        user_message_text = helpers.fill_template("{name}, тебя и так нету в составе на {date}!", name=get_player_name(player),date=helpers.get_next_matchday_formatted())
                    else:
                        user_message_text = helpers.fill_template("❌ {name} удален из состава на игру {date}!", name=get_player_name(player),date=helpers.get_next_matchday_formatted())
                        database.update_registraion_player_matchday(helpers.get_next_matchday(), constants.TYPE_REMOVE, player_id)
                log(user_message_text)
                bot_message = bot.reply_to(message, user_message_text)
                bot.set_message_reaction(message.chat.id,
                                        message.message_id,
                                        [ReactionTypeEmoji('😭')],
                                        is_big=True)
            else:
                reply_only_CEO_can_do_it(bot, message)

    except Exception as e:
        bot.reply_to(message, constants.UNHANDLED_EXCEPTION_MESSAGE)
        log_error(e)