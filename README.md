
# clip_nightbot

The whole purpose of this is to ease the process of clipping
after extensive issue in clipping by my one of the favorite streamer. I made this </br>

How to Use ? 

2 options 
1 ) give me discord webhook url and your youtube channel link. I can host it for you for the time being </br>
![](https://dcbadge.vercel.app/api/shield/408994955147870208)
![](https://dcbadge.vercel.app/api/server/2XVBWK99Vy) </br>

or

Host it yoursef
first edit `creds.json` with channelid and discord webhook where the request is to be done </br>
and then just run `main.py` `python3 main.py` </br>
you can use `nohup python3 main.py &` to run the script in background </br>
PLEASE NOTE THAT THE PORT 5001 is open to world for this to be discoverable.

Nightbot command:
`​!addcom !clip $(urlfetch http://your_host_here:5001/clip/$(chatid)/$(querystring))`

optional arguments
showlink (defaults to true) - shows the link where you can see all of the links </br>
screenshot (defaults to true) - take the screenshot or not. set it to false if you are facing issues with it</br>
delay (defaults to 0) - add a artifical delay to the command. useful if you want to show the link in future or in past </br>


`http://your_host_here:5001/clip/$(chatid)/$(querystring)?showlink=false&screenshot=false` - no links no screenshot </br>
`http://your_host_here:5001/clip/$(chatid)/$(querystring)?showlink=false` - no links but screenshot</br>
`http://your_host_here:5001/clip/$(chatid)/$(querystring)?screenshot=false` - links but no screenshot</br>

`http://your_host_here:5001/clip/$(chatid)/$(querystring)?delay=-20` - delay in past by 20 seconds.</br>


you can add `-ul=userlevel` userlevel can be found [here](https://docs.nightbot.tv/commands/commands#advanced-usage) to decrease the spam and allow only particular person to do the clipping part (mods etc.)

![alt text](/assets/Screenshot_156.png)
![alt text](/assets/Screenshot_157.png)
