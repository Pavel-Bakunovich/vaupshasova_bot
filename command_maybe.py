from logger import log, log_error
from telebot.types import ReactionTypeEmoji
import helpers
from helpers import get_arguments
from common import add_player_if_not_existant_with_params, get_player_name, validate_access, validate_CEO_zone,reply_only_CEO_can_do_it
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
                    database.register_player_matchday(helpers.get_next_matchday(),constants.TYPE_MAYBE, player_id)

                    user_message_text = f"❓ {get_player_name(player)}, записался в список может-бытьчиков на игру {helpers.get_next_matchday_formatted()}"
                    log(user_message_text)
                else:
                    player_registration_type = matchday[1]
                    if player_registration_type == constants.TYPE_ADD:
                        user_message_text = f"❓ {get_player_name(player)}, окей, снимаем тебя с состава и записываем в список может-бытьчиков на игру {helpers.get_next_matchday_formatted()}!"
                        log(user_message_text)
                        database.update_registraion_player_matchday(helpers.get_next_matchday(), constants.TYPE_MAYBE, player_id)
                    if player_registration_type == constants.TYPE_MAYBE:
                        user_message_text = f"❓ {get_player_name(player)}, так ты и так уже в списке может-бытчиков!"
                        log(user_message_text)
                    if player_registration_type == constants.TYPE_CHAIR:
                        user_message_text = f"❓ {get_player_name(player)}, переводим тебя со стула в список может-бытьчиков на игру {helpers.get_next_matchday_formatted()}!"
                        log(user_message_text)
                        database.update_registraion_player_matchday(helpers.get_next_matchday(), constants.TYPE_MAYBE, player_id)
                    if player_registration_type == constants.TYPE_REMOVE:
                        user_message_text = f"❓ {get_player_name(player)}, ты раньше минусовался, но записываем тебя в список может-бытьчиков на игру {helpers.get_next_matchday_formatted()}!"
                        log(user_message_text)
                        database.update_registraion_player_matchday(helpers.get_next_matchday(), constants.TYPE_MAYBE, player_id)

                bot_message = bot.reply_to(message, user_message_text)
                bot.set_message_reaction(message.chat.id,
                                        message.message_id,
                                        [ReactionTypeEmoji('✍️')],
                                        is_big=True)
            else:
                reply_only_CEO_can_do_it(bot, message)
    except Exception as e:
        bot.reply_to(message, constants.UNHANDLED_EXCEPTION_MESSAGE)
        log_error(e)