import time
import random
import string
from threading import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

playerMinThreshold = 2 #Enter the minimum player threshold you desire (Note that the threshold includes the bot as well)
driverDirectory = '/Users/michaelshum/Desktop/dumb_python_scripts/WebDrivers/chromedriver' #Put the directory of the chromedriver here.
url = 'https://skribbl.io'

disconnect = False
d_reason = 1
pause = False
endthreads = False

print('\nEntering skribbl.io...')

def chatupdates():
	global chatLogHistory
	global chatLogLatest
	global pause
	global playerCount
	global endthreads

	endthreads = False
	playerCountStore = playerCount
	chatLogHistory = ''
	
	print('==============================')
	print('[SHOWING CHAT NOW]')

	while endthreads != True:
		playerCount = (driver.find_element_by_xpath('//*[@id="containerGamePlayers"]')).size['height'] / 48
		if playerCount != playerCountStore:
			print('\n[{} PLAYERS IN GAME.]\n').format(playerCount)
			playerCountStore = playerCount
		chatLogLatest = (driver.find_element_by_xpath('//*[@id="boxMessages"]/p[last()]').text)
		if (chatLogLatest == "Spam detected! You're sending too many messages."):
			pause = True
		else:
			pause = False

		chatLog = (driver.find_element_by_xpath('//*[@id="boxMessages"]').text)
		if chatLogHistory != chatLog:
			print(chatLog.replace(chatLogHistory,'').strip('\n'))
		chatLogHistory = chatLog
		
	print('[STOPPED SHOWING CHAT]')
	print('==============================')

def chatSend(theString):
	driver.find_element_by_xpath('//*[@id="inputChat"]').send_keys(theString)
	driver.find_element_by_xpath('//*[@id="inputChat"]').submit()

def randomString(stringLength):
	lettersAndDigits = string.ascii_letters + string.digits
	return ''.join(random.choice(lettersAndDigits) for i in range(stringLength))

def disconnectCheck(): #Function to determine if the bot should disconnect.
	global disconnect
	global d_reason
	disconnect = False
	while disconnect == False:
		playerCount = (driver.find_element_by_xpath('//*[@id="containerGamePlayers"]')).size['height'] / 48
		if playerCount < playerMinThreshold:
			disconnect = True
			d_reason = 1
		elif (driver.find_element_by_xpath('//*[@id="overlay"]/div').get_attribute('style') == "bottom: 0%;") and (driver.find_element_by_xpath('//*[@id="overlay"]/div/div[1]').text == "Choose a word"):
			disconnect = True
			d_reason = 2
		else:
			disconnect = False

def chatSpam(): #Chat spam function
	global pause
	global endthreads
	while(True):
		chatSend(randomString(random.randint(1,99)))
		if disconnect == False:
			if pause == True:
				print '[PAUSING...]'
				time.sleep(5)
			else:
				time.sleep(0.85)
		elif disconnect == True:
			if d_reason == 2:
				chatSend("Sorry, I wasn't made to draw. I was made only to spam.")
			if d_reason == 1:
				chatSend("You guys suck. I'm outta here.")
			chatSend('Your terror with me is now over. Take care now!')
			tc.join()
			td.join()
			time.sleep(3)
			endthreads = True
			break

def gameSearch():
	global tryCount
	global playerCount

	tryCount = 0
	while True:
		if (tryCount % 15 == 0) and (tryCount != 0):
			print('\nRestarting browser in an attempt to find a game more quickly...\n')
			driver.quit()
			initfunc()
			driver.find_element_by_xpath('//*[@id="formLogin"]/button[1]').click()
		elif (tryCount == 0):
			print('\n==============================')
			print('Starting game search...')
			driver.refresh()
			driver.find_element_by_xpath('//*[@id="formLogin"]/button[1]').click()
		else:
			driver.refresh()
			driver.find_element_by_xpath('//*[@id="formLogin"]/button[1]').click()
		time.sleep(8)
		playerCount = (driver.find_element_by_xpath('//*[@id="containerGamePlayers"]')).size['height'] / 48
		tryCount = tryCount + 1
		if (playerCount == 0) and (driver.find_element_by_xpath('//*[@id="preroll"]').get_attribute('style').find("block;") > -1):
			print('[Attempt '),tryCount,(']: An ad played. Searching for a new game...')
		elif (playerCount < playerMinThreshold):
			if playerCount == 0:
				playerCount = 1
			print('[Attempt '),tryCount,(']: Game is below minimum player threshold (Threshold:'),playerMinThreshold,('- Player Count:'), playerCount,('). Searching for a new game...')
			chatSend('Just passing through...')
		else:
			joinedGameStart()
			break

def joinedGameStart():
	global tryCount
	global chatLogHistory
	global tc
	global td
	print('[Attempt '),tryCount,(']: Found a game above threshold with '),playerCount,(' players! Initiating spam...\n')
	chatSend('Hey there. I am spamBot. I am here to make this game hell for you.') #Feel free to change this line.
	chatSend('Please enjoy hell with me! *If you copy me, you will probably get kicked.') #Feel free to change this line.
	time.sleep(2.5)

	tc = Thread(target=chatupdates)
	tc.start()

	td = Thread(target=disconnectCheck)
	td.start()

def initfunc():
	chrome_options = Options()
	chrome_options.add_argument("--headless")
	chrome_options.add_argument("--mute-audio")
	global driver
	driver = webdriver.Chrome(executable_path=driverDirectory, chrome_options=chrome_options) #Change the directory to where your chromedriver is located.
	driver.implicitly_wait(15) 
	driver.get(url)
	driver.find_element_by_xpath('//*[@id="inputName"]').send_keys('spamBot') #Feel free to change the name.
	time.sleep(1)
	driver.find_element_by_xpath('/html/body/div[2]/div/a[1]').click()

#Bot function
initfunc()
while True:
	gameSearch()
	time.sleep(1)
	chatSpam()


	
