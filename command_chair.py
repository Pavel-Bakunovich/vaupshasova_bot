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
                    database.register_player_matchday(helpers.get_next_matchday(),
                                                    "chair", player[0])

                    user_message_text = helpers.fill_template("🪑 {name}, cел на стульчик на игру {date}" ,name=get_player_name(player),date=helpers.get_next_matchday_formatted())
                    log(user_message_text)
                else:
                    if matchday[2] == "add":
                        user_message_text = helpers.fill_template("🪑 {name}, окей, снимаем тебя с состава и записываем на стул на игру {date}!" ,name=get_player_name(player),date=helpers.get_next_matchday_formatted())
                        log(user_message_text)
                        database.update_registraion_player_matchday(helpers.get_next_matchday(), "chair", player[0])
                    if matchday[2] == "chair":
                        user_message_text = helpers.fill_template("🪑 {name}, так ты и так уже на стуле сидишь!" ,name=get_player_name(player))
                        log(user_message_text)
                    if matchday[2] == "remove":
                        user_message_text = helpers.fill_template("🪑 {name}, ты раньше минусовался, но записываем тебя на стул на игру {date}! Так уж и быть." ,name=get_player_name(player),date=helpers.get_next_matchday_formatted())
                        log(user_message_text)
                        database.update_registraion_player_matchday(helpers.get_next_matchday(), "chair", player[0])

                bot_message = bot.reply_to(message, user_message_text)
                bot.set_message_reaction(message.chat.id,
                                        message.message_id,
                                        [ReactionTypeEmoji('✍️')],
                                        is_big=True)
                send_random_joke(bot, message, player)
                send_abusive_comment(bot, bot_message, user_message_text)
            else:
                reply_to_unauthorized(bot, message, player)
        else:
            reply_registration_not_allowed(bot, message, player)
    except Exception as e:
        bot.reply_to(message, constants.UNHANDLED_EXCEPTION_MESSAGE)
        log_error(e)