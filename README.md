# clip_nightbot

The whole purpose of this is to ease the process of clipping
after extensive issue in clipping by my one of the favorite streamer. I made this </br>

How to Use ? 

2 options 
1 ) give me discord webhook url and your youtube channel link. I can host it for you for the time being

or

Host it yoursef
first edit `creds.json` with channelid and discord webhook where the request is to be done </br>
and then just run `main.py` `python3 main.py` </br>
you can use `nohup python3 main.py &` to run the script in background </br>
PLEASE NOTE THAT THE PORT 5001 is open to world for this to be discoverable.

Nightbot command:
`​!addcom !clip $(urlfetch http://your_host_here:5001/clip/$(chatid)/$(querystring))`

you can add `-ul=userlevel` userlevel can be found [here](https://docs.nightbot.tv/commands/commands#advanced-usage) to decrease the spam and allow only particular person to do the clipping part (mods etc.)

![alt text](/assets/Screenshot_156.png)
![alt text](/assets/Screenshot_157.png)
