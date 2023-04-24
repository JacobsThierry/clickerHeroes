from pynput import keyboard, mouse
import PIL
from PIL import ImageGrab
import time
import random

_latestScreen = -1

screenRate = 5
def getScreen(force=False):
	global _screenshot
	global _latestScreen

	if(force or _latestScreen == -1 or time.time() - _latestScreen > screenRate ):
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
clickPerSec = 39 #La limite en jeu devrait être 40
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
		
		#On reste dans chaque niveau le temps de tuer 12 ennemies : ça permet de monter plus vite dans les niveaux.
		#Je met 12 car je ne connais pas le temps de respawn des ennemies.
		timePerTick = 60 if getDps() == 0 else max(30,min(60,(getMonsterHp(getLevel()) * 12)/getDps()))

		print("time per tick =", timePerTick)

		spamClick(timePerTick)
		time.sleep(0.2)
		collectGold()
		time.sleep(0.1)
		useSpell()
		time.sleep(0.1)
		buyUpgrade()


		level = print("Level = ", getLevel(), " hp des ennemies = ", f"{getMonsterHp(getLevel()):e}" )

		try:
			screenshot = getScreen()
			#on regarde la couleur du gift
			pickedColor = screenshot.getpixel( (1798, 887))
			dist = distance(pickedColor, tuple( 255 * elem for elem in colour.Color("#e93351").rgb ) )

			if dist < 50:
				openGift()
		except:
			pass

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
	screenshot = imageProcessing(screenshot)
	
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

	m = mouse.Controller()
	#reset du scroll
	m.position = resetScroll
	m.press(mouse.Button.left)
	time.sleep(0.3)
	m.release(mouse.Button.left)
	time.sleep(0.1)



	proceeded = []


	for i in range(35):

		try:
			if stopSpam:
				return
		except: pass

		screenshot = getScreen(force=True)
		screenshot = screenshot.convert("RGB")
		heroes = shopReader()
		for hero in heroes:
			if hero not in proceeded:
				print(hero.name)
				hero.buyUpgrades()


				for k in range(10 if hero.lvl < 11 else 1 ):
					hero.lvlUpHero()
				proceeded.append(hero)



		#on regarde la scroll bar pour voir si on est en bas ou pas
		pickedColor = screenshot.getpixel( (925, 1028))
			
		#print( tuple( 255 * elem for elem in colour.Color("#ffdc2b").rgb ))

		dist = distance(pickedColor, tuple( 255 * elem for elem in colour.Color("#ffdc2b").rgb ) )

		if(dist < 50):
			return
		
		for j in range(4):
			m.position = scrollDown
			time.sleep(0.03)
			m.press(mouse.Button.left)
			m.release(mouse.Button.left)
		time.sleep(1) #On attend la fin de l'annimation


import cv2 as cv
import numpy as np


def imageProcessing(screenshot):
	
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
	screenshotDps = imageProcessing(screenshotDps)
	textDps = pytesseract.image_to_string(screenshotDps)
	
	textDps = textDps.strip().lower()
	
	textDps = textDps[0: textDps.index("dps") ]
	
	textDps = textDps.strip().lower()
	textDps = textDps.replace(",", "")

	screenshotClick = np.array(getScreen().crop(clickDamageBox))
	screenshotClick = imageProcessing(screenshotClick)
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

	hp = 0
	global _monsterHp

	try: _monsterHp
	except: _monsterHp = 0

	try:
		isboss = 10 if level%5 == 0 else 1
		if level < 141:
			hp = math.ceil(10 * (level - 1 + int(1.55**(level - 1))) * isboss)
		elif level < 500:
			hp = math.ceil( 10 * (139 + (155**(139))//100 * (1145**(level - 140))//1000 * isboss) )
		else:
			hp = math.ceil( (1545**(level-200001))//1000 * (1240 * 10**(25409))//1000 + (level-1) * 10 )
		_monsterHp = hp
		return hp
	except:
		return _monsterHp


# from https://pyimagesearch.com/2015/02/16/faster-non-maximum-suppression-python/
def non_max_suppression(boxes, overlapThresh):
	# if there are no boxes, return an empty list
	if len(boxes) == 0:
		return []
	# if the bounding boxes integers, convert them to floats --
	# this is important since we'll be doing a bunch of divisions
	if boxes.dtype.kind == "i":
		boxes = boxes.astype("float")
	# initialize the list of picked indexes	
	pick = []
	# grab the coordinates of the bounding boxes
	x1 = boxes[:,0]
	y1 = boxes[:,1]
	x2 = boxes[:,2]
	y2 = boxes[:,3]
	# compute the area of the bounding boxes and sort the bounding
	# boxes by the bottom-right y-coordinate of the bounding box
	area = (x2 - x1 + 1) * (y2 - y1 + 1)
	idxs = np.argsort(y2)
	# keep looping while some indexes still remain in the indexes
	# list
	while len(idxs) > 0:
		# grab the last index in the indexes list and add the
		# index value to the list of picked indexes
		last = len(idxs) - 1
		i = idxs[last]
		pick.append(i)
		# find the largest (x, y) coordinates for the start of
		# the bounding box and the smallest (x, y) coordinates
		# for the end of the bounding box
		xx1 = np.maximum(x1[i], x1[idxs[:last]])
		yy1 = np.maximum(y1[i], y1[idxs[:last]])
		xx2 = np.minimum(x2[i], x2[idxs[:last]])
		yy2 = np.minimum(y2[i], y2[idxs[:last]])
		# compute the width and height of the bounding box
		w = np.maximum(0, xx2 - xx1 + 1)
		h = np.maximum(0, yy2 - yy1 + 1)
		# compute the ratio of overlap
		overlap = (w * h) / area[idxs[:last]]
		# delete all indexes from the index list that have
		idxs = np.delete(idxs, np.concatenate(([last],
			np.where(overlap > overlapThresh)[0])))
	# return only the bounding boxes that were picked using the
	# integer data type
	return boxes[pick].astype("int")


shopLocation = (5,290)
shopSize = (880, 786)
shopBox = selectionToBbox(shopLocation, shopSize)

cardUpgradeInitPos = (313, 132)
cardUpgradePosIncr = 60
levelUpButton = (130, 100)
class heroCard:
	def __init__(self, name, lvl, cardX, cardY):
		self.name = name
		self.lvl = lvl
		self.cardX = cardX
		self.cardY = cardY
	
	def __eq__(self, o):
		if isinstance(o, heroCard):
			return self.name == o.name
		return False
	
	def buyUpgrades(self):
		m = mouse.Controller()
		for i in range(3 if self.name.lower().strip == "amenhotep" else 7):
			m.position = (self.cardX + cardUpgradeInitPos[0] + cardUpgradePosIncr * i, self.cardY + cardUpgradeInitPos[1] )
			m.press(mouse.Button.left)
			m.release(mouse.Button.left)
			time.sleep(0.05)
	
	
	def lvlUpHero(self):
		m = mouse.Controller()
		m.position = (self.cardX + levelUpButton[0], self.cardY + levelUpButton[1])
		m.press(mouse.Button.left)
		m.release(mouse.Button.left)
		time.sleep(0.05)

import os

#return an array with the heroes that can be seen in the shop
def shopReader() -> list[heroCard]:
	screenshot = getScreen().convert("RGB")
	cropped = np.array(screenshot.crop(shopBox))
	cropped = cropped[:, :, ::-1].copy() 
	cropped2 = cv.cvtColor(cropped, cv.COLOR_RGB2GRAY)
	template = cv.imread("pattern1.png", cv.IMREAD_GRAYSCALE)
	w, h = template.shape[::-1]

	res = cv.matchTemplate(cropped2,template,cv.TM_CCOEFF_NORMED)

	(yCoords, xCoords) = np.where(res >= 0.3)
	

	rects = []
	# loop over the starting (x, y)-coordinates again
	for (x, y) in zip(xCoords, yCoords):
		# update our list of rectangles
		rects.append((x, y, x + w, y + h))

	# apply non-maxima suppression to the rectangles
	pick = non_max_suppression(np.array(rects), 0.2)
	
	heroes = []
	for (startX, startY, endX, endY) in pick:
		card = cropped[startY : endY, startX : endX  ]

		heroes.append(heroCard(getHeroName(card), getHeroLevel(card), startX + shopLocation[0], startY + shopLocation[1] ))
		#cv.imwrite(os.path.join("C:\\Users\\thier\\Desktop\\clicker heroes",heroes[-1].name + ".png" ), card )

	return heroes
		


nameLocation = (251, 12)
nameSize = (488, 40)
nameBox = selectionToBbox(nameLocation, nameSize)
def getHeroName(card):
	nameCropped = cv2CropBBox(card, nameBox)
	nameCropped = imageProcessing(nameCropped)
	text = pytesseract.image_to_string(nameCropped).strip().lower()
	return text

heroLevelLocation = (398, 55)
heroLevelSize = (327, 35)
heroLevelBox = selectionToBbox(heroLevelLocation, heroLevelSize)
def getHeroLevel(card):
	levelCropped = cv2CropBBox(card, heroLevelBox)
	levelCropped = imageProcessing(levelCropped)
	#cv.imshow("eye", np.array(levelCropped))
	#cv.waitKey(0)
	
	text = pytesseract.image_to_string(levelCropped).strip().lower().replace("lvl", "").replace("lv!", "").strip()
	try:
		return int(text)
	except:
		return -1


def cv2CropBBox(img, bbox):
	return img[bbox[1] : bbox[3], bbox[0] : bbox[2] ]



def openGift():
	m = mouse.Controller()
	m.position = (1838, 918)
	m.press(mouse.Button.left)
	m.release(mouse.Button.left)
	time.sleep(1.5)
	m.position = (948, 557)
	m.press(mouse.Button.left)
	m.release(mouse.Button.left)
	time.sleep(1.5)
	m.position = (1553, 170)




pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
wait()

#loop()
openGift()

#buyUpgrade()
#buyUpgrade()

#openGift()

#buyUpgrade()

#shopReader()

#buyUpgrade()
#print(f"{getDps():e}")
#print(getLevel())
#useSpell()