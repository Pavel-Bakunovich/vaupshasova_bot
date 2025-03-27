from logger import log, log_error
from telebot.types import ReactionTypeEmoji
import helpers
from helpers import authorized
from common import add_player_if_not_existant, send_random_joke, reply_to_unauthorized, get_player_name_formal
import database
import constants

def execute(message, bot):
    try:
        player = add_player_if_not_existant(message.from_user.first_name,
                                            message.from_user.last_name,
                                            message.from_user.username,
                                            message.from_user.id)
        
        today = helpers.get_today_minsk_time()
        if today.weekday() == 5:
            if (authorized(message.chat.id)):
                still_sleeping_count = database.wakeup(helpers.get_next_matchday(), player[0])
                
                if still_sleeping_count == 0:
                    bot.reply_to(message, "Все проснулись! ☀️")
                else:
                    if still_sleeping_count <= 3:
                        bot.reply_to(message, helpers.fill_template("Ждем еще пока проснутся {count} сплюшки", count=still_sleeping_count))

                bot.set_message_reaction(message.chat.id, message.message_id, [ReactionTypeEmoji('👍')], is_big=True)

                log(helpers.fill_template("Woke up: {name}",name=get_player_name_formal(player)))
                send_random_joke(bot, message, player)
            else:
                reply_to_unauthorized(bot, message, player)
        else:
            bot.reply_to(message, "Перекличка начинается в субботу! Еще рано.")
            bot.set_message_reaction(message.chat.id,
                             message.message_id, [ReactionTypeEmoji('🤬')],
                             is_big=True)
    except Exception as e:
        bot.reply_to(message, constants.UNHANDLED_EXCEPTION_MESSAGE)
        log_error(e)