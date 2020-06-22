# skribbl.io - spamBot
*kill games with spam*

## about
join skribbl.io games and spam random text with this script. if you play this game, you probably have seen it floating around at times. it uses chromedriver from selenium to interact with google chrome and the website. i'm not the savviest at writing code, so feel free to point out anything.

## features
- spams a random string of text at a random length every second. the spam can't be faster or else you will be automatically kicked super fast.
- prints chat to the shell every 0.5 seconds.
- automatically finds games, even when you get disconnected.
- when it's the bots turn to draw, it will automatically leave.
- anti-spam detection

## prerequisites 
- get python (duh).
- install selenium into your shell/into IDLE using pip install. search that up if u dont know what to do.
- in the script, change the `driverDirectory` to where your chromedriver is located. i included the driver in here, just put in the directory.

## optional stuff
- you can change the `playerMinThreshold` to whatever player count you want. don't put anything lower than 2 (obviously) or higher than 8 (max players in a game).
- feel free to change the text it spams, the name of the bot, and the chat it shows.
- you can disable line 11 if you want to see the game. i have the option so i can free up some ram.
