from logger import log, log_error
from telebot.types import ReactionTypeEmoji
import helpers
from helpers import allow_registration,authorized
from common import add_player_if_not_existant, get_player_name, send_random_joke, send_abusive_comment, reply_registration_not_allowed, reply_to_unauthorized
import database
import constants

def execute(message, bot):
    user_message_text = ""

    try:
        player = add_player_if_not_existant(message.from_user.first_name,
                                            message.from_user.last_name,
                                            message.from_user.username,
                                            message.from_user.id)
        if (allow_registration()):
            if (authorized(message.chat.id)):
                matchday = database.find_registraion_player_matchday(helpers.get_next_matchday(), message.from_user.id)

                if matchday is None:
                    user_message_text = helpers.fill_template("{name}, тебя и так нету в составе на {date}!", name=get_player_name(player),date=helpers.get_next_matchday_formatted())
                else:
                    if matchday[2] == constants.TYPE_REMOVE:
                        user_message_text = helpers.fill_template("{name}, тебя и так нету в составе на {date}!", name=get_player_name(player),date=helpers.get_next_matchday_formatted())
                    else:
                        user_message_text = helpers.fill_template("❌ {name} удален из состава на игру {date}!", name=get_player_name(player),date=helpers.get_next_matchday_formatted())
                        database.update_registraion_player_matchday(helpers.get_next_matchday(), constants.TYPE_REMOVE, player[0])
                log(user_message_text)
                bot_message = bot.reply_to(message, user_message_text)
                bot.set_message_reaction(message.chat.id,
                                        message.message_id,
                                        [ReactionTypeEmoji('😭')],
                                        is_big=True)
                send_random_joke(bot, message)
                send_abusive_comment(bot, bot_message, user_message_text)
            else:
                reply_to_unauthorized(bot, message, player)
        else:
            reply_registration_not_allowed(bot, message, player)
    except Exception as e:
        bot.reply_to(message, constants.UNHANDLED_EXCEPTION_MESSAGE)
        log_error(e)