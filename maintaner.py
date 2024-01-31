import json
from discord_webhook import DiscordWebhook, DiscordEmbed
import time
import requests as request

management_webhook_url = None
management_webhook_url = json.load(open("creds.json", "r")).get('management_webhook', None)
if not management_webhook_url:
    exit("No management webhook found")


def periodic_task():
    management_webhook = DiscordWebhook(url=management_webhook_url)
    management_webhook.add_file(file=open("queries.db", "rb"), filename="queries.db")
    management_webhook.add_file(file=open("record.log", "rb"), filename="record.log")
    management_webhook.content = f"<t:{int(time.time())}:F>"
    try:
        management_webhook.execute()
    except request.exceptions.MissingSchema:
        exit("Invalid webhook URL")
        
while True:
    periodic_task()
    time.sleep(60)