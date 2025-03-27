from logger import log, log_error
from telebot.types import ReactionTypeEmoji
import helpers
from helpers import authorized
from common import add_player_if_not_existant, reply_to_unauthorized,get_player_name_formal
import constants
import deepseek

def execute(message, bot):
    try:
        player = add_player_if_not_existant(message.from_user.first_name,
                                            message.from_user.last_name,
                                            message.from_user.username,
                                            message.from_user.id)

        if (authorized(message.chat.id)):
            with open(constants.JOKE_PROMPT_TEMPLATE_FILENAME,"r") as joke_prompt_template_file:
                joke_prompt_template_text = joke_prompt_template_file.read()
           
            parts = message.text.split(' ', 1)
            if len(parts) > 1:
                params = parts[1]
                joke_prompt_template_text = helpers.fill_template(joke_prompt_template_text, message_from_player=params)
            else:
                joke_prompt_template_text = helpers.fill_template(joke_prompt_template_text, message_from_player="Ничего не сказал.")

            joke_prompt_template_text = helpers.fill_template(joke_prompt_template_text, name=get_player_name_formal(player))

            joke = deepseek.send_request(joke_prompt_template_text, 1.5)

            bot.reply_to(message, joke)
            log(helpers.fill_template("Joke requested by {name}",name=get_player_name_formal(player)))
        else:
            reply_to_unauthorized(bot, message, player)
    except Exception as e:
        bot.reply_to(message, constants.UNHANDLED_EXCEPTION_MESSAGE)
        log_error(e)