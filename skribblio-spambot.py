import time
import random
import string
import sys
import math
from multiprocessing import Process, Queue, Pipe
from subprocess import Popen
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

playerMinThreshold = 2 #Enter the minimum player threshold you desire (Note that the threshold includes the bot as well)
botCount = 4

global url
url = 'https://skribbl.io/'

loadingLonger = 'n'
process_list = list()
kicked = False
disconnect = False

def chatSend(theString):
	driver.find_element_by_xpath('//*[@id="inputChat"]').send_keys(theString)
	driver.find_element_by_xpath('//*[@id="inputChat"]').submit()

def randomString(stringLength):
	lettersAndDigits = string.ascii_letters + string.digits
	return ''.join(random.choice(lettersAndDigits) for i in range(stringLength))

def failedtoloadCheck(xpath):
	while True:
		try:
			driver.find_element_by_xpath(xpath).click()
			break
		except:
			driver.refresh()

def gameSearch():
	global botstatus
	global tryCount
	global playerCount
	global loadingLonger

	tryCount = 0
	while True:
		if (tryCount % 10 == 0) and (tryCount != 0):
			driver.execute_script("window.open('','_blank');")
			driver.close()
			driver.switch_to_window(driver.window_handles[0])
			driver.get(url)
			failedtoloadCheck('//*[@id="formLogin"]/button[1]')
		elif (tryCount == 0):
			driver.refresh()
			failedtoloadCheck('//*[@id="formLogin"]/button[1]')
		elif (loadingLonger == 'y'):
			loadingLonger = 'n'
		else:
			driver.refresh()
			failedtoloadCheck('//*[@id="formLogin"]/button[1]')
		time.sleep(5)
		playerCount = (driver.find_element_by_xpath('//*[@id="containerGamePlayers"]')).size['height'] / 48
		tryCount = tryCount + 1
		if (playerCount == 0) and (driver.find_element_by_xpath('//*[@id="preroll"]').get_attribute('style').find("block;") > -1):
			continue
		elif (playerCount == 0):
			loadingLonger = 'y'
			time.sleep(0.5)
			tryCount = tryCount - 1
		elif (playerCount < playerMinThreshold):
			chatSend('Just passing through...')
		else:
			joinedGameStart()
			return False

def chatSpam(): #Chat spam function
	while(True):
		chatSend(randomString(random.randint(1,99)))
		chatLogLatest = (driver.find_element_by_xpath('//*[@id="boxMessages"]/p[last()]').text)
		disconnectCheck()
		if disconnect == False:
			if (chatLogLatest == "Spam detected! You're sending too many messages."):
				time.sleep(5)
			else:
				time.sleep(0.85)
		else:
			chatSend("Sorry, I wasn't made to draw. I was made only to spam.")
			chatSend('Your terror with me is now over. Take care now!')
			time.sleep(1)
			return False

def disconnectCheck(): #Function to determine if the bot should disconnect.
	global disconnect
	global d_reason
	global kicked

	disconnect = False
	kicked == False

	while (disconnect == False) and (kicked != True):
		playerCount = (driver.find_element_by_xpath('//*[@id="containerGamePlayers"]')).size['height'] / 48
		if (playerCount < playerMinThreshold) and (playerCount != 0):
			disconnect = True
			print('\n[NOT ENOUGH PLAYERS IN THE GAME! PREPAREING TO LEAVE...]\n')
			d_reason = 1
		elif (driver.find_element_by_xpath('//*[@id="overlay"]/div').get_attribute('style') == "bottom: 0%;") and (driver.find_element_by_xpath('//*[@id="overlay"]/div/div[1]').text == "Choose a word"):
			disconnect = True
			print('\n[YOU WERE CHOSEN TO DRAW! PREPARING TO LEAVE...]\n')
			d_reason = 2
		else:
			disconnect = False

		if driver.find_element_by_xpath('//*[@id="modalKicked"]').get_attribute('style') == "display:block;":
			kicked = True
			print('\n[YOU WERE KICKED BY THE SERVER CONSOLE! FINDING A NEW GAME]\n')
		else:
			kicked = False

def joinedGameStart():
	global tryCount
	global chatLogHistory

	print'==================================='
	print p.name,' has joined a game!'
	print'==================================='
	firstSearch = 'n'
	chatSend('Hey there. I am spamBot. I am here to make this game hell for you.')
	chatSend('Please enjoy hell with me! *If you copy me, you will probably get kicked.')
	time.sleep(2.5)
	tryCount = 0

def botFunction(batch):
	for i in range(0,batch):
		driverDirectory = '/Users/michaelshum/Desktop/dumb_python_scripts/WebDrivers/chromedriver' #Put the directory of the chromedriver here.
		chrome_options = Options()
		chrome_options.add_argument("--headless")
		chrome_options.add_argument("--mute-audio")
		global driver
		driver = webdriver.Chrome(executable_path=driverDirectory, chrome_options=chrome_options) #Change the directory to where your chromedriver is located.
		driver.implicitly_wait(15) 
		driver.get(url)
		print'==================================='
		print p.name,' has successfully joined skribbl.io!'
		print'==================================='
		driver.find_element_by_xpath('//*[@id="inputName"]').send_keys('spamBot') #Feel free to change the name.
		time.sleep(1)
		driver.find_element_by_xpath('/html/body/div[2]/div/a[1]').click()

		while(True):
			gameSearch()
			chatSpam()
			print'==================================='
			print p.name,' has disconnected from its game!'
			print'==================================='

def printchat():
	while(True):
		global chatLogHistory
		chatLog = (driver.find_element_by_xpath('//*[@id="boxMessages"]').text)
		if chatLogHistory != chatLog:
			print(chatLog.replace(chatLogHistory,'').strip('\n'))
		chatLogHistory = chatLog
if botCount >= 8:
	cpus = cpu_count()
else:
	cpus = botCount

batch = int(math.ceil(float(botCount)/float(cpus)))

#Summoning Bots
for i in range(0,cpus):
	p = Process(name='Bot #{}'.format(i+1), target=botFunction, args=(batch,))
	process_list.append(p.name)
	p.start()
	print p.name + ' initiated.'
	time.sleep(0.1)
			
