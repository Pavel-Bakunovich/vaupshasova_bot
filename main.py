import os
import telebot
import constants
import helpers
import database
import deepseek
import random
from logger import log, log_error
from dotenv import load_dotenv
from telebot.types import ReactionTypeEmoji

load_dotenv()
API_KEY = os.environ['TELEGRAM_API_TOKEN']
log("Environment variabled loaded.")
bot = telebot.TeleBot(API_KEY)
log("Bot object initialized.")

@bot.message_handler(commands=['add'])
def add(message):
    #pin message
    #tb = telebot.TeleBot(api_bot)
    #message = tb.send_message(group_id, 'Test!')
    #tb.pin_chat_message(group_id, message.message_id)
    user_message_text = ""
    try:
        player = add_player_if_not_existant(message.from_user.first_name,
                                            message.from_user.last_name,
                                            message.from_user.username,
                                            message.from_user.id)
        if (helpers.allow_registration()):
            if (helpers.authorized(message.chat.id)):
                matchday = database.find_registraion_player_matchday(helpers.get_next_matchday(), message.from_user.id)
                if matchday is None:
                    if (database.get_matchday_players_count(helpers.get_next_matchday()) < 12):
                        database.register_player_matchday(helpers.get_next_matchday(), "add", player[0])
                        user_message_text = helpers.fill_template("✍️ {name}, ты добавлен в состав на игру {date}.",
                            name=get_player_name(player),
                            date=helpers.get_next_matchday_formatted())
                        log(user_message_text)
                    else:
                        user_message_text = helpers.fill_template("🪑 {name}, на игру {date} больше нет мест. Садим тебя в очередь на стульчик.", name=get_player_name(player),date=helpers.get_next_matchday_formatted())
                        log(user_message_text)
                        database.register_player_matchday(helpers.get_next_matchday(), "chair", player[0])
                else:
                    if matchday[2] == "add":
                        user_message_text = helpers.fill_template("{name}, ты ж уже записался!",name=get_player_name(player))
                    else:
                        if (database.get_matchday_players_count(helpers.get_next_matchday()) < 12):
                            user_message_text = helpers.fill_template("✍️ {name}, окей, переносим тебя в основной состав на игру {date}.", name=get_player_name(player),date=helpers.get_next_matchday_formatted())
                            log(user_message_text)
                            database.update_registraion_player_matchday(helpers.get_next_matchday(), "add", player[0])
                        else:
                            user_message_text = helpers.fill_template("🪑 {name}, на игру {date} больше нет мест. Садим тебя на стульчик.", name=get_player_name(player),date=helpers.get_next_matchday_formatted())
                            log(user_message_text)
                            database.update_registraion_player_matchday(helpers.get_next_matchday(), "chair", player[0])
        
                bot_message = bot.reply_to(message, user_message_text)
                bot.set_message_reaction(message.chat.id,
                                        message.message_id,
                                        [ReactionTypeEmoji('✍️')],
                                        is_big=True)
                send_random_joke(bot, message, player)
                send_abusive_comment(bot, bot_message, user_message_text)
            else:
                reply_to_unauthorized(bot, message, player)
        else:
            reply_registration_not_allowed(bot, message, player)
    except Exception as e:
        bot.reply_to(message, constants.UNHANDLED_EXCEPTION_MESSAGE)
        log_error(e)


@bot.message_handler(commands=['remove'])
def remove(message):
    user_message_text = ""

    try:
        player = add_player_if_not_existant(message.from_user.first_name,
                                            message.from_user.last_name,
                                            message.from_user.username,
                                            message.from_user.id)
        if (helpers.allow_registration()):
            if (helpers.authorized(message.chat.id)):
                matchday = database.find_registraion_player_matchday(helpers.get_next_matchday(), message.from_user.id)

                if matchday is None:
                    user_message_text = helpers.fill_template("{name}, тебя и так нету в составе на {date}!", name=get_player_name(player),date=helpers.get_next_matchday_formatted())
                else:
                    if matchday[2] == "remove":
                        user_message_text = helpers.fill_template("{name}, тебя и так нету в составе на {date}!", name=get_player_name(player),date=helpers.get_next_matchday_formatted())
                    else:
                        user_message_text = helpers.fill_template("❌ {name}, удален из состава на игру {date}!", name=get_player_name(player),date=helpers.get_next_matchday_formatted())
                        database.update_registraion_player_matchday(helpers.get_next_matchday(), "remove", player[0])
                log(user_message_text)
                bot_message = bot.reply_to(message, user_message_text)
                bot.set_message_reaction(message.chat.id,
                                        message.message_id,
                                        [ReactionTypeEmoji('😭')],
                                        is_big=True)
                send_random_joke(bot, message, player)
                send_abusive_comment(bot, bot_message, user_message_text)
            else:
                reply_to_unauthorized(bot, message, player)
        else:
            reply_registration_not_allowed(bot, message, player)
    except Exception as e:
        bot.reply_to(message, constants.UNHANDLED_EXCEPTION_MESSAGE)
        log_error(e)


@bot.message_handler(commands=['chair'])
def chair(message):
    user_message_text = ""
    try:
        player = add_player_if_not_existant(message.from_user.first_name,
                                            message.from_user.last_name,
                                            message.from_user.username,
                                            message.from_user.id)
        if (helpers.allow_registration()):
            if (helpers.authorized(message.chat.id)):
                matchday = database.find_registraion_player_matchday(helpers.get_next_matchday(), message.from_user.id)

                if matchday is None:
                    database.register_player_matchday(helpers.get_next_matchday(),
                                                    "chair", player[0])

                    user_message_text = helpers.fill_template("🪑 {name}, cел на стульчик на игру {date}" ,name=get_player_name(player),date=helpers.get_next_matchday_formatted())
                    log(user_message_text)
                else:
                    if matchday[2] == "add":

                        user_message_text = helpers.fill_template("🪑 {name}, окей, снимаем тебя с состава и записываем на стул на игру {date}!" ,name=get_player_name(player),date=helpers.get_next_matchday_formatted())
                        log(user_message_text)
                        database.update_registraion_player_matchday(helpers.get_next_matchday(), "chair", player[0])
                    if matchday[2] == "chair":
                        user_message_text = helpers.fill_template("🪑 {name}, так ты и так уже на стуле сидишь!" ,name=get_player_name(player))
                        log(user_message_text)
                    if matchday[2] == "remove":
                        user_message_text = helpers.fill_template("🪑 {name}, ты раньше минусовался, но записываем тебя на стул на игру {date}! Так уж и быть." ,name=get_player_name(player),date=helpers.get_next_matchday_formatted())
                        log(user_message_text)
                        database.update_registraion_player_matchday(helpers.get_next_matchday(), "chair", player[0])

                bot_message = bot.reply_to(message, user_message_text)
                bot.set_message_reaction(message.chat.id,
                                        message.message_id,
                                        [ReactionTypeEmoji('✍️')],
                                        is_big=True)
                send_random_joke(bot, message, player)
                send_abusive_comment(bot, bot_message, user_message_text)
            else:
                reply_to_unauthorized(bot, message, player)
        else:
            reply_registration_not_allowed(bot, message, player)
    except Exception as e:
        bot.reply_to(message, constants.UNHANDLED_EXCEPTION_MESSAGE)
        log_error(e)

import datetime
@bot.message_handler(commands=['squad'])
def squad(message):
    try:
        current_player = add_player_if_not_existant(message.from_user.first_name,
                                            message.from_user.last_name,
                                            message.from_user.username,
                                            message.from_user.id)
        if (helpers.allow_registration()):
            if (helpers.authorized(message.chat.id)):
                with open(constants.SQUAD_TEMPLATE_FILENAME,"r") as squad_template_file:
                    squad_template_text = squad_template_file.read()
                squad_template_text = squad_template_text.replace("{date}", helpers.get_next_matchday_formatted())

                matchday_roster = database.get_squad(helpers.get_next_matchday())
                today = helpers.get_today_minsk_time()
                #today = datetime.date(year = 2025, month = 3, day = 29) - for debugging
                i = 1
                for player in matchday_roster:
                    if player[2] == 'add':
                        if today.weekday() == 5:
                            if player[5] == True:
                                squad_template_text = squad_template_text.replace("{Player " + str(i) + "}", "👀 " + get_player_name_extended(player))
                            else:
                                squad_template_text = squad_template_text.replace("{Player " + str(i) + "}", "💤 " + get_player_name_extended(player))
                        else:
                            squad_template_text = squad_template_text.replace("{Player " + str(i) + "}", get_player_name_extended(player))
                        i += 1

                for player in matchday_roster:
                    if (player[2] == 'chair'):
                        if today.weekday() != 5:
                            squad_template_text += "\n🪑 " + get_player_name_extended(player)

                for player in matchday_roster:
                    if (player[2] == 'remove'):
                        if today.weekday() != 5:
                            squad_template_text += "\n❌ " + get_player_name_extended(player)

                slots = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
                for x in slots:
                    squad_template_text = squad_template_text.replace(
                        "{Player " + str(x) + "}", "")

                bot.reply_to(message, squad_template_text)
                log(helpers.fill_template("Squad list requested by {name}",name=get_player_name_formal(current_player)))
                send_random_joke(bot, message, current_player)
            else:
                reply_to_unauthorized(bot, message, player)
        else:
            reply_registration_not_allowed(bot, message, current_player)
    except Exception as e:
        bot.reply_to(message, constants.UNHANDLED_EXCEPTION_MESSAGE)
        log_error(e)

@bot.message_handler(commands=['split'])
def split(message):
    try:
        current_player = add_player_if_not_existant(message.from_user.first_name,
                                            message.from_user.last_name,
                                            message.from_user.username,
                                            message.from_user.id)
        if (helpers.allow_registration()):
            if (helpers.authorized(message.chat.id)):
                with open(constants.SPLIT_SQUAD_TEMPLATE_FILENAME,"r") as split_squad_template_file:
                    split_squad_template_text = split_squad_template_file.read()
                matchday_roster = database.get_squad(helpers.get_next_matchday())

                i = 1
                squad_list = ""
                for player in matchday_roster:
                    if player[2] == 'add':
                        squad_list += helpers.fill_template("{number}. {name}\n", number=i, name=get_player_name_extended(player))
                        i += 1

                split_squad_template_text = helpers.fill_template(split_squad_template_text, squad=squad_list)
            
                split_squad = deepseek.send_request(split_squad_template_text, 0)

                bot.reply_to(message, split_squad)
                log(helpers.fill_template("Split squad with GenAI command requested by {name}",name=get_player_name_formal(current_player)))
                send_random_joke(bot, message, current_player)
            else:
                reply_to_unauthorized(bot, message, player)
        else:
            reply_registration_not_allowed(bot, message, current_player)
    except Exception as e:
        bot.reply_to(message, constants.UNHANDLED_EXCEPTION_MESSAGE)
        log_error(e)

@bot.message_handler(commands=['joke'])
def joke(message):
    try:
        player = add_player_if_not_existant(message.from_user.first_name,
                                            message.from_user.last_name,
                                            message.from_user.username,
                                            message.from_user.id)
        
    

        if (helpers.authorized(message.chat.id)):
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

@bot.message_handler(commands=['talk'])
def talk(message):
    try:
        player = add_player_if_not_existant(message.from_user.first_name,
                                            message.from_user.last_name,
                                            message.from_user.username,
                                            message.from_user.id)
        
        if (helpers.authorized(message.chat.id)):
            with open(constants.TALK_PROMPT_TEMPLATE_FILENAME,"r") as talk_prompt_template_file:
                talk_prompt_template_text = talk_prompt_template_file.read()
           
            parts = message.text.split(' ', 1)
            if len(parts) > 1:
                params = parts[1]
                talk_prompt_template_text = helpers.fill_template(talk_prompt_template_text, player_prompt=params)
            else:
                talk_prompt_template_text = helpers.fill_template(talk_prompt_template_text, player_prompt="Ничего не сказал.")

            talk_prompt_template_text = helpers.fill_template(talk_prompt_template_text, player_name=get_player_name_formal(player))

            response = deepseek.send_request(talk_prompt_template_text, 1.5)

            bot.reply_to(message, response)
            log(helpers.fill_template("Talk command requested by {name}: \'{player_message}\'",name=get_player_name_formal(player),player_message=params))
        else:
            reply_to_unauthorized(bot, message, player)
    except Exception as e:
        bot.reply_to(message, constants.UNHANDLED_EXCEPTION_MESSAGE)
        log_error(e)

@bot.message_handler(commands=['wakeup'])
def wakeup(message):
    try:
        player = add_player_if_not_existant(message.from_user.first_name,
                                            message.from_user.last_name,
                                            message.from_user.username,
                                            message.from_user.id)
        
        today = helpers.get_today_minsk_time()
        if today.weekday() == 5:
            if (helpers.authorized(message.chat.id)):
                still_sleeping_count = database.wakeup(helpers.get_next_matchday(), player[0])
                
                if still_sleeping_count == 0:
                    bot.reply_to(message, "Все проснулись! ☀️")
                else:
                    if still_sleeping_count <= 3:
                        bot.reply_to(message, helpers.fill_template("Ждем еще пока проснутся {count} сплюшки", count=still_sleeping_count))

                bot.set_message_reaction(message.chat.id,
                             message.message_id, [ReactionTypeEmoji('👍')],
                             is_big=True)

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

def send_random_joke(bot, message, player):
    response = ""
    prompt = ""
    random_number = random.random()
    if (random_number < 0.20):
        prompt = "Придумай злобную шутку про Манчестер Юнайтед. Используй обидные обзывательства. К этому сообщению имеет отношение {name}. Больльщики Манчестер Юнайтед в нашем чате: Сергей Мшар и Дима Шилько. Шутка не должна быть слишком длинной - максимум 2 предложения."
        
    else:
        if (random_number > 0.80):
            prompt = "Придумай злобную шутку про Максима Окунева. Он старый толстый игрок. Шутка должна быть в следующем формате. Вот два примера: На улице летом скоро будет 30, а тебе уже не будет . Кефир обезжиренный, а ты нет. В шутке обязательно должно быть упомянуто имя Максим. В ответа включи только одну шутку."

    if prompt != "":
        response = deepseek.send_request(helpers.fill_template(prompt, name = get_player_name(player)), 1.5)
        bot.send_message(message.chat.id, response)
        log(helpers.fill_template("Random joke sent: \'{joke}\'", joke=response))

def send_abusive_comment(bot, message, bot_message):
    if (random.random() < 0.20):
        abusive_message = deepseek.send_request(helpers.fill_template(constants.ABUSIVE_COMMENT_DEEPSEEK, bot_message = bot_message), 1.5)
        bot.reply_to(message, abusive_message)
        log(helpers.fill_template("Abusive comment sent: \'{joke}\'", joke=abusive_message))

def get_player_name_extended(player):
    if (player[11] is None):
        return str(player[7]) + " " + str(player[8]) + " (" + str(
            player[9]) + ")"
    else:
        return str(player[11]) + " " + str(player[12])

def get_player_name(player):
    if (player[5] is None):
        return str(player[1]) + " " + str(player[2]) + " (" + str(
            player[3]) + ")"
    else:
        return str(player[7])

def get_player_name_formal(player):
    if (player[5] is None):
        return str(player[1]) + " " + str(player[2]) + " (" + str(
            player[3]) + ")"
    else:
        return str(player[5]) + " " + str(player[6])

def add_player_if_not_existant(first_name, last_name, username, telegram_id):
    player = database.find_player(telegram_id)
    if player is None:
        return database.create_player(first_name, last_name, username, telegram_id)
    else:
        return player

def reply_registration_not_allowed(bot, message, player):
    bot.reply_to(
        message,
        helpers.fill_template(
            "{player_name}, eще рано. Регистрация на {date} открывается в понедельник.",
            date=helpers.get_next_matchday_formatted(),
            player_name=get_player_name(player)))
    bot.set_message_reaction(message.chat.id,
                             message.message_id, [ReactionTypeEmoji('🤬')],
                             is_big=True)
    log(helpers.fill_template("Too early for registration message sent to {name}", name=get_player_name_formal(player)))

def reply_to_unauthorized(bot, message, player):
    bot.reply_to(message,"Вам нельзя пользоваться этим ботом. Он предназначается эксклюзивно для Лиги Ваупшасова.")
    bot.set_message_reaction(message.chat.id,
                             message.message_id, [ReactionTypeEmoji('🤬')],
                             is_big=True)
    log(helpers.fill_template("Unauthorized message sent: \'{name}\', (id: {id})", name=get_player_name_formal(player),id=message.from_user.id))

log("Started polling.")
bot.polling()