from datetime import datetime, timezone
from util import *
from discord_webhook import DiscordWebhook

import sqlite3

class Clip:
    channel = None
    id = None
    message_id = None
    desc = None
    time = None
    time_in_seconds = None
    user_id = None
    user_name = None
    stream_link = None
    webhook = None
    delay = None
    userlevel = None
    ss_id = None
    ss_link = None
    private= False

    def __init__(self, data):
        # data is a [str]
        x = {}
        level = data[10]
        if not level:
            level = "everyone"
        self.userlevel = level
        self.stream_link = data[7]
        self.stream_id = data[7].split("/")[-1].split("?")[0]
        self.channel = data[0]
        self.id = data[1][-3:] + str(int(data[4]))
        self.message_id = data[1]
        self.desc = data[2]
        self.time = datetime.fromtimestamp(int(data[3]), tz=timezone.utc)
        self.time_in_seconds = data[4]
        self.user_id = data[5]
        self.user_name = data[6]
        self.delay = int(data[9]) if data[9] else 0
        self.webhook = data[8]
        self.ss_id = data[11]
        self.ss_link = data[12]
        self.hms = time_to_hms(self.time_in_seconds)
        self.download_link = f"/video/{self.id}"
        self.private = str(data[13]) == '1'
    
    def __str__(self):
        return self.desc
    
    def json(self):
        x = {}
        x["link"] = self.stream_link
        x["author"] = {"name": self.user_name, "id": self.user_id, "level": self.userlevel}
        x["clip_time"] = self.time_in_seconds
        x["time"] = self.time  # real life time when clip was made
        x["message"] = self.desc
        x["stream_id"] = self.stream_id
        x["dt"] = self.time.strftime("%Y-%m-%d %H:%M:%S")
        x["hms"] = self.hms
        x["id"] = self.id
        x["delay"] = self.delay
        x["discord"] ={
            "webhook": self.webhook,
            "ss_id": self.ss_id,
            "ss_link": self.ss_link
        }
        x['download_link'] = self.download_link
        x['private'] = self.private
        return x 
    
    def edit(self, new_desc:str, conn:sqlite3.Connection):
        with conn:
            cur = conn.cursor()
            cur.execute(
                "UPDATE QUERIES SET clip_desc=? WHERE channel_id=? AND message_id LIKE ? AND time_in_seconds >= ? AND time_in_seconds < ?",
                (
                    new_desc,
                    self.channel,
                    f"%{self.id[:3]}",
                    int(self.id[3:]) - 1,
                    int(self.id[3:]) + 1,
                ),
            )
        conn.commit()
        webhook_url = get_webhook_url(self.channel)
        if webhook_url and self.webhook:
            hms = self.hms
            new_message = f"{self.id} | **{new_desc}** \n\n{hms}\n<{self.stream_link}>"
            if self.delay:
                new_message += f"\nDelayed by {self.delay} seconds."
            webhook = DiscordWebhook(
                url=webhook_url,
                id=self.webhook,
                allowed_mentions={"role": [], "user": [], "everyone": False},
                content=new_message,
            )
            try:
                webhook.edit()
            except Exception as e:
                print(e)
                pass
        self.desc = new_desc
        return True
    
    def delete(self, conn:sqlite3.Connection):
        with conn:
            cur = conn.cursor()
            cur.execute(
                "DELETE FROM QUERIES WHERE channel_id=? AND message_id LIKE ? AND time_in_seconds >= ? AND time_in_seconds < ?",
                (self.channel, f"%{self.id[:3]}", self.time_in_seconds - 1, self.time_in_seconds + 1),
            )
            conn.commit()
        webhook_url = get_webhook_url(self.channel)
        if webhook_url and self.webhook:
            webhook = DiscordWebhook(
                url=webhook_url,
                id=self.webhook,
                allowed_mentions={"role": [], "user": [], "everyone": False},
            )
            try:
                webhook.delete()
            except Exception as e:
                print(e)
                pass
            if self.ss_id:
                webhook = DiscordWebhook(
                    url=webhook_url,
                    id=self.ss_id,
                    allowed_mentions={"role": [], "user": [], "everyone": False},
                )
                try:
                    webhook.delete()
                except Exception as e:
                    print(e)
                    pass
        return True