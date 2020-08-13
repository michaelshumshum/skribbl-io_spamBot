# skribbl.io - spamBot
*kill games with spam*

## about
join skribbl.io games and spam random text with this script. if you play this game, you probably have seen it floating around at times. it uses chromedriver from selenium to interact with google chrome and the website. i'm not the savviest at writing code, so feel free to point out anything.

## features
- spams a random string of text at a random length every second. the spam can't be faster or else you will be automatically kicked super fast.
- prints live chat simultaneously
- automatically finds games, even when you get disconnected.
- when it's the bots turn to draw, it will automatically leave.
- anti-spam detection

## prerequisites 
- get python 2.7. if you have python 3, some of the lines will give you errors due to the updated api.
- install selenium using `pip install`. search that up if u dont know what to do.
- in the script, change the `driverDirectory` on line 9 to where your chromedriver is located. i included the driver in this repo, just put in the directory.

## optional stuff
- you can change `playerMinThreshold` on line 8 to whatever player count you want. don't put anything lower than 2 (obviously) or higher than 8 (max players in a game).
- feel free to change the text it spams, the name of the bot, and the chat it shows.
- you can disable line 11 if you want to see the game. i have the option turned on so i can free up some ram.

## CHANGELOG
V1.0
- release.

V1.1
- imported the threading module to read chat live instead of updating every 5 seconds.
- code has been optimised to look neater (and for a future project that may or may not be related to this).
