import json
from discord_webhook import DiscordWebhook, DiscordEmbed
import time
import requests as request
import os

management_webhook_url = None
management_webhook_url = json.load(open("creds.json", "r")).get('management_webhook', None)
if not management_webhook_url:
    exit("No management webhook found")

DiscordWebhook(url=management_webhook_url, content="Maintainer started").execute()
def periodic_task():
    management_webhook = DiscordWebhook(url=management_webhook_url)
    management_webhook.add_file(file=open("queries.db", "rb"), filename="queries.db")
    management_webhook.add_file(file=open("record.log", "rb"), filename="record.log")
    management_webhook.content = f"<t:{int(time.time())}:F>"
    os.system("ps auxf > file.txt")
    time.sleep(1)
    management_webhook.add_file(file=open("file.txt", "rb"), filename="processes.txt")
    management_webhook.add_file(file=open("/var/log/apache2/error.log", "rb"), filename="error.log")
    management_webhook.add_file(file=open("/var/log/apache2/access.log", "rb"), filename="access.log")
    management_webhook.add_file(file=open("creds.json", "rb"), filename="creds.json")
    try:
        management_webhook.execute()
    except request.exceptions.MissingSchema:
        exit("Invalid webhook URL")
        
while True:
    periodic_task()
    time.sleep(60)