from flask import Flask

from json import load, loads, dump, dumps
import time
from flask import request
from discord_webhook import DiscordWebhook

from urllib.parse import parse_qs
import scrapetube
from chat_downloader.sites import YouTubeChatDownloader
app = Flask(__name__)


@app.route('/')
def slash():
    return 'Hello World!'

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
        return "we don't have info where to send the clip to. contact owner of this stuff."


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
    clip_time  = request_time - vid["start_time"]/1000000 - 5
    url = "https://youtu.be/"+vid["original_video_id"]+"?t="+str(int(clip_time))
    message_cc_webhook = f"Clip requested by {user_name} ({user_id})\n{clip_desc}\n{url}"
    webhook = DiscordWebhook(url=webhook_url, content=message_cc_webhook)
    response = webhook.execute()
    return f"Clip requested by {user_name} with message -> {clip_desc} {url}"


app.run(host='0.0.0.0', port=5001)