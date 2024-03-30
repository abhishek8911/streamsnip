# Clip_Nightbot/Streamsnip: Stream Clipping Simplified
![Streamsnip](https://cronitor.io/badges/l4zGl5/production/rOa5oshJWmlCgt3t1OQ4Yh5xXGc.svg)![Chart.js](https://img.shields.io/badge/chart.js-F5788D.svg?style=Flat&logo=chart.js&logoColor=white)![Flask](https://img.shields.io/badge/flask-%23000.svg?style=Flat&logo=flask&logoColor=white)![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=Flat&logo=amazon-aws&logoColor=white)![Python](https://img.shields.io/badge/python-3670A0?style=Flat&logo=python&logoColor=ffdd54)![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=Flat&logo=javascript&logoColor=%23F7DF1E)![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=Flat&logo=css3&logoColor=white)![Apache](https://img.shields.io/badge/apache-%23D42029.svg?style=Flat&logo=apache&logoColor=white)![YouTube](https://img.shields.io/badge/YouTube-%23FF0000.svg?style=Flat&logo=YouTube&logoColor=white)![Youtube Gaming](https://img.shields.io/badge/Youtube%20Gaming-FF0000?style=Flat&logo=Youtubegaming&logoColor=white)</br>
The primary goal of Clip_Nightbot is to streamline the clipping process, addressing challenges faced by one of my favorite streamers. Here's how you can make the most of it:
## Monetization
This program is a free for everyone as of now. But you can contribute. </br>
<a href="https://surajbhari.stck.me" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: 41px !important;width: 174px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;" ></a> </br>
Most of the donations goes back to development and hosting costing. 
## Nightbot Command:

```markdown
!addcom !clip $(urlfetch https://streamsnip.com/clip/$(chatid)/$(querystring))
```
Just adding this command will get you started. but if you want to have a discord message. or customization then read below.

If you want to send a discord message. then I would need to add a webhook URL alongside the youtube channel ID. for that fill [this form](https://forms.gle/NgF67HBR69CxAcvJ8) or contact me here.<br>
![Discord Badge](https://dcbadge.vercel.app/api/shield/408994955147870208) </br>
[![Server Badge](https://dcbadge.vercel.app/api/server/2XVBWK99Vy)](https://discord.gg/2XVBWK99Vy)


## Optional Arguments:

- `showlink` (default: true) - Display the link where all clips can be viewed.
- `screenshot` (default: false) - Enable or disable screenshot capture. If enabled the nightbot may not get response in given time and will say "Timed out" message. but it will still clip.
- `delay` (default: 0) - Introduce an artificial delay to the command. Useful for scheduling links in the future or past.
- `silent` (default: 2||Highest) - Level of the clipping message. see example below. </br> 
  ![image](https://github.com/SurajBhari/clip_nightbot/assets/45149585/f4e0bffa-1759-491a-ada9-c1ca4a55240b)
- `private` (default: false) - If set to true. the clips made are not shown on the web nor impact stats. if you don't want your channel to show up on website. you use it. This override `silent` and returns just ​​`clipped 😉` </br>
  ![image](https://github.com/SurajBhari/clip_nightbot/assets/45149585/42c6744e-f3d1-4335-822c-3c3713ac4ab4)
- `webhook` (default: None) - You can pass your own webhook rather than using the one you provided me (if you did), if combined with `private` you can make totally anonymous clips in a private channel.
  this take webhook in format of webhook_id/webhook_token
  ex. lets say a webhook is -> `https://discord.com/api/webhooks/1211440693168447599/ieU15QcFI_PcAun88TFGpUuRMK6E7Me14jioxB1mbJrRU6ay3XI8jByeEk3XKlVKr8_s` then you pass `webhook=1211440693168447599/ieU15QcFI_PcAun88TFGpUuRMK6E7Me14jioxB1mbJrRU6ay3XI8jByeEk3XKlVKr8_s`
- `message_level` (default: 0) - Customize how the discord message should look like. to support "anonymity"
  ![Untitled](https://github.com/SurajBhari/clip_nightbot/assets/45149585/614c15d8-d3d1-4765-ad7f-ee0a48965730)
- `take_delays` (default: false) - Do you consider your viewers to be smarter than average person ? if you turn this on. the first and last `word` will be evaluted to add/subtract delay.
  The following screenshot was taken with delay=0. but it still gave a delay of `20 seconds` as the clipper wrote `-20` as first word.  
  ![image](https://github.com/SurajBhari/clip_nightbot/assets/45149585/361dac19-192a-4a75-aa8f-0d94a480790d)


Here's one example using all of it.
```
https://streamsnip.com/clip/$(chatid)/$(querystring)?showlink=false&screenshot=true&delay=-30&private=true&webhook=1211440693168447599/ieU15QcFI_PcAun88TFGpUuRMK6E7Me14jioxB1mbJrRU6ay3XI8jByeEk3XKlVKr8_s&message_level=3
```

### Examples:
- `https://streamsnip.com/clip/$(chatid)/$(querystring)?showlink=false` - No links.
- `https://streamsnip.com/clip/$(chatid)/$(querystring)?showlink=false&screenshot=true` - No links, but with screenshots.
- `https://streamsnip.com/clip/$(chatid)/$(querystring)?screenshot=true` - Screenshots are given.
- `https://streamsnip.com/clip/$(chatid)/$(querystring)?delay=-20` - Set a delay in the past by 20 seconds.

## Other Commands
1. `!delete <clip_id>` - delete the given clip
```markdown
!addcom !delete $(urlfetch https://streamsnip.com/delete/$(query)) -ul=moderator
```
⚠️ don't remove the `-ul=moderator` part, otherwise anyone can delete your clips. </br>
![image](https://github.com/SurajBhari/clip_nightbot/assets/45149585/35d174c8-5f3f-4bb8-a6f7-15fc59ee0c43) </br>
  - `silent` (default: 2||Highest) - Level of returning message. 0 - no message. 1 - clip id(s) that was/were deleted. else no change.
---
2. `!edit <clip_id> <new_title>` - edit the title of the given clip
```markdown
!addcom !edit $(urlfetch https://streamsnip.com/edit/$(querystring)) -ul=moderator
```
⚠️ don't remove the `-ul=moderator` part, otherwise anyone can edit your clips. </br>
![image](https://github.com/SurajBhari/clip_nightbot/assets/45149585/f76e4bc6-dc20-4fa1-b58a-e237b4f7ba8f) </br>
  - `silent` (default: 2||Highest) - Level of returning message. 0 - no message. 1 - clip id that was edited. else no change.
---
3. `!clips` or `!export` - gives link where you can see all the clips 
```markdown
!addcom !export $(urlfetch https://streamsnip.com/export)
```
![image](https://github.com/SurajBhari/clip_nightbot/assets/45149585/7d72988e-0ab0-46a1-b7cb-0183e542eb2d)

---
#### Super Advanced, Proceed with caution here
4. `!search` gives the last clip that had the query in in it
 ```markdown
 !addcom !search $(urlfetch https://streamsnip.com/search/$(querystring))
```

SUPER PRO MODE </br>
Idea from [here](https://community.nightdev.com/t/clip-command-then-have-lastclip-automatically-update/35360), You can combine !search command to give out timestamp to particular events in the stream </br>
A combo can look like this 
```
!addcom !clipkill $(urlfetch https://streamsnip.com/clip/$(chatid)/kill-automated)
!addcom !lastkill $(urlfetch https://streamsnip.com/search/kill-automated)
```
Want more advanced ? here </br>
There is one more endpoint named `/searchx/<clip-desc>` that returns JSON of the clip with that clip-desc.</br>
THIS IS JUST 1 EXAMPLE. SKY IS THE LIMIT HERE
```
!addcom !lastkilltime $(eval clip=$(urlfetch json https://streamsnip.com/searchx/kill-automated); clip['hms'])
```
returning data looks something like this </br>
![carbon (3)](https://github.com/SurajBhari/clip_nightbot/assets/45149585/f7709890-6959-4a25-8a6d-292c9d20e10b)

6. `!uptime` gives uptime of the latest stream of the channel that called this command
   ```markdown
   !addcom !uptime $(urlfetch https://streamsnip.com/uptime)
   ```
   #### Args
   `level` - (default: 0) - What level of answer you want. ~~Here's a screenshot that showcase it.~~ soon. 
   
8. `!streaminfo` ADVANCED - this gives streaminfo in JSON format that you can use to do some other stuff.
   data looks something like this.
   ![carbon](https://github.com/SurajBhari/clip_nightbot/assets/45149585/811ec86a-9d69-4cc3-bde5-2d2cc66bd5ac)
   
   Route is at `/stream_info`
   ```markdown
   !addcom !myid $(eval info=$(urlfetch json https://streamsnip.com/stream_info); info['author_id'])
   ```

### Additional Customization:

You can use `-ul=userlevel` to limit clipping to specific user levels (e.g., mods). Find user levels [here](https://docs.nightbot.tv/commands/commands#advanced-usage) to reduce spam and grant clipping access to specific individuals.  </br>


---
