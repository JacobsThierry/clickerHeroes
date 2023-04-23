from pynput import keyboard, mouse
import time
import random


def wait_on_press(key):
	 pass

def wait_on_release(key):
	try:
		if key == keyboard.Key.space:
			return False
		else:
			print("foo")
	except:
		 pass
		  

def spamClick_on_press(key):
   pass

def spamClick_on_release(key):
	try:
		if key == keyboard.Key.space:
			global stopSpam
			stopSpam = True
			return False
		else:
			print("foo")
	except:
		 pass

def spamClick(timer: int):
	global stopSpam
	stopSpam = False
	listener = keyboard.Listener(on_press=spamClick_on_press, on_release=spamClick_on_release)
	listener.start()
	m = mouse.Controller()
	m.position = (1458, 650)
	starttime = time.time()
	while((starttime + timer) > time.time() and not stopSpam ):
		
		m.position = (1458 + random.randint(-100, 100), 650 + random.randint(-100, 100))
		m.press(mouse.Button.left)
		m.release(mouse.Button.left)
		time.sleep(0.01)
		

def wait():
	with keyboard.Listener(
			on_press=wait_on_press,
			on_release=wait_on_release) as listener:
		listener.join()
		



#mainLoop
def loop():
	k = keyboard.Controller()
	while(True):
		pass
		
		
		
def loop():
	pass

wait()
spamClick(10)