# vaupshasova_bot
Vaupshasova Bot
Это бот, который помогает друзьям собирать состав на игру в футбол - записаться, отписаться, вести список записавшихся на игру.

./google-cloud-sdk/bin/gcloud functions deploy vaupshasova_bot --set-env-vars "TELEGRAM_TOKEN=TOKEN" --runtime python312 --trigger-http --project=angular-lambda-289018 --source ./GitHub/vaupshasova_bot/


curl "https://api.telegram.org/botTOKEN/setWebhook?url=https://us-central1-angular-lambda-289018.cloudfunctions.net/vaupshasova_bot"



Backlog:
1. Add ability to register player on their behalf. Like /add Сергей Лисовский. This is power user features, only for me.
2. Add chat restrtiction - only Лига Ваупшасова can use this bot.
3. Add GenAI. Let it joke around.
