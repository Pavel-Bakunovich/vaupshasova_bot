from logger import log, log_error
from telegram import ReactionTypeEmoji
import helpers
from helpers import get_arguments, get_next_matchday, get_next_matchday_formatted
from common import add_player_if_not_existant_with_params, get_player_name,reply_only_CEO_can_do_it,validate_access,validate_CEO_zone
import database
import constants

async def execute(message, bot):
    user_message_text = ""

    try:
        player = add_player_if_not_existant_with_params(message.text,
                                                        message.from_user.first_name,
                                                        message.from_user.last_name,
                                                        message.from_user.username,
                                                        message.from_user.id)
        if await validate_access(message.chat.id, player, bot, message):
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
                        await player_signed_off_from_squad(player_registration_type, bot, message)
                log(user_message_text)
                bot_message = await bot.reply_to(message, user_message_text)
                await bot.set_message_reaction(message.chat.id,
                                        message.message_id,
                                        [ReactionTypeEmoji('😭')],
                                        is_big=True)
            else:
                await reply_only_CEO_can_do_it(bot, message)

    except Exception as e:
        await bot.reply_to(message, constants.UNHANDLED_EXCEPTION_MESSAGE)
        log_error(e)

async def player_signed_off_from_squad(registration_type, bot, message):
    if registration_type == constants.TYPE_ADD:
        matchday_remaining_free_slots = 12 - database.get_matchday_players_count(helpers.get_next_matchday())
        if matchday_remaining_free_slots > 0:
            # If there is only one free slot left after removing the player, we need to reassign "on chair" players to "in squad"
            matchday_players_on_chair = database.get_matchday_players_on_chair(helpers.get_next_matchday())
            if len(matchday_players_on_chair) > 0:
                next_up_player = matchday_players_on_chair[0]
                player_name = next_up_player[3]
                telegram_login = next_up_player[4]
                if telegram_login == None:
                    telegram_login = ""
                else:
                    telegram_login = f" @{telegram_login}"
                message_to_player = f"{player_name}{telegram_login}, твоя очередь залетать в состав на игру {get_next_matchday_formatted()}! Жми /add если готов заскакивать. Или /remove, /maybe если не готов. И давай скорее!"
                bot_message = await bot.reply_to(message, message_to_player)
                log(message_to_player)
                