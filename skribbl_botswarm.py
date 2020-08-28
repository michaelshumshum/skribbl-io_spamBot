import time
import random
import string
import random
import os
import sys
from multiprocessing import *
import npyscreen
from threading import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

driverDirectory = '/Users/michaelshum/Desktop/dumb_python_scripts/WebDrivers/chromedriver' #Put the directory of the chromedriver here.
url = 'https://skribbl.io/'

def chatSend(theString):
	driver.find_element_by_xpath('//*[@id="inputChat"]').send_keys(theString)
	driver.find_element_by_xpath('//*[@id="inputChat"]').submit()

def relogin():
	driver.refresh()
	time.sleep(1)
	driver.find_element_by_xpath('//*[@id="formLogin"]/button[1]').click()
	time.sleep(4)

def randomString(stringLength):
	lettersAndDigits = string.ascii_letters + string.digits
	return ''.join(random.choice(lettersAndDigits) for i in range(stringLength))

def botfunc(queue,num):
	while True:
		while True:
			global driver
			chrome_options = Options()
			chrome_options.add_argument("--headless")
			chrome_options.add_argument("--mute-audio")
			driver = webdriver.Chrome(executable_path=driverDirectory, chrome_options=chrome_options) #Change the directory to where your chromedriver is located.
			driver.implicitly_wait(15) 
			queue.put([i,'Initializing'])
			driver.get(url)
			try:
				driver.find_element_by_xpath('//*[@id="inputName"]').send_keys('spamBot') #Feel free to change the name.
				time.sleep(1)
				driver.find_element_by_xpath('//*[@id="formLogin"]/button[1]').click()
				time.sleep(3)
				while True:
					queue.put([i,'Searching'])
					try:
						try:
							playerCount = (driver.find_element_by_xpath('//*[@id="containerGamePlayers"]')).size['height'] / 48
						except:
							playerCount = 1
						if playerCount > 1:
							chatSend('Hey there. I am spamBot. I am here to make this game hell for you.') #Feel free to change this line.
							chatSend('Please enjoy hell with me! *If you copy me, you will probably get kicked.') #Feel free to change this line.
							playerCountStore = ''
							time.sleep(2.5)
							while True:
								try:
									try:
										driver.find_element_by_xpath('//*[@id="containerPlayerlist"]/div[2]').click()
									except:
										continue
									chatSend(randomString(random.randint(1,99)))
									time.sleep(1)
									playerCount = (driver.find_element_by_xpath('//*[@id="containerGamePlayers"]')).size['height'] / 48
									if playerCount != playerCountStore:
										queue.put([i,'In Game with {} players'.format(playerCount)])
										playerCountStore = playerCount
									if playerCount < 2:
										relogin()
										break
									if (driver.find_element_by_xpath('//*[@id="overlay"]/div').get_attribute('style') == "bottom: 0%;") and (driver.find_element_by_xpath('//*[@id="overlay"]/div/div[1]').text == "Choose a word"):
										chatSend("Sorry, I wasn't made to draw. I was made only to spam.")
										time.sleep(0.2)
										chatSend('Your terror with me is now over. Take care now!')
										relogin()
										break
								except:
									relogin()
									break
						else: 
							relogin()
					except:
						driver.close()
						driver.quit()
						queue.put([i,'Offline'])
						break
			except:
				driver.close()
				driver.quit()
				queue.put([i,'Offline'])
				break

bots = []

q = Queue()
parent, child = Pipe()

botCount = 8

for i in range(0,botCount):
	b = Process(target=botfunc, name='Bot {}'.format(i+1), args=(q,i,))
	bots.append('Bot {}'.format(i+1))
	b.start()
	time.sleep(0.1)

def listening(conn):
	statuses = []
	for i in range(0,botCount):
		statuses.append('Offline')
	while True:
		status = q.get()
		num = status[0]
		line = status[1]
		statuses[num] = line
		conn.send(statuses)

l = Process(target=listening, name='listening_process', args=(child,))
l.start()

def guifunc(*args):
	gui = npyscreen.Form(name='skribbl.io - spamBot')
	btstat = gui.add(npyscreen.SimpleGrid, name='bot statuses')

	while True:
		statuses = parent.recv()
		btstat.values = []
		for x in range(0,botCount):
			row = []
			row.append(bots[x])
			row.append(statuses[x])
			btstat.values.append(row)
		gui.display()

npyscreen.wrapper_basic(guifunc)

for bot in bots:
	bot.join()

