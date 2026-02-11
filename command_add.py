from logger import log, log_error
from telebot.types import ReactionTypeEmoji
import helpers
from helpers import get_arguments, get_next_matchday_formatted
from common import get_player_name, add_player_if_not_existant_with_params, validate_access, reply_only_CEO_can_do_it, validate_CEO_zone
import database
import constants

def execute(message, bot):
    #pin message
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
            player_telegram_id = player[3]
            player_id = player[7]
            
            if validate_CEO_zone(message.from_user.id,get_arguments(message.text)):
                matchday = database.find_registraion_player_matchday(helpers.get_next_matchday(), player_telegram_id)
                #Fix this - this variable is not matchday_remaining_free_slots, it's matchday_regstered_players_count
                registered_players_count = database.get_matchday_players_count(helpers.get_next_matchday())
                if matchday is None:
                    if (registered_players_count < 12):
                        database.register_player_matchday(helpers.get_next_matchday(), constants.TYPE_ADD, player_id)
                        user_message_text = f"✍️ {get_player_name(player)}, ты добавлен в состав на игру {get_next_matchday_formatted()}."
                        check_eligibility_for_adding_to_squad(bot, message, registered_players_count, get_player_name(player), player_id)
                        log(user_message_text)
                    else:
                        user_message_text = f"🪑 {get_player_name(player)}, на игру {get_next_matchday_formatted()} больше нет мест. Садим тебя в очередь на стульчик."
                        log(user_message_text)
                        database.register_player_matchday(helpers.get_next_matchday(), constants.TYPE_CHAIR, player_id)
                else:
                    player_registration_type = matchday[1]
                    if player_registration_type == constants.TYPE_ADD:
                        user_message_text = helpers.fill_template("{name}, ты ж уже записался!",name=get_player_name(player))
                        log(user_message_text)
                    else:
                        if (registered_players_count < 12):
                            user_message_text = f"✍️ {get_player_name(player)}, окей, переносим тебя в основной состав на игру {get_next_matchday_formatted()}."
                            log(user_message_text)
                            check_eligibility_for_adding_to_squad(bot, message, registered_players_count, get_player_name(player), player_id)
                            database.update_registraion_player_matchday(helpers.get_next_matchday(), constants.TYPE_ADD, player_id)
                        else:
                            user_message_text = helpers.fill_template("🪑 {name}, на игру {date} больше нет мест! Садим тебя на стульчик.", name=get_player_name(player),date=helpers.get_next_matchday_formatted())
                            log(user_message_text)
                            database.update_registraion_player_matchday(helpers.get_next_matchday(), constants.TYPE_CHAIR, player_id)

                bot_message = bot.reply_to(message, user_message_text)
                bot.set_message_reaction(message.chat.id,
                                        message.message_id,
                                        [ReactionTypeEmoji('✍️')],
                                        is_big=True)
                
                registered_players_count = 12 - database.get_matchday_players_count(helpers.get_next_matchday())
                if (registered_players_count <= 3 and registered_players_count > 0):
                    bot.reply_to(message, f"⚠️ Внимание, осталось мест: {registered_players_count}")
                else:
                    if registered_players_count == 0:
                        bot.reply_to(message, "✅ Состав собран, господа присяжные заседатели! Состав собран!")
            else:
                reply_only_CEO_can_do_it(bot, message)

    except Exception as e:
        bot.reply_to(message, constants.UNHANDLED_EXCEPTION_MESSAGE)
        log_error(e)

#In case if player adds himself to the squad, we need to check if there are players on chair to be moved to squad first
def check_eligibility_for_adding_to_squad(bot, message, registered_players_count, name_of_player_to_add, player_id_to_add):
    if registered_players_count < 12:
        matchday_players_on_chair = database.get_matchday_players_on_chair(helpers.get_next_matchday())
        if len(matchday_players_on_chair) > 0:
            next_up_player = matchday_players_on_chair[0]
            player_name = next_up_player[3]
            player_id = next_up_player[0]
            telegram_login = next_up_player[4]
            if telegram_login == None:
                telegram_login = ""
            else:
                telegram_login = f" @{telegram_login}"
            if (player_id != player_id_to_add):
                message_to_player = f"🚨🚨🚨 Внимание! Фол! {name_of_player_to_add} добавился в состав вне очереди! {player_name}{telegram_login}, твоя очередь залетать в состав на игру {get_next_matchday_formatted()}, так как ты ждал очереди на стуле! Вызывайте милицию! Или звоните директору @pavel_bakunovich!"
                bot.reply_to(message, message_to_player)
                log(message_to_player)
            else:
                log(f"Player {name_of_player_to_add} was added to the squad, as per order. No faul committed.")
            
                