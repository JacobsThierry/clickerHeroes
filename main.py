from pynput import keyboard, mouse
import PIL
from PIL import ImageGrab
import time
import random

_latestScreen = -1

screenRate = 5
def getScreen():
	global _screenshot
	global _latestScreen

	if(_latestScreen == -1 or time.time() - _latestScreen > screenRate ):
		_screenshot = ImageGrab.grab()
	
	return _screenshot


def waitOnPress(key):
	 pass



def waitOnRelease(key):
	try:
		if key == keyboard.Key.space:
			return False
		else:
			print("foo")
	except:
		 pass
		  


def spamClickOnPress(key):
	pass

def spamClickOnRelease(key):
	try:
		if key == keyboard.Key.space:
			global stopSpam
			stopSpam = True
			return False
		else:
			print("foo")
	except:
		 pass




mobLocation = (1458, 650)
clickPerSec = 50
def spamClick(timer: int):
	
	global stopSpam
	m = mouse.Controller()
	oldPos = m.position
	m.position = mobLocation
	starttime = time.time()

	while((starttime + timer) > time.time() and not stopSpam ):
		m.position = (mobLocation[0], mobLocation[1])
		m.press(mouse.Button.left)
		m.release(mouse.Button.left)
		time.sleep(1/clickPerSec)
	m.position = oldPos


import math
def collectGold():
	m = mouse.Controller()
	for collectionRadius in range(30, 150, 30):
		m.position = mobLocation
		m.position = mobLocation[0] + collectionRadius, mobLocation[1]
		for i in range(0, 360, 30):
			if stopSpam:
				return
			if i%6==0:
				m.position = (mobLocation[0]+collectionRadius*math.cos(math.radians(i)),mobLocation[1]+collectionRadius*math.sin(math.radians(i)))
				spamClick(0.1)


def wait():
	with keyboard.Listener(
			on_press=waitOnPress,
			on_release=waitOnRelease) as listener:
		listener.join()
		


nextLevelLocation = (1542, 75)
def nextLevel():
	m = mouse.Controller()
	m.position = nextLevelLocation
	m.press(mouse.Button.left)
	m.release(mouse.Button.left)
	

previousLevelLocation = (1329, 72)
def previousLevel():
	m = mouse.Controller()
	m.position = previousLevelLocation
	m.press(mouse.Button.left)
	m.release(mouse.Button.left)

spellLocation = (1023, 288)
spellIncrement = (0, 376 - 288)
def useSpell():
	m = mouse.Controller()
	for i in range(9):
		m.position = (spellLocation[0] + spellIncrement[0] * i, spellLocation[1] + spellIncrement[1] * i)
		m.press(mouse.Button.left)
		m.release(mouse.Button.left)
		time.sleep(0.01)


def changeLevel(diff : int):
	if int < 0:
		func = previousLevel
	else:
		func = nextLevel
	i = abs(i)
	while(i > 0):
		func()
		time.sleep(0.1)




#mainLoop
def loop():
	listener = keyboard.Listener(on_press=spamClickOnPress, on_release=spamClickOnRelease)
	listener.start()
	global stopSpam
	stopSpam = False
	k = keyboard.Controller()
	while(not stopSpam):
		
		spamClick(60)
		collectGold()
		useSpell()
		buyUpgrade()


		level = print("Level = ", getLevel(), " hp des ennemies = ", f"{getMonsterHp(getLevel()):e}" )

		try:
			print("DPS = ", f"{getDps():e}" )
			print("hp des monstres au prochain niveau :", f"{getMonsterHp(getLevel() + 1):e}" )
			
			if(getDps() * 20 > getMonsterHp(getLevel() + 1) or getLevel() < 10 ):
				nextLevel()
				print("On passe au niveau suivant")
			elif(getDps() * 20 < getMonsterHp(getLevel())):
				previousLevel()
				print("On revient au niveau précédent")
		except:
			pass



# Fonction pour calculer la distance Euclidienne entre deux couleurs
def distance(c1, c2):
	return ((c1[0]-c2[0])**2 + (c1[1]-c2[1])**2 + (c1[2]-c2[2])**2) ** 0.5


import colour
hpPixelLocation = (1336, 933)
#hpPixelLocation = (436, 574)

#retourne un nombre en 0 et 1 correspondant a la valeur approximative des hp de l'ennemie obtenu grace a la couleur des pv
def getEnnemyHpPercent():
	screenshot = getScreen()
	screenshot = screenshot.convert("RGB")
	hpColor = screenshot.getpixel(hpPixelLocation)

	maxHp = colour.Color("#48bf00")
	midHp = colour.Color("#f56500")

	minHp = colour.Color("#ff0000")
	gray = colour.Color("#413f3f")

	if(hpColor == gray):
		return 0
	
	
	gradient = [gray] + list(minHp.range_to(midHp,50)) + list(midHp.range_to(maxHp,50))
	
	# Trouver la couleur la plus proche de la couleur de référence 
	closest_color = min(gradient, key=lambda c: distance(tuple( 255 * elem for elem in c.rgb ) , hpColor))
	position = gradient.index(closest_color)
	return position

import pytesseract


#Convertion de selection gimp vers des bbox
def selectionToBbox(location, size):
	return (location[0], location[1], location[0] + size[0], location[1] + size[1])


levelTextLocation = (1107, 139)
levelTextSize = (679, 50)
levelTextBox = selectionToBbox(levelTextLocation, levelTextSize)

import re


def getLevel():

	global _lastLevel

	try: _lastLevel
	except: _lastLevel = 1

	screenshot = np.array(getScreen().crop(levelTextBox).convert("RGB"))
	screenshot = dpsImageProcessing(screenshot)
	
	#je pourrais process la screen plus tard pour avoir de meilleurs résultats
	text = pytesseract.image_to_string(screenshot)
	text = text.strip()
	text = text.lower()

	
	
	try:
		l = int(re.sub(r"[^0-9]", "", text))
		_lastLevel = l
		return l
	except:
		return _lastLevel

scrollUp = (927, 321)
scrollDown = (927, 1053)
resetScroll = (927, 380)
scrollOneDown = 2

initPosition = [ (160,428), (160,610), (160,790), (160, 970), ] #on fait les 4 premiers personnages a part
downPos = (160, 1031)

upgradepos = 320 #position x de la 1e upgrade
upgradeposincr = 60
upgradeCount = 7
def buyUpgrade():

	if stopSpam:
		return

	m = mouse.Controller()
	#reset du scroll
	m.position = resetScroll
	m.press(mouse.Button.left)
	time.sleep(0.3)
	m.release(mouse.Button.left)
	time.sleep(0.1)

	
	for h in initPosition:
		if stopSpam:
			return
		for i in range(upgradeCount):#on achète les upgrades
			time.sleep(0.01)
			m.position = (upgradepos + upgradeposincr * i, h[1])
			time.sleep(0.01)
			m.press(mouse.Button.left)
			m.release(mouse.Button.left)

		#Le scroll inconsistant fait que les premiers heros ne sont que peu achetés : on les spam
		for k in range(5):
			time.sleep(0.01)
			m.position = h
			
			for g in range(10):
				m.press(mouse.Button.left)
				m.release(mouse.Button.left)
				time.sleep(0.01)

		
	#On fait en sorte que le prochain hero soit en bas de la liste
	for i in range(4):
		time.sleep(0.01)
		m.position = scrollDown
		time.sleep(0.01)
		m.press(mouse.Button.left)
		m.release(mouse.Button.left)
	
	for i in range(20):
		if stopSpam:
			return

		for j in range(upgradeCount):#on achète les upgrades
			time.sleep(0.01)
			m.position = (upgradepos + upgradeposincr * j, downPos[1])
			m.press(mouse.Button.left)
			m.release(mouse.Button.left)

		time.sleep(0.01)
		m.position = downPos
		time.sleep(0.01)
		for g in range(10):
			m.press(mouse.Button.left)
			m.release(mouse.Button.left)
			time.sleep(0.01)
		

		#J'ai l'impression d'avoir des inconsistances avec le scroll. Je crois que ça scroll un % du total, ce qui pose problème avec le nombre de héro qui augmente. Donc je vais scroll trop de fois pour ne rien rater
		for j in range(scrollOneDown ):
			time.sleep(0.01)
			m.position = scrollDown
			time.sleep(0.01)
			m.press(mouse.Button.left)
			m.release(mouse.Button.left)
		
		screenshot = ImageGrab.grab()
		screenshot = screenshot.convert("RGB")
		#on regarde la scroll bar pour voir si on est en bas ou pas
		pickedColor = screenshot.getpixel( (925, 1028))
		
		#print( tuple( 255 * elem for elem in colour.Color("#ffdc2b").rgb ))

		dist = distance(pickedColor, tuple( 255 * elem for elem in colour.Color("#ffdc2b").rgb ) )
		#print("dist = ", dist)
		if(dist < 50):
			return



import cv2 as cv
import numpy as np


def dpsImageProcessing(screenshot):
	
	screenshot = cv.GaussianBlur(screenshot, (1, 1), 0)
	screenshot = cv.cvtColor(screenshot, cv.COLOR_RGB2GRAY)
	th, screenshot = cv.threshold(screenshot,250,255,cv.THRESH_BINARY)
	kernel = np.ones((1,1),np.uint8)
	screenshot = cv.morphologyEx(screenshot, cv.MORPH_OPEN, kernel)

	screenshot = PIL.Image.fromarray(np.uint8(screenshot))
	return screenshot

dpsTextLocation = (33, 220)
dpsTextSize = (500, 32)
dpsTextBox = selectionToBbox(dpsTextLocation, dpsTextSize)

clickDamageLocation = (30, 250)
clickDamageSize = (548, 38)
clickDamageBox = selectionToBbox(clickDamageLocation, clickDamageSize)
def getDps():

	global _oldDps

	try: _oldDps
	except: _oldDps = 0

	screenshotDps = np.array(getScreen().crop(dpsTextBox))
	screenshotDps = dpsImageProcessing(screenshotDps)
	textDps = pytesseract.image_to_string(screenshotDps)
	
	textDps = textDps.strip().lower()
	
	textDps = textDps.replace("dps", "")
	
	textDps = textDps.strip().lower()
	textDps = textDps.replace(",", "")

	screenshotClick = np.array(getScreen().crop(clickDamageBox))
	screenshotClick = dpsImageProcessing(screenshotClick)
	textClick = pytesseract.image_to_string(screenshotClick)
	textClick = textClick.strip().lower()
	textClick = textClick.replace("click", "").replace("damage", "")

	
	try:
		dps = float(textDps) + float(textClick) * clickPerSec
		if dps == 0:
			dps = _oldDps
		else:
			_oldDps = dps
	except:
		dps = _oldDps
	return dps


def getMonsterHp(level : int):
	isboss = 10 if level%5 == 0 else 1
	if level < 140:
		return math.ceil(10 * (level - 1 + 1.55**(level - 1)) * isboss)
	if level < 500:
		return math.ceil( 10 * (139 + 1.55**(139) * 1.145**(level - 140) * isboss) )
	
	return math.ceil( 1.545**(level-200001) * 1.240 * 10**(25409) + (level-1) *10 )

##ça marche po :(((
shopLocation = (5,290)
shopSize = (880, 786)
shopBox = selectionToBbox(shopLocation, shopSize)
def shopReader():
	screenshot = getScreen()
	cropped = np.array(screenshot.crop(shopBox))
	ret, thresh = cv.threshold(cv.cvtColor(cropped, cv.COLOR_RGB2GRAY) ,120,210,cv.THRESH_BINARY)
	contours, _ = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
	
	img = cropped

	for cnt in contours:
		x1,y1 = cnt[0][0]
		approx = cv.approxPolyDP(cnt, 0.01*cv.arcLength(cnt, True), True)
		if len(approx) == 4:
			x, y, w, h = cv.boundingRect(cnt)
			ratio = float(w)/h
			if ratio >= 0.9 and ratio <= 1.1:
				img = cv.drawContours(img, [cnt], -1, (0,255,255), 3)
				cv.putText(img, 'Square', (x1, y1), cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
			else:
				cv.putText(img, 'Rectangle', (x1, y1), cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
			img = cv.drawContours(img, [cnt], -1, (0,255,0), 3)
	cv.imshow("Shapes", img)
	cv.waitKey(0)
	cv.destroyAllWindows()

pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
wait()

loop()

#shopReader()

#buyUpgrade()
#print(f"{getDps():e}")
#print(getLevel())
#useSpell()