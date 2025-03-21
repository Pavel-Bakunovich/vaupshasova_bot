# vaupshasova_bot
Vaupshasova Bot
Это бот, который помогает друзьям собирать состав на игру в футбол - записаться, отписаться, вести список записавшихся на игру.

./google-cloud-sdk/bin/gcloud functions deploy vaupshasova_bot --set-env-vars "TELEGRAM_TOKEN=<TOKEN>" --runtime python312 --trigger-http --project=angular-lambda-289018 --source ./GitHub/vaupshasova_bot/


curl "https://api.telegram.org/bot<TOKEN>/setWebhook?url=https://us-central1-angular-lambda-289018.cloudfunctions.net/vaupshasova_bot"
