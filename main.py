from flask import Flask, jsonify, request, render_template, redirect, url_for, session, flash
from bs4 import BeautifulSoup
import requests
import subprocess

from json import load, loads, dump, dumps
import time
import builtins
from bs4 import BeautifulSoup
from requests import get
from flask import request
from discord_webhook import DiscordWebhook
import sqlite3
from flask import redirect, render_template, request, send_file, session, url_for

from urllib.parse import parse_qs
import scrapetube
from chat_downloader.sites import YouTubeChatDownloader
app = Flask(__name__)

db = sqlite3.connect("queries.db", check_same_thread=False)
cur = db.cursor()
# create a table channel_id message_id clip_desc, time, time_in_seconds, user_id, user_name, stream_link
cur.execute("CREATE TABLE IF NOT EXISTS QUERIES(channel_id VARCHAR(40), message_id VARCHAR(40), clip_desc VARCHAR(40), time int, time_in_seconds int, user_id VARCHAR(40), user_name VARCHAR(40), stream_link VARCHAR(40))")
db.commit()


@app.route('/')
def slash():
    return "if you can read this, then the program is running absolutely fine."

@app.route("/export")
def export():
    try:
        channel = parse_qs(request.headers["Nightbot-Channel"])
    except KeyError:
        return "Not able to auth"
    channel_id = channel.get("providerId")[0]
    return f"You can download the export from http://surajbhari.info:5001/exports/{channel_id}"

def get_channel_clips(channel_id:str):
    if not channel_id:
        return {}
    cur.execute(f"select * from QUERIES where channel_id=?", (channel_id, ))
    data = cur.fetchall()
    l = []
    for y in data:
        x = {}
        x['link'] = y[7]
        x['author'] = {
            'name': y[6],
            'id': y[5]
        }
        x['clip_time'] = y[5]
        x['time'] = y[4]
        x['message'] = y[2]
        x['stream_id'] = y[7].replace("https://youtu.be/", "").split("?")[0]
        x['dt'] = time.strftime('%Y-%m-%d %H:%M:%S UTC', time.localtime(y[3]))
        l.append(x)
    l.reverse()
    return l

@app.route("/exports/<channel_id>")
def exports(channel_id = None):
    return render_template("export.html", data=get_channel_clips(channel_id))

def get_channel_image(channel_id:str):
    if not channel_id:
        return "https://foreignpolicyi.org/wp-content/uploads/2022/04/avatar.jpg"
    try:
        channel_link = f"https://youtube.com/channel/{channel_id}"
        html_data = get(channel_link).text
        soup = BeautifulSoup(html_data, 'html.parser')
        channel_image = soup.find("meta", property="og:image")["content"]
    except Exception as e:
        channel_image = "https://foreignpolicyi.org/wp-content/uploads/2022/04/avatar.jpg"
        print(e)
        pass
    return channel_image

@app.route("/clip/<message_id>/")
@app.route("/clip/<message_id>/<clip_desc>")
def clip(message_id, clip_desc=None):
    request_time = time.time()
    if not message_id:
        return "No message id provided"
    if not clip_desc:
        clip_desc = "None"
    try:
        channel = parse_qs(request.headers["Nightbot-Channel"])
        user = parse_qs(request.headers["Nightbot-User"])
    except KeyError:
        return "Not able to auth"

    with open("creds.json", "r") as f:
        creds = load(f)
    
    channel_id = channel.get("providerId")[0]
    try:
        webhook_url = creds[channel_id]
    except KeyError:
        return "we don't have info where to send the clip to. contact owner of website where you got the link from."


    user_id = user.get("providerId")[0]
    user_name = user.get("displayName")[0]
    vids = scrapetube.get_channel(channel_id, content_type="streams")
    live_found_flag = False

    for vid in vids:
        if vid["thumbnailOverlays"][0]["thumbnailOverlayTimeStatusRenderer"]["style"] == "LIVE":
            live_found_flag = True
            break
    if not live_found_flag:
        return "No live stream found"
    #only get the previous chat and don't wait for new one
    vid = YouTubeChatDownloader().get_video_data(video_id=vid["videoId"])
    clip_time  = request_time - vid["start_time"]/1000000 + 5
    url = "https://youtu.be/"+vid["original_video_id"]+"?t="+str(int(clip_time))
    # if clip_time is in seconds. then hh:mm:ss format would be like
    hour = int(clip_time/3600)
    minute = int(clip_time/60) % 60
    second = int(clip_time) % 60
    if hour:
        hour_minute_second = f"{hour}:{minute}:{second}"
    else:
        hour_minute_second = f"{minute}:{second}"
    message_cc_webhook = f"**{clip_desc}** \n\n{hour_minute_second}<{url}>"
    channel_image = get_channel_image(user_id)

    # insert the entry to database
    cur.execute("INSERT INTO QUERIES VALUES(?, ?, ?, ?, ?, ?, ?, ?)", (channel_id, message_id, clip_desc, request_time, clip_time, user_id, user_name, url))
    db.commit()
    try:
        return f"Clip requested by {user_name} with message -> {clip_desc} at {hour_minute_second} sent to discord. See all clips at http://{request.host}{url_for('exports', channel_id=channel_id)}"
    finally:
        file_name = take_screenshot(url, clip_time)
        webhook = DiscordWebhook(url=webhook_url, content=message_cc_webhook, username= user_name + f" ({user_id})", avatar_url=channel_image)
        with open(file_name, "rb") as f:
            webhook.add_file(file=f.read(), filename="ss.jpg")
        response = webhook.execute()
        print(f"Sent screenshot to {user_name} from {channel_id} with message -> {clip_desc} {url}\n {response}")


def take_screenshot(video_url:str, seconds:int):
    # Get the video URL using yt-dlp
    try:
        video_info = subprocess.check_output(["yt-dlp", "-f", "bestvideo", "--get-url", video_url], universal_newlines=True)
    except subprocess.CalledProcessError as e:
        print("Error:", e)
        exit(1)

    # Remove leading/trailing whitespace and newline characters from the video URL
    video_url = video_info.strip()
    file_name = "ss.jpg"

    # FFmpeg command
    ffmpeg_command = [
        "ffmpeg",
        "-y",                     # say yes to prompts
        "-ss", str(seconds),      # Start time
        "-i", video_url,          # Input video URL
        "-vframes", "1",          # Number of frames to extract (1)
        "-q:v", "2",              # Video quality (2)
        "-hide_banner",           # Hide banner
        "-loglevel", "error",     # Hide logs
        file_name                 # Output image file
    ]

    try:
        subprocess.run(ffmpeg_command, check=True)
    except subprocess.CalledProcessError as e:
        print("Error:", e)
        exit(1)
    
    return file_name

app.run(host='0.0.0.0', port=5001)