import time
import random
import string
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

playerMinThreshold = 3 #Enter the minimum player threshold you desire (Note that the threshold includes the bot as well)
driverDirectory = '/Users/michaelshum/Downloads/chromedriver' #Put the directory of the chromedriver here.

chrome_options = Options()
chrome_options.add_argument("--headless")  #Disable if you want to see the game.
chrome_options.add_argument("--mute-audio")
driver = webdriver.Chrome(driverDirectory, chrome_options=chrome_options) #Change the directory to where your chromedriver is located.
driver.implicitly_wait(30) 

loadingLonger = 'n'

print('Entering skribbl.io...')
driver.get('https://skribbl.io/')
driver.find_element_by_xpath('//*[@id="inputName"]').send_keys('spamBot') #Feel free to change the name.
time.sleep(1)
driver.find_element_by_xpath('/html/body/div[2]/div/a[1]').click()

def chatLogPrint():
	global chatLogHistory
	chatLog = (driver.find_element_by_xpath('//*[@id="boxMessages"]').text)
	if chatLogHistory != chatLog:
		print(chatLog.replace(chatLogHistory,'').strip('\n'))
	time.sleep(0.5)
	chatLogHistory = chatLog

def chatSend(theString):
	driver.find_element_by_xpath('//*[@id="inputChat"]').send_keys(theString)
	driver.find_element_by_xpath('//*[@id="inputChat"]').submit()

def randomString(stringLength):
	lettersAndDigits = string.ascii_letters + string.digits
	return ''.join(random.choice(lettersAndDigits) for i in range(stringLength))

def gameSearch():
	global tryCount
	global playerCount
	global loadingLonger
	if (tryCount % 10 == 0) and (tryCount != 0):
		print('Starting a new tab session in an attempt to find a game more quickly...')
		driver.execute_script("window.open('','_blank');")
		driver.close()
		driver.switch_to_window(driver.window_handles[0])
		driver.get('https://skribbl.io')
		driver.find_element_by_xpath('//*[@id="formLogin"]/button[1]').click()
	elif (tryCount == 0):
		print('Starting game search...')
		if (firstSearch == 'n'):
			driver.refresh()
		driver.find_element_by_xpath('//*[@id="formLogin"]/button[1]').click()
	elif (loadingLonger == 'y'):
		loadingLonger = 'n'
	else:
		driver.refresh()
		driver.find_element_by_xpath('//*[@id="formLogin"]/button[1]').click()
	time.sleep(5)
	playerCount = (driver.find_element_by_xpath('//*[@id="containerGamePlayers"]')).size['height'] / 48
	tryCount = tryCount + 1
	if (playerCount == 0) and (driver.find_element_by_xpath('//*[@id="preroll"]').get_attribute('style').find("block;") > -1):
		print('[Attempt '),tryCount,(']: An ad played. Searching for a new game...')
	elif (playerCount == 0):
		print('Game is taking a while to load. Waiting a little longer...')
		loadingLonger = 'y'
		time.sleep(0.5)
		tryCount = tryCount - 1
	elif (playerCount < playerMinThreshold):
		print('[Attempt '),tryCount,(']: Game is below minimum player threshold (Threshold:'),playerMinThreshold,('- Player Count:'), playerCount,('). Searching for a new game...')
		chatSend('Just passing through...')
	else:
		joinedGameStart()

def joinedGameStart():
	global tryCount
	global chatLogHistory
	chatLogHistory = ''
	print('[Attempt '),tryCount,(']: Found a game above threshold with '),playerCount,(' players! Initiating spam...')
	print('[SHOWING CHAT NOW]')
	chatSend('Hey there. I am spamBot. I am here to make this game hell for you.') #Feel free to change this line.
	chatSend('Please enjoy hell with me! *If you copy me, you will probably get kicked.') #Feel free to change this line.
	time.sleep(2.5)
	tryCount = 0
	
playerCount = (driver.find_element_by_xpath('//*[@id="containerGamePlayers"]')).size['height'] / 48
tryCount = 0
firstSearch = 'y'
while(playerCount < playerMinThreshold):
	gameSearch()
firstSearch = 'n'


while(True):
	playerCount = (driver.find_element_by_xpath('//*[@id="containerGamePlayers"]')).size['height'] / 48
	if playerCount < 1:
		if playerCount == 0:
			print('[YOU HAVE BEEN KICKED MANUALLY BY THE SERVER! FINDING A NEW GAME...]')
		else:
			print('[ALL PLAYERS HAVE LEFT THE CURRENT GAME! FINDING A NEW GAME...')
		tryCount = 0
		while(playerCount < playerMinThreshold):
			gameSearch()
	spamChat = randomString(random.randint(1,99))
	chatSend(spamChat)
	chatLogLatest = (driver.find_element_by_xpath('//*[@id="boxMessages"]/p[last()]').text)
	chatLogPrint()

	if (chatLogLatest == "Spam detected! You're sending too many messages."): #Checks if the server has said we are spamming.
		print('[SERVER HAS DETECTED SPAM! PAUSING FOR 5 SECONDS...]')
		spamCooldown = 0
		while(spamCooldown < 5):
			chatLogPrint()
			chatLogPrint()
			spamCooldown = spamCooldown + 1
	playerCount = (driver.find_element_by_xpath('//*[@id="containerGamePlayers"]')).size['height'] / 48
	if playerCount < 1:
		if playerCount == 0:
			print('[YOU HAVE BEEN KICKED MANUALLY BY THE SERVER! FINDING A NEW GAME...]')
		else:
			print('[ALL PLAYERS HAVE LEFT THE CURRENT GAME! FINDING A NEW GAME...')
		tryCount = 0
		while(playerCount < playerMinThreshold):
			gameSearch()

	if (driver.find_element_by_xpath('//*[@id="overlay"]/div').get_attribute('style') == "bottom: 0%;") and (driver.find_element_by_xpath('//*[@id="overlay"]/div/div[1]').text == "Choose a word"): #Checks if spamBot is the drawer. If so, leaves the game before the players can kick.
		print('[YOU WERE CHOSEN TO DRAW! FINDING A NEW GAME...]')
		chatSend("Sorry, I wasn't made to draw. I was made only to spam.") #Feel free to change this line.
		chatSend('Your terror with me is now over. Take care now!') #Feel free to change this line.
		time.sleep(0.5)
		chatLogPrint()
		print('[STOPPED SHOWING CHAT]')
		driver.refresh()
		playerCount = (driver.find_element_by_xpath('//*[@id="containerGamePlayers"]')).size['height'] / 48
		tryCount = 0
		while(playerCount < playerMinThreshold):
			gameSearch()

	chatLogPrint()