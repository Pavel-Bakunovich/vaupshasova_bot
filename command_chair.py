from logger import log, log_error
from telebot.types import ReactionTypeEmoji
import helpers
from helpers import get_arguments
from common import add_player_if_not_existant_with_params, get_player_name, send_abusive_comment, validate_access, validate_CEO_zone,reply_only_CEO_can_do_it
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
            player_telegram_id = player[4]
            player_id = player[0]
            if validate_CEO_zone(message.from_user.id,get_arguments(message.text)):
                matchday = database.find_registraion_player_matchday(helpers.get_next_matchday(), player_telegram_id)

                if matchday is None:
                    database.register_player_matchday(helpers.get_next_matchday(),constants.TYPE_CHAIR, player_id)

                    user_message_text = helpers.fill_template("🪑 {name}, cел на стульчик на игру {date}" ,name=get_player_name(player),date=helpers.get_next_matchday_formatted())
                    log(user_message_text)
                else:
                    if matchday[2] == constants.TYPE_ADD:
                        user_message_text = helpers.fill_template("🪑 {name}, окей, снимаем тебя с состава и записываем на стул на игру {date}!" ,name=get_player_name(player),date=helpers.get_next_matchday_formatted())
                        log(user_message_text)
                        database.update_registraion_player_matchday(helpers.get_next_matchday(), constants.TYPE_CHAIR, player_id)
                    if matchday[2] == constants.TYPE_CHAIR:
                        user_message_text = helpers.fill_template("🪑 {name}, так ты и так уже на стуле сидишь!" ,name=get_player_name(player))
                        log(user_message_text)
                    if matchday[2] == constants.TYPE_REMOVE:
                        user_message_text = helpers.fill_template("🪑 {name}, ты раньше минусовался, но записываем тебя на стул на игру {date}! Так уж и быть." ,name=get_player_name(player),date=helpers.get_next_matchday_formatted())
                        log(user_message_text)
                        database.update_registraion_player_matchday(helpers.get_next_matchday(), constants.TYPE_CHAIR, player_id)

                bot_message = bot.reply_to(message, user_message_text)
                bot.set_message_reaction(message.chat.id,
                                        message.message_id,
                                        [ReactionTypeEmoji('✍️')],
                                        is_big=True)
                send_abusive_comment(bot, bot_message, user_message_text)
            else:
                reply_only_CEO_can_do_it(bot, message, player)
    except Exception as e:
        bot.reply_to(message, constants.UNHANDLED_EXCEPTION_MESSAGE)
        log_error(e)