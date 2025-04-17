from logger import log, log_error
import helpers
from helpers import allow_registration,authorized
from common import add_player_if_not_existant, send_random_joke, reply_registration_not_allowed, reply_to_unauthorized, get_player_name_formal, get_player_name_extended
import database
import constants
import deepseek

def execute(message, bot):
    try:
        current_player = add_player_if_not_existant(message.from_user.first_name,
                                            message.from_user.last_name,
                                            message.from_user.username,
                                            message.from_user.id)
        if (allow_registration()):
            if (authorized(message.chat.id)):
                with open(constants.SPLIT_SQUAD_TEMPLATE_FILENAME,"r") as split_squad_template_file:
                    split_squad_template_text = split_squad_template_file.read()
                matchday_roster = database.get_squad(helpers.get_next_matchday())

                i = 1
                squad_list = ""
                for player in matchday_roster:
                    if player[2] == constants.TYPE_ADD:
                        squad_list += helpers.fill_template("{number}. {name}\n", number=i, name=get_player_name_extended(player))
                        i += 1

                split_squad_template_text = helpers.fill_template(split_squad_template_text, squad=squad_list)
            
                split_squad = deepseek.send_request(split_squad_template_text, 0)

                bot.reply_to(message, split_squad)
                log(helpers.fill_template("Split squad with GenAI command requested by {name}",name=get_player_name_formal(current_player)))
            else:
                reply_to_unauthorized(bot, message, player)
        else:
            reply_registration_not_allowed(bot, message, current_player)
    except Exception as e:
        bot.reply_to(message, constants.UNHANDLED_EXCEPTION_MESSAGE)
        log_error(e)