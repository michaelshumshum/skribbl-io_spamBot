import time
import random
import string
import random
from multiprocessing import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

driverDirectory = '/Users/michaelshum/Desktop/dumb_python_scripts/WebDrivers/chromedriver' #Put the directory of the chromedriver here.
url = 'https://skribbl.io'

bots = []

messages = ['George Floyd deserved to die! Fuck all niggers!', 
'The Jews deserved the Holocaust! Hitler was a great man!', 
'Nothing worse than tiny eyed chinks. Stay in China you fucking assholes!', 
'Bow down to America you degenerate scum! Especially you Chinese faggots.', 
'Stay in the fucking ghetto you niggers. There is no place for black rats like you!',
'Legalize slavery! Chinks, Jews, and Niggers have no right to be free.',
'Life would be better if only white men existed.',
'Heil Hitler! He was the chosen one to bring reform to the world!',
'Stay in Mexico you Spanish whores! Fucking build our wall already.',
'Go back to Iraq and fight with the Taliban you fucking terrorists! Cant wait for 9/11 part 2.',
'Cant wait to nuke all of you fucking bastards. See you in hell, sucking Satans dick.']

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

def botfunc():
	while True:
		while True:
			global driver
			chrome_options = Options()
			chrome_options.add_argument("--headless")
			chrome_options.add_argument("--mute-audio")
			driver = webdriver.Chrome(executable_path=driverDirectory, chrome_options=chrome_options) #Change the directory to where your chromedriver is located.
			driver.implicitly_wait(10) 
			driver.get(url)
			try:
				driver.find_element_by_xpath('//*[@id="inputName"]').send_keys('spamBot') #Feel free to change the name.
				time.sleep(1)
				driver.find_element_by_xpath('/html/body/div[2]/div/a[1]').click()
				driver.find_element_by_xpath('//*[@id="formLogin"]/button[1]').click()
				time.sleep(3)
			except:
				driver.close()
				driver.quit()
				print '{} has crashed. Restarting...'.format(b.name)
				break

			while True:
				try:
					try:
						playerCount = (driver.find_element_by_xpath('//*[@id="containerGamePlayers"]')).size['height'] / 48
					except:
						playerCount = 1
					if playerCount > 1:
						chatSend('Hey there. I am spamBot. I am here to make this game hell for you.') #Feel free to change this line.
						chatSend('Please enjoy hell with me! *If you copy me, you will probably get kicked.') #Feel free to change this line.
						time.sleep(2.5)
						while True:
							try:
								chatSend(randomString(random.randint(1,99)))
								time.sleep(1)
								playerCount = (driver.find_element_by_xpath('//*[@id="containerGamePlayers"]')).size['height'] / 48
								if playerCount == 1:
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
					print '{} has crashed. Restarting...'.format(b.name)
					break

for i in range(0,4):
	b = Process(target=botfunc, name='Bot {}'.format(i+1))
	bots.append('bot{}'.format(i))
	b.start()