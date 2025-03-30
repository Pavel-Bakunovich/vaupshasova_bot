from logger import log, log_error
import helpers
from helpers import authorized
from common import add_player_if_not_existant, reply_to_unauthorized, get_player_name_formal
import deepseek
import constants

def execute(message, bot):
    try:
        player = add_player_if_not_existant(message.from_user.first_name,
                                            message.from_user.last_name,
                                            message.from_user.username,
                                            message.from_user.id)
        
        if (authorized(message.chat.id)):
            with open(constants.TALK_PROMPT_TEMPLATE_FILENAME,"r") as talk_prompt_template_file:
                talk_prompt_template_text = talk_prompt_template_file.read()
           
            parts = message.text.split(' ', 1)
            params = ""
            if len(parts) > 1:
                params = parts[1]
                talk_prompt_template_text = helpers.fill_template(talk_prompt_template_text, player_prompt=params)
            else:
                talk_prompt_template_text = helpers.fill_template(talk_prompt_template_text, player_prompt="Ничего не сказал.")

            talk_prompt_template_text = helpers.fill_template(talk_prompt_template_text, player_name=get_player_name_formal(player))

            response = deepseek.send_request(talk_prompt_template_text, 0)

            bot.reply_to(message, response)
            log(helpers.fill_template("Talk command requested by {name}: \'{player_message}\'",name=get_player_name_formal(player),player_message=str(params)))
        else:
            reply_to_unauthorized(bot, message, player)
    except Exception as e:
        bot.reply_to(message, constants.UNHANDLED_EXCEPTION_MESSAGE)
        log_error(e)