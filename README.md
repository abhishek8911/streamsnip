# Clip_Nightbot: Stream Clipping Simplified

The primary goal of Clip_Nightbot is to streamline the clipping process, addressing challenges faced by one of my favorite streamers. Here's how you can make the most of it:

## Usage Options:

1. **Hosted Solution:**
   Provide your Discord webhook URL and YouTube channel link, and I'll handle the hosting temporarily for you. 

   ![Discord Badge](https://dcbadge.vercel.app/api/shield/408994955147870208)
   ![Server Badge](https://dcbadge.vercel.app/api/server/2XVBWK99Vy)

2. **Self-Hosting:**
   If you prefer more control, follow these steps:
   - Edit `creds.json` with your channel ID and Discord webhook details.
   - Run `main.py` using `python3 main.py`.
   - Optionally, use `nohup python3 main.py &` to run the script in the background.

   *Note: Port 5001 must be open for external accessibility.*

## Nightbot Command:

```markdown
!addcom !clip $(urlfetch http://your_host_here:5001/clip/$(chatid)/$(querystring))
```

## Optional Arguments:

- `showlink` (default: true) - Display the link where all clips can be viewed.
- `screenshot` (default: false) - Enable or disable screenshot capture. If enabled the nightbot may not get response in given time and will say "Timed out" message. but it will still clip.
- `delay` (default: 0) - Introduce an artificial delay to the command. Useful for scheduling links in the future or past.

### Examples:

- `http://your_host_here:5001/clip/$(chatid)/$(querystring)?showlink=false&screenshot=false` - No links, no screenshots.
- `http://your_host_here:5001/clip/$(chatid)/$(querystring)?showlink=false` - No links, but with screenshots.
- `http://your_host_here:5001/clip/$(chatid)/$(querystring)?screenshot=false` - Links provided, no screenshots.
- `http://your_host_here:5001/clip/$(chatid)/$(querystring)?delay=-20` - Set a delay in the past by 20 seconds.

## Other Commands
1. `!delete <clip_id>` - delete the given clip
```
!addcom !delete $(urlfetch http://your_host_here:5001/delete/$(query)) -ul=moderator
```
⚠️ don't remove the `-ul=moderator` part, otherwise everyone can delete your clips.

2. `!clips` or `!export` - gives link where you can see all the clips 
```markdown
!addcom !export $(urlfetch http://your_host_here:5001/export/$(chatid))
```

3. `!cliptest` - test if the clipper is working
```markdown
!addcom !cliptest $(urlfetch http://your_host_here:5001/)
```
### Additional Customization:

You can use `-ul=userlevel` to limit clipping to specific user levels (e.g., mods). Find user levels [here](https://docs.nightbot.tv/commands/commands#advanced-usage) to reduce spam and grant clipping access to specific individuals.

![Screenshot 1](/assets/Screenshot_156.png)
![Screenshot 2](/assets/Screenshot_157.png)

---
