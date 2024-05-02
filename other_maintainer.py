import json
from discord_webhook import DiscordWebhook, DiscordEmbed
import time
import requests as request
import os
import psutil
from main import *
import threading
from requests import get

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
    clips = get("https://streamsnip.com/data").json()[:250]
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
    time.sleep(60*30)
