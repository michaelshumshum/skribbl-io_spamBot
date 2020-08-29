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

def chatupdate(queue):
	chat = driver.find_element_by_xpath('//*[@id="boxMessages"]').text
	chatlist = chat.splitlines()

	queue.put(['chat',chatlist])

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

def botrestart(queue):
	driver.close()
	driver.quit()
	queue.put([i,'Offline',round(time.time())])

def botinit(queue):
	global driver
	chrome_options = Options()
	chrome_options.add_argument("--headless")
	chrome_options.add_argument("--mute-audio")
	driver = webdriver.Chrome(executable_path=driverDirectory, chrome_options=chrome_options) #Change the directory to where your chromedriver is located.
	driver.implicitly_wait(25) 
	queue.put([i,'Initializing',round(time.time())])
	driver.get(url)

def botfunc(queue,num):
	global driver
	while True:
		while True:
			botinit(queue)
			try:
				driver.find_element_by_xpath('//*[@id="inputName"]').send_keys('spamBot') #Feel free to change the name.
				time.sleep(1)
				#driver.find_element_by_xpath('/html/body/div[2]/div/a[1]').click()
				driver.find_element_by_xpath('//*[@id="formLogin"]/button[1]').click()
			except:
				botrestart(queue)
				break
			_time = round(time.time())
			while True:
					queue.put([i,'Searching',_time])
					try:
						time.sleep(5)
						playerCount = (driver.find_element_by_xpath('//*[@id="containerGamePlayers"]')).size['height'] / 48
						if playerCount > 1:
							_time = round(time.time())
							chatSend('Hey there. I am spamBot. I am here to make this game hell for you.') #Feel free to change this line.
							chatSend('Please enjoy hell with me! *If you copy me, you will probably get kicked.') #Feel free to change this line.
							time.sleep(2.5)
							while True:
								try:
									try:
										driver.find_element_by_xpath('//*[@id="containerPlayerlist"]/div[2]').click()
									except:
										continue
									chatSend(randomString(random.randint(1,99)))
									#chatupdate(queue)
									time.sleep(1)
									playerCount = (driver.find_element_by_xpath('//*[@id="containerGamePlayers"]')).size['height'] / 48
									queue.put([i,'In game with {} players'.format(playerCount),_time])
									if playerCount < 2:
										relogin()
										queue.put(['chat','Disconnected'])
										break
									if (driver.find_element_by_xpath('//*[@id="overlay"]/div').get_attribute('style') == "bottom: 0%;") and (driver.find_element_by_xpath('//*[@id="overlay"]/div/div[1]').text == "Choose a word"):
										chatSend("Sorry, I wasn't made to draw. I was made only to spam.")
										time.sleep(0.2)
										chatSend('Your terror with me is now over. Take care now!')
										relogin()
										_time = round(time.time())
										#queue.put(['chat',['Disconnected']])
										break
								except:
									relogin()
									_time = round(time.time())
									break
						else: 
							relogin()
					except:
						botrestart(queue)
						break

bots = []

q = Queue()
parent, child = Pipe()

botCount = 8

for i in range(0,botCount):
	b = Process(target=botfunc, name='Bot {}'.format(i+1), args=(q,i,))
	bots.append('Bot {}'.format(i+1))
	b.start()
	time.sleep(0.75)

#GUI Stuff

def listening(conn):
	statuses = []
	chat = []
	times = []
	ingame = []
	for i in range(0,botCount):
		statuses.append('Offline')
		ingame.append('False')
		times.append(0.0)
	while True:
		recieve = q.get()
		num = recieve[0]
		if num == 'chat':
			chat = []
			chat = recieve[1]
			conn.send([chat,'chat'])
		else:
			line = recieve[1]
			if 'In game' in line:
				_ingame = True
			else:
				_ingame = False
			_time = recieve[2]
			times[num] = _time
			statuses[num] = line
			ingame[num] = _ingame
			conn.send([statuses,'status',times,ingame])

l = Process(target=listening, name='listening_process', args=(child,))
l.start()

class status(npyscreen.BoxTitle):
	_contained_widget = npyscreen.SimpleGrid
	entry_widget = npyscreen.SimpleGrid

class logs(npyscreen.BoxTitle):
	_contained_widget = npyscreen.Pager
	entry_widget = npyscreen.Pager

class choice(npyscreen.BoxTitle):
	_contained_widget = npyscreen.MultiLineAction
	entry_widget = npyscreen.MultiLineAction

class Form(npyscreen.Form):
	def create(self):
		rows, columns = os.popen('stty size').read().split()
		rows = int(rows)
		columns = int(columns)
		logsheight = -(rows-(botCount+5))
		self.btstat = self.add(status, name='bot statuses',editable=False,max_height=botCount+3)
		self.choice = self.add(choice, name='choice',editable=True,max_width=columns/12)
		self.logs = self.add(logs, name='logs',editable=False,relx=columns/12+2,rely=logsheight)
	def valueupdate(self):
		if recieved[1] == 'status':
			self.btstat.values = [['BOT NUMBER', 'STATUS', 'TIME IN STATUS']]
			for x in range(0,botCount):
				row = []
				times = recieved[2]
				statuses = recieved[0]
				row.append(bots[x])
				row.append(statuses[x])
				row.append(round(time.time())- times[x])
				self.btstat.values.append(row)
				ingame = recieved[3]
			for x in range(0,botCount):
				if (ingame[x] == True) and (bots[x] not in botsingame):
					botsingame.append(bots[x])
				elif (bots[x] in botsingame) and (ingame[x] == False):
					botsingame.remove(bots[x])
				botsingame.sort()
		if recieved[1] == 'chat':
			self.logs.values = recieved[0]
		elif 'Disconnected' in recieved[2]:
			self.logs.values = []
		self.choice.values = botsingame

def guifunc(*args):
	global botsingame
	botsingame = []
	gui = Form(name='skribbl.io - spamBot')
	while True:
		global recieved
		recieved = parent.recv()
		gui.valueupdate()
		gui.display()

print npyscreen.wrapper_basic(guifunc)

for bot in bots:
	bot.join()

