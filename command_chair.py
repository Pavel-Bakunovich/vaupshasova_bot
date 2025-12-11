from logger import log, log_error
from telebot.types import ReactionTypeEmoji
import helpers
from helpers import get_arguments, get_next_matchday
from common import get_next_matchday_formatted, add_player_if_not_existant_with_params, get_player_name, validate_access, validate_CEO_zone,reply_only_CEO_can_do_it
import database
import constants
import command_remove

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
                matchday_remaining_free_slots = 12 - database.get_matchday_players_count(helpers.get_next_matchday())
                matchday_chair_count = database.get_matchday_chair_count(helpers.get_next_matchday())
                if matchday is None:
                    user_message_text = put_player_to_chair(False, player, player_id, matchday_remaining_free_slots, matchday_chair_count)
                else:
                    player_registration_type = matchday[1]
                    if player_registration_type == constants.TYPE_ADD:
                        user_message_text = f"🪑 {get_player_name(player)}, окей, снимаем тебя с состава на игру {get_next_matchday_formatted()} и записываем в может-бытьчики, а не на стул. Стул для тех, кто готов играть, но нет мест."
                        log(user_message_text)
                        database.update_registraion_player_matchday(helpers.get_next_matchday(), constants.TYPE_MAYBE, player_id)
                        command_remove.player_signed_off_from_squad(player_registration_type, bot, message)
                    if player_registration_type == constants.TYPE_CHAIR:
                        user_message_text = f"🪑 {get_player_name(player)}, так ты и так уже на стуле сидишь!"
                        log(user_message_text)
                    if player_registration_type == constants.TYPE_REMOVE or player_registration_type == constants.TYPE_MAYBE:
                        user_message_text = put_player_to_chair(True, player, player_id, matchday_remaining_free_slots, matchday_chair_count)

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



def put_player_to_chair(is_update, player, player_id, matchday_remaining_free_slots, matchday_chair_count):
    if matchday_remaining_free_slots > 0:
        # What if 1 slot remains with 2 chairs and user wants to /chair. With this logic he will be added to maybe list.
        # In such case, need to add him to the chair.
        user_message_text = ""
        if matchday_chair_count < matchday_remaining_free_slots:
            register_player_internal(is_update, player_id, constants.TYPE_MAYBE)
            user_message_text = f"🪑 {get_player_name(player)}, на следующую игру {get_next_matchday_formatted()} еще есть места. А /chair для тех, кто готов играть, а места нет. Переводим тебя в может-бытьчики. Ну или нажимай /add, если готов записаться в состав."
            log(user_message_text)
        else:
            register_player_internal(is_update, player_id, constants.TYPE_CHAIR)
            user_message_text = f"🪑 {get_player_name(player)}, cел на стульчик на игру {get_next_matchday_formatted()}. На следующую игру свободных мест: {matchday_remaining_free_slots}. На стуле до тебя сидят: {matchday_chair_count}. Контроль!"
            log(user_message_text)
    else:
        register_player_internal(is_update, player_id, constants.TYPE_CHAIR)
        user_message_text = f"🪑 {get_player_name(player)}, cел на стульчик на игру {get_next_matchday_formatted()}. Кстати, на следующую игру уже нет мест."
        log(user_message_text)
    return user_message_text

def register_player_internal(is_update, player_id, type):
    if is_update == True:
        database.update_registraion_player_matchday(get_next_matchday(), type, player_id)
    else:
        database.register_player_matchday(get_next_matchday(), type, player_id)
        