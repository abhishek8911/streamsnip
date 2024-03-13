from typing import Optional
from json import load, dump


def time_to_hms(seconds: int):
    hour = int(seconds / 3600)
    minute = int(seconds / 60) % 60
    second = int(seconds) % 60
    if hour < 10:
        hour = f"0{hour}"
    if minute < 10:
        minute = f"0{minute}"
    if second < 10:
        second = f"0{second}"
    if int(hour):
        hour_minute_second = f"{hour}:{minute}:{second}"
    else:
        hour_minute_second = f"{minute}:{second}"
    return hour_minute_second


def get_webhook_url(channel_id) -> Optional[str]:
    with open("creds.json", "r") as f:
        creds = load(f)

    try:
        webhook_url = creds[channel_id]
    except KeyError:
        return None
    return webhook_url
