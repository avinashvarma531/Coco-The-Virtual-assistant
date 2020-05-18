import pyautogui as pg
from time import sleep
import webbrowser
import os

screenWidth,screenHeight=pg.size()

flg=True

pg.FAILSAFE=False

def googling(query):
	url='https://google.com/search?q='+query.replace(' ','+')
	webbrowser.get('windows-default').open(url)

def openSettings(app):
	pg.press('winleft')
	pg.typewrite(app)
	sleep(1)
	pg.press('enter')

def sysInActivity(act):
	if act=='lock screen':
		os.system('rundll32.exe user32.dll,LockWorkStation')
	elif act=='shutdown':
		os.system('shutdown /s')
	elif act=='hibernate':
		os.system('shutdown /h')
	elif act=='restart':
		os.system('shutdown /r')
	else:
		return 'Sorry! I cannot do that.'

def switchOn(toggle):
	if toggle=='night light':
		sleep(1.5)
		pg.press('winleft')
		sleep(0.5)
		pg.typewrite('brightness')
		sleep(0.5)
		pg.press('enter')
		sleep(3)
		pg.press('tab')
		sleep(1)
		pg.press('space')
		sleep(1)
		pg.click(1900,5)
		return None
	elif toggle=='Wi-Fi':
		pg.moveTo(1620,1054,1,pg.easeOutQuad)
		pg.click()
		pg.moveTo(1525,983,1,pg.easeOutQuad)
		pg.click()
		return None
	elif toggle=='hotspot' or toggle=='mobile hotspot':
		pg.moveTo(1620,1054,1,pg.easeOutQuad)
		pg.click()
		pg.moveTo(1735,986,1,pg.easeOutQuad)
		pg.click()
		return None
	elif toggle=='airplane mode':
		pg.moveTo(1620,1054,1,pg.easeOutQuad)
		pg.click()
		pg.moveTo(1632,979,1,pg.easeOutQuad)
		pg.click()
		return None
	elif toggle=='battery saver':
		pg.moveTo(1650,1053,1,pg.easeOutQuad)
		pg.click()
		sleep(0.5)
		global flg
		if flg:
			pg.moveTo(1458,867,1,pg.easeOutQuad)
			flg=False
		else:
			pg.moveTo(1582,867,1,pg.easeOutQuad)
			flg=True
		sleep(0.5)
		pg.click()
		pg.click(1237,1059)
		return None
	else:
		return 'Sorry! I cannot do that.'

def browser(site):
	url='https://'+site
	webbrowser.get('windows-default').open(url)

# def showDesktop():
# 	pg.moveTo(screenWidth-1,screenHeight-1)
# 	sleep(0.75)
# 	pg.click()

