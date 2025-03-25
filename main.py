import os
import telebot
import constants
import helpers
import database
import deepseek
import random
from dotenv import load_dotenv
from telebot.types import ReactionTypeEmoji

load_dotenv()
API_KEY = os.environ['TELEGRAM_API_TOKEN']
bot = telebot.TeleBot(API_KEY)


@bot.message_handler(commands=['add'])
def add(message):
    # Split message text into parts and remove command
    #parts = message.text.split(' ', 1)
    # Check if parameters were provided
    #if len(parts) > 1:
    #    params = parts[1]  # This contains "Sergey Lisovskiy"
    #    print("Parameters:", params)
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
                    if (database.get_matchday_players_count(
                            helpers.get_next_matchday()) < 12):
        
                        database.register_player_matchday(helpers.get_next_matchday(), "add", player[0])
                        user_message_text = helpers.fill_template(
                            "✍️ {name}, ты добавлен в состав на игру {date}.",
                            name=get_player_name(player),
                            date=helpers.get_next_matchday_formatted())
                    else:
                        user_message_text = helpers.fill_template("🪑 {name}, на игру {date} больше нет мест. Садим тебя в очередь на стульчик.", name=get_player_name(player),date=helpers.get_next_matchday_formatted())
                        
                    
                        database.update_registraion_player_matchday(
                            helpers.get_next_matchday(), "chair", player[0])
                else:
                    if matchday[2] == "add":
                        user_message_text = helpers.fill_template("{name}, ты ж уже записался!",name=get_player_name(player))
                    else:
                        if (database.get_matchday_players_count(helpers.get_next_matchday()) < 12):
                            user_message_text = helpers.fill_template("✍️ {name}, окей, переносим тебя в основной состав на игру {date}.", name=get_player_name(player),date=helpers.get_next_matchday_formatted())
                            
                            database.update_registraion_player_matchday(
                                helpers.get_next_matchday(), "add", player[0])
                        else:
                            user_message_text = helpers.fill_template("🪑 {name}, на игру {date} больше нет мест. Садим тебя на стульчик.", name=get_player_name(player),date=helpers.get_next_matchday_formatted())
                            
                            database.update_registraion_player_matchday(
                                helpers.get_next_matchday(), "chair", player[0])
        
                bot.reply_to(message, user_message_text)
                bot.set_message_reaction(message.chat.id,
                                        message.message_id,
                                        [ReactionTypeEmoji('✍️')],
                                        is_big=True)
                send_random_joke(bot, message, player)
            else:
                reply_to_unauthorized(bot, message)
        else:
            reply_registration_not_allowed(bot, message, player)
    except Exception as e:
        bot.reply_to(message, "Чота я паламался. Давай по-новой.")
        print(e)


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
                        database.update_registraion_player_matchday(
                            helpers.get_next_matchday(), "remove", player[0])

                bot.reply_to(message, user_message_text)
                bot.set_message_reaction(message.chat.id,
                                        message.message_id,
                                        [ReactionTypeEmoji('😭')],
                                        is_big=True)
                send_random_joke(bot, message, player)
            else:
                reply_to_unauthorized(bot, message)
        else:
            reply_registration_not_allowed(bot, message, player)
    except Exception as e:
        bot.reply_to(message, "Чота я паламался. Давай по-новой.")
        print(e)


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
                else:
                    if matchday[2] == "add":

                        user_message_text = helpers.fill_template("🪑 {name}, окей, снимаем тебя с состава и записываем на стул на игру {date}!" ,name=get_player_name(player),date=helpers.get_next_matchday_formatted())
                        database.update_registraion_player_matchday(helpers.get_next_matchday(), "chair", player[0])
                    if matchday[2] == "chair":
                        user_message_text = helpers.fill_template("🪑 {name}, так ты и так уже на стуле сидишь!" ,name=get_player_name(player))
                    if matchday[2] == "remove":
                        user_message_text = helpers.fill_template("🪑 {name}, ты раньше минусовался, но записываем тебя на стул на игру {date}! Так уж и быть." ,name=get_player_name(player),date=helpers.get_next_matchday_formatted())

                        database.update_registraion_player_matchday(helpers.get_next_matchday(), "chair", player[0])

                bot.reply_to(message, user_message_text)
                bot.set_message_reaction(message.chat.id,
                                        message.message_id,
                                        [ReactionTypeEmoji('✍️')],
                                        is_big=True)
                send_random_joke(bot, message, player)
            else:
                reply_to_unauthorized(bot, message)
        else:
            reply_registration_not_allowed(bot, message, player)
    except Exception as e:
        bot.reply_to(message, "Чота я паламался. Давай по-новой.")
        print(e)


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
                i = 1
                for player in matchday_roster:
                    if player[2] == 'add':
                        squad_template_text = squad_template_text.replace(
                            "{Player " + str(i) + "}",
                            get_player_name_extended(player))
                        i += 1

                for player in matchday_roster:
                    if (player[2] == 'chair'):
                        squad_template_text += "\n🪑 " + get_player_name_extended(
                            player)

                for player in matchday_roster:
                    if (player[2] == 'remove'):
                        squad_template_text += "\n❌ " + get_player_name_extended(
                            player)

                slots = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
                for x in slots:
                    squad_template_text = squad_template_text.replace(
                        "{Player " + str(x) + "}", "")

                bot.reply_to(message, squad_template_text)
                send_random_joke(bot, message, current_player)
            else:
                reply_to_unauthorized(bot, message)
        else:
            reply_registration_not_allowed(bot, message, current_player)
    except Exception as e:
        bot.reply_to(message, "Чота я паламался. Давай по-новой.")
        print(e)

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

                send_random_joke(bot, message, current_player)
            else:
                reply_to_unauthorized(bot, message)
        else:
            reply_registration_not_allowed(bot, message, current_player)
    except Exception as e:
        bot.reply_to(message, "Чота я паламался. Давай по-новой.")
        print(e)

def send_random_joke(bot, message, player):
    response = ""
    prompt = ""
    random_number = random.random()
    if (random_number < 0.30):
        prompt = "Придумай злобную шутку про Манчестер Юнайтед. Используй обидные обзывательства. К этому сообщению имеет отношение {name}. Больльщики Манчестер Юнайтед в нашем чате: Сергей Мшар и Дима Шилько. Шутка не должна быть слишком длинной - максимум 2 предложения."
        
    else:
        if (random_number > 0.70):
            prompt = "Придумай злобную шутку про Максима Окунева. Он старый толстый игрок. Шутка должна быть в следующем формате. Вот два примера: На улице летом скоро будет 30, а тебе уже не будет . Кефир обезжиренный, а ты нет. В шутке обязательно должно быть упомянуто имя Максим. В ответа включи только одну шутку."

    if prompt != "":
        response = deepseek.send_request(helpers.fill_template(prompt, name = get_player_name(player)), 1.5)
        bot.send_message(message.chat.id, response)        

def get_player_name_extended(player):
    if (player[10] is None):
        return str(player[6]) + " " + str(player[7]) + " (" + str(
            player[8]) + ")"
    else:
        return str(player[10]) + " " + str(player[11])

def get_player_name(player):
    if (player[5] is None):
        return str(player[1]) + " " + str(player[2]) + " (" + str(
            player[3]) + ")"
    else:
        return str(player[7])

def add_player_if_not_existant(first_name, last_name, username, telegram_id):
    player = database.find_player(telegram_id)
    if player is None:
        return database.create_player(first_name, last_name, username,
                                      telegram_id)
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

def reply_to_unauthorized(bot, message):
    bot.reply_to(message,"Вам нельзя пользоваться этим ботом. Он предназначается эксклюзивно для Лиги Ваупшасова.")
    bot.set_message_reaction(message.chat.id,
                             message.message_id, [ReactionTypeEmoji('🤬')],
                             is_big=True)

bot.polling()
