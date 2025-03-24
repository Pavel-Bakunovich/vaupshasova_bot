# vaupshasova_bot
Vaupshasova Bot
Это бот, который помогает друзьям собирать состав на игру в футбол - записаться, отписаться, вести список записавшихся на игру.

DEPLOYMENT COMMAND TO GCP CLOUD RUN FUNCTIONS
./google-cloud-sdk/bin/gcloud functions deploy vaupshasova_bot --set-env-vars "TELEGRAM_TOKEN=TOKEN" --runtime python39 --trigger-http --project=angular-lambda-289018 --source ./GitHub/vaupshasova_bot/

SET AND REMOVE WEEBHOOKS
curl "https://api.telegram.org/botTOKEN/setWebhook?url=https://us-central1-angular-lambda-289018.cloudfunctions.net/vaupshasova_bot"
curl "https://api.telegram.org/botTOKEN/setWebhook?remove"

BACKLOG
1. Add ability to register player on their behalf. Like /add Сергей Лисовский. This is power user features, only for me.
2. ✅ Add chat restrtiction - only Лига Ваупшасова can use this bot.
3. Make the bot multi-account. So other football chats can use it.
4. Let bot pin a message and update it with the squad. Instead of /squad every time when y ou need to check out the squad.
5. ✅ Add GenAI. Let it joke around.
6. Add message when 3 seats are left: "3 места осталось.", "2 места осталось"...
7. ✅ Fix timezone issue
8. ✅ Find cheaper hosting
9. Bot should track those who hasn't yet woke up yet on a game day.
