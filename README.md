# Stock Availability Bot
I created this bot after failing to buy a new GPU in Dec 2020 due to low stocks and high demand. This bot detects when stocks become available on RPTechIndia.in (Only distributor with Nvidia FE cards that were priced reasonably) and sends an alert on Telegram about the available quantity and product page url.

This bot consists of webscraper hosted on AWS Lambda which checks product web pages every 15 mins and a telegram bot through which alert is sent if stock is present

All the dependencies for Lambda development package zip file are present in the repo.

# How to use:
1. Create a bot with https://t.me/botfather and get it's api token
2. Ping your bot with any message on Telegram (required to allow the bot to reply)
3. Go to https://api.telegram.org/bot{BOT_TOKEN}/getUpdates where {BOT_TOKEN} is the api token from step 1
4. Find the chat title(s) where the bot will alert and get their chat id(s). The chat information will be visible only after you have pinged the bot.
5. In the file lambda_function.py, replace YOUR_CHAT_ID and YOUR_BOT_SECRET with the chat id(s) from step 4 and api token from step 1
6. (Optional) If you want the alerts for multiple chats, you will need to edit the code to iterate over a list of chat ids when the function sends alerts
7. Execute the lambda_python.py on a schedule (I hosted on AWS Lambda and scheduled to run every 15mins using CloudWatch).

NOTE: Be sure to keep reasonable interval of time (10 - 15 mins) between the script runs, otherwise the website servers will reject the connection requests

This script can be easily modified to check multiple websites and products by just changing the alert criteria (eg:search if 'Add to Cart' is available)
