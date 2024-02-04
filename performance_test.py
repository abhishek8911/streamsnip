import cronitor
import json
import time
from requests import get

config = json.load(open('testing_config.json', "r"))
cronitor.api_key = config["api_key"]
headers = {
    "Nightbot-Response-Url": "https://api.nightbot.tv/1/channel/send/",
    "Nightbot-User": "name=Suraj&displayName=Suraj&provider=youtube&providerId=UCbZZmB8L3IEHutGbvpWo9Ow&userLevel=owner",
    "Nightbot-Channel": "name=Lofi%20Girl&displayName=Lofi%20Girl&provider=youtube&providerId=UCSJ4gkVC6NrvII8umztf0Ow"
}
first_iteration = True
monitor = cronitor.Monitor.put(
    key='Streamsnip-Performance-Test',
    type='job',
    schedule='*/5 * * * *',
)
while True:
    while int(time.time()) % 300 != 0:
        continue
    first_iteration = False
    start_time = time.time() 
    #Or, you can embed telemetry events directly in your code
    monitor.ping(state='run')
    
    r = get("https://streamsnip.com/clip/PERFORMANCE-TEST/PERFORMANCE-TEST", headers=headers)
    print(r.text)
    if r.status_code != 200:
        monitor.ping(state='fail')
        continue
    r = get("https://streamsnip.com/searchx/PERFORMANCE-TEST", headers=headers)
    print(r.json())
    clip_id = r.json()['id']
    
    r = get(f"https://streamsnip.com/edit/{clip_id}%20NEW_TITLE", headers=headers)
    if r.status_code != 200:
        monitor.ping(state='fail')
        continue
    
    r = get(f"https://streamsnip.com/delete/{clip_id}", headers=headers)
    if r.status_code != 200:
        monitor.ping(state='fail')
        continue
    print("Time taken: ", time.time() - start_time, " seconds.")
    monitor.ping(state='complete')

