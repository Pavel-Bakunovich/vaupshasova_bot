from logger import log, log_error
from telebot.types import ReactionTypeEmoji
import helpers
from helpers import authorized
from common import add_player_if_not_existant, reply_to_unauthorized, get_player_name_extended, get_player_name_formal
import database
import constants
import datetime

def execute(message, bot):
    try:
        current_player = add_player_if_not_existant(message.from_user.first_name,
                                            message.from_user.last_name,
                                            message.from_user.username,
                                            message.from_user.id)
        if (authorized(message.chat.id)):
            with open(constants.SQUAD_TEMPLATE_FILENAME,"r") as squad_template_file:
                squad_template_text = squad_template_file.read()
            squad_template_text = squad_template_text.replace("{date}", helpers.get_next_matchday_formatted())

            matchday_roster = database.get_squad(helpers.get_next_matchday())
            today = helpers.get_today_minsk_time()
            #today = datetime.date(year = 2025, month = 3, day = 29)# - for debugging
            i = 1
            for player in matchday_roster:
                if player[2] == constants.TYPE_ADD:
                    if today.weekday() == 5:
                        if player[5] == True:
                            squad_template_text = squad_template_text.replace("{Player " + str(i) + "}", "👀 " + get_player_name_extended(player))
                        else:
                            squad_template_text = squad_template_text.replace("{Player " + str(i) + "}", "💤 " + get_player_name_extended(player))
                    else:
                        squad_template_text = squad_template_text.replace("{Player " + str(i) + "}", get_player_name_extended(player))
                    i += 1

            for player in matchday_roster:
                if (player[2] == constants.TYPE_CHAIR):
                    if today.weekday() != 5:
                        squad_template_text += "\n🪑 " + get_player_name_extended(player)

            for player in matchday_roster:
                if (player[2] == constants.TYPE_REMOVE):
                    if today.weekday() != 5:
                        squad_template_text += "\n❌ " + get_player_name_extended(player)

            slots = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
            for x in slots:
                squad_template_text = squad_template_text.replace(
                    "{Player " + str(x) + "}", "")

            bot.reply_to(message, squad_template_text)
            log(helpers.fill_template("Squad list requested by {name}",name=get_player_name_formal(current_player)))
        else:
            reply_to_unauthorized(bot, message, player)
    except Exception as e:
        bot.reply_to(message, constants.UNHANDLED_EXCEPTION_MESSAGE)
        log_error(e)