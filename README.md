# skribbl.io - spamBot
*kill games with spam (and spaghetti code)*

## about
join skribbl.io games and spam random text with this script. if you play this game, you probably have seen it floating around at times. it uses chromedriver from selenium to interact with google chrome and the website. i'm not the savviest at writing code, so feel free to point out anything.

## features
regular bot:
- spams a random string of text of a random length every second. the spam can't be faster or else you will be automatically kicked super fast.
- prints live chat simultaneously
- automatically finds games, even when you get disconnected.
- when it's the bots turn to draw, it will automatically leave.
- anti-spam detection.

bot swarm:
- does the same thing as the regular bot, but summons 8 bots at the same time.
- a few things are not implemented into this one:
      > spam detection
      > live chat updates
- easier to customize compared to the normal bot.
- crash detection, so the bots can run forever without issue.

## prerequisites 
- make sure to have the latest version of google chrome.
- get python 2.7. if you have python 3, some of the lines will give you errors due to the updated api.
- install selenium and npyscreen using `pip install`. search that up if u dont know what to do.
- in the script, change the `driverDirectory` on line 9 (line 13 in bot swarm) to where your chromedriver is located. i included the driver in this repo, just put in the directory.

## optional stuff
- you can change `playerMinThreshold` on line 8 whatever player count you want. don't put anything lower than 2 (obviously) or higher than 8 (max players in a game).
- feel free to change the text it spams, the name of the bot, and the chat it shows.

## CHANGELOG
v2.2
- gui now looks more organized and has two additional widgets: choice and logs.
- currently, choice only displays a list of bots that are in a game. logs doesn't do anything (yet).
- the chat log works with one bot at a time right now as i haven't implemented 'switching' feature. if you want, uncomment lines 86 and 92 and change botcount on line 113 to 1. this performs similiary to the original bot, but the textbox isn't scrollable, so you will only be able to see the first few lines before it cuts off. in general, it's still pretty garbage and will be worked on.
- in the next update, i am looking to change and fully implement chat logs and allow it to work on multiple bots at a time. for now, you will have to live without it.
- bot statuses now has a time in status column, telling how long the bot has been in it's current status.

v2.1
- bot swarm now has a simple UI that displays the status of each bot. uses the `npyscreen` module
- i will abadom the regular bot as it is pretty much useless. though, i will still keep it here.
- what's next:
      > adding an accesible chatlog for each bot.
      > better UI design
      
V2.0
- release of bot swarm script
- issue in the normal bot that needs attention:
      > 50% of the time when kicked, the bot will crash
      
V1.1.2
- i accidentally removed a `kicked` check for when the server kicks it manually. in the rare case it happened, the bot didn't know what to do and crashed. that has been added into the `disconnectCheck` thread.
- the reason to disconnect is provided when it is disconnecting.
- the threads now behave properly. a lot of times, the threads would continue, even when it is supposed to leave, resulting in the code stopping and preventing the code to go any further.

V1.1.1
- `disconnectCheck` is now run as a thread, instead of a called function. as long as only one of these bots are run at a time, it should not be a problem with workload.
- whenver a player leaves, you get notified of how many players are still in the game.
- spam detection has been changed to update live along side the `chatupdates`
- spam intervals has been changed to 0.85 seconds vs 1 second.
- every 15 attempts, the browser will restart. before, every 10 seconds, it would just switch to a new tab, which was completely retarded.

V1.1
- imported the threading module to read chat live instead of updating every 5 seconds.
- code has been optimised to look neater.
- removed `loadingLonger` check as it caused a bug where it would fail if the first attempt didn't load. also, it wasn't very necessary in most cases as the page rarely affected you finding games.
- starting work on botswarm.

V1.0
- initial release.


