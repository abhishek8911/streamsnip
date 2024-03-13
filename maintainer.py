import json
from discord_webhook import DiscordWebhook, DiscordEmbed
import time
import requests as request
import os
import psutil
from main import *
import threading

management_webhook_url = None
management_webhook_url = json.load(open("creds.json", "r")).get(
    "management_webhook", None
)
if not management_webhook_url:
    exit("No management webhook found")


def download_clips(ids, thread_no):
    for clip_id in ids:
        out = download_and_store(clip_id)
        if isinstance(out, str):
            if "error" not in out.lower():
                management_webhook = DiscordWebhook(
                    url=management_webhook_url,
                    content=f"#{thread_no} - Downloaded - {out}",
                )
                management_webhook.execute()


DiscordWebhook(url=management_webhook_url, content="Maintainer started").execute()


def periodic_task():
    management_webhook = DiscordWebhook(url=management_webhook_url)
    management_webhook.add_file(file=open("queries.db", "rb"), filename="queries.db")
    management_webhook.add_file(file=open("record.log", "rb"), filename="record.log")
    management_webhook.content = f"<t:{int(time.time())}:F>"
    os.system("ps auxf > file.txt")
    time.sleep(1)
    management_webhook.add_file(file=open("file.txt", "rb"), filename="processes.txt")
    management_webhook.add_file(
        file=open("/var/log/apache2/error.log", "rb"), filename="error.log"
    )
    management_webhook.add_file(
        file=open("/var/log/apache2/access.log", "rb"), filename="access.log"
    )
    # management_webhook.add_file(file=open("creds.json", "rb"), filename="creds.json")
    # consturct a string that contains most important vitals of system
    # and send it to the webhook
    system_vitals = f"{task_count} CPU: {psutil.cpu_percent()}%\nMemory: {psutil.virtual_memory().percent}%\nDisk: {psutil.disk_usage('/').percent}%"
    management_webhook.content += system_vitals

    try:
        management_webhook.execute()
    except request.exceptions.MissingSchema:
        exit("Invalid webhook URL")
    if psutil.virtual_memory().percent > 90:
        management_webhook = DiscordWebhook(
            url=management_webhook_url, content="Memory usage is high RESTARTING SERVER"
        )
        management_webhook.execute()
        # restart the system
        os.system("reboot")

    if task_count % 30 != 0:
        return
    return  # lock it for now
    clips = get_channel_clips()[:250]
    clip_ids = [x.id for x in clips]
    already_downloaded = [x.split(".")[0] for x in os.listdir("clips")]
    need_to_download_ids = []
    # delete clips that are not in clips
    for clip in os.listdir("clips"):
        if clip.split(".")[0] not in clip_ids:
            os.remove(f"clips/{clip}")
            continue
        if clip.endswith(".part"):
            os.remove(f"clips/{clip}")
    need_to_download_ids = [x for x in clip_ids if x not in already_downloaded]
    management_webhook = DiscordWebhook(
        url=management_webhook_url,
        content=f"Need to download {len(need_to_download_ids)} clips, Already have {len(already_downloaded)} clips",
    )
    management_webhook.execute()

    # Number of threads for downloading
    num_threads = 3

    # Split `need_to_download_ids` into chunks for each thread
    chunk_size = len(need_to_download_ids) // num_threads
    chunks = [
        need_to_download_ids[i : i + chunk_size]
        for i in range(0, len(need_to_download_ids), chunk_size)
    ]

    # Create threads and start downloading
    threads = []
    thread_count = 1
    for chunk in chunks:
        thread = threading.Thread(
            target=download_clips,
            args=(
                chunk,
                thread_count,
            ),
        )
        thread_count += 1
        thread.start()
        threads.append(thread)

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # Send a message to the management webhook
    management_webhook = DiscordWebhook(
        url=management_webhook_url, content="Clips downloaded"
    )
    management_webhook.execute()


task_count = 0
while True:
    task_count += 1
    periodic_task()
    time.sleep(60)
