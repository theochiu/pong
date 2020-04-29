
import time, sys
from random import randint

# constants
HEIGHT = 30
WIDTH = 120
CSI = "\033["
# CSI = "\e["
TESTING = True

global isWindows

isWindows = False
try:
	from win32api import STD_INPUT_HANDLE
	from win32console import GetStdHandle, KEY_EVENT, ENABLE_ECHO_INPUT, ENABLE_LINE_INPUT, ENABLE_PROCESSED_INPUT
	isWindows = True
except ImportError as e:
	import sys
	import select
	import termios


class KeyPoller():
	def __enter__(self):
		global isWindows
		if isWindows:
			self.readHandle = GetStdHandle(STD_INPUT_HANDLE)
			self.readHandle.SetConsoleMode(ENABLE_LINE_INPUT|ENABLE_ECHO_INPUT|ENABLE_PROCESSED_INPUT)

			self.curEventLength = 0
			self.curKeysLength = 0

			self.capturedChars = []
		else:
			# Save the terminal settings
			self.fd = sys.stdin.fileno()
			self.new_term = termios.tcgetattr(self.fd)
			self.old_term = termios.tcgetattr(self.fd)

			# New terminal setting unbuffered
			self.new_term[3] = (self.new_term[3] & ~termios.ICANON & ~termios.ECHO)
			termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.new_term)

		return self

	def __exit__(self, type, value, traceback):
		if isWindows:
			pass
		else:
			termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.old_term)

	def poll(self):
		if isWindows:
			if not len(self.capturedChars) == 0:
				return self.capturedChars.pop(0)

			eventsPeek = self.readHandle.PeekConsoleInput(10000)

			if len(eventsPeek) == 0:
				return None

			if not len(eventsPeek) == self.curEventLength:
				for curEvent in eventsPeek[self.curEventLength:]:
					if curEvent.EventType == KEY_EVENT:
						if ord(curEvent.Char) == 0 or not curEvent.KeyDown:
							pass
						else:
							curChar = str(curEvent.Char)
							self.capturedChars.append(curChar)
				self.curEventLength = len(eventsPeek)

			if not len(self.capturedChars) == 0:
				return self.capturedChars.pop(0)
			else:
				return None
		else:
			dr,dw,de = select.select([sys.stdin], [], [], 0)
			if not dr == []:
				return sys.stdin.read(1)
			return None

# END STACKOVEFLOW

def test_key2():
	with KeyPoller() as keyPoller:
		while True:
			c = keyPoller.poll()

			if c:
				setpos(0,6)
				sys.stdout.write(str(c))

			else:	
				setpos(0, 5)
				sys.stdout.write(str(c))

			if c and ord(c) == 3: 
				print("ctrl-c")
				quit()

			# time.sleep(1)

			# if not c is None:
			# 	if c == "c":
			# 		break
			# print(c)

def getchar():
	# Returns a single character from standard input
	import os
	ch = ''
	if os.name == 'nt': # how it works on windows
		import msvcrt
		ch = msvcrt.getch()
	else:
		import tty, termios, sys
		fd = sys.stdin.fileno()
		old_settings = termios.tcgetattr(fd)
		# try:
		tty.setraw(sys.stdin.fileno())
		ch = sys.stdin.read(1)
		# finally:
		# termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
	if ord(ch) == 3: quit() # handle ctrl+C
	return ch


def setpos(x, y):
	'''set cursor position'''
	# putstr(CSI); putint(y+1); putstr(";"); putint(x+1); putstr("H");
	sys.stdout.write(CSI + str(y+1) + ";" + str(x+1) + "H")

def fgbg(n):
	''' Set the foreground and background colors with an 8-bit value '''
	f = (n>>4) & 0xf;
	b = (n>>0) & 0xf;
	if (f < 8):
		f += 30;
	else:
		f += 90 - 8;

	if (b < 8):
		b += 40;
	else:
		b += 100 - 8;

	# putstr(CSI); putint(f); putstr(";"); putint(b); putstr("m");
	sys.stdout.write(CSI + str(f) + ";" + str(b) + "m")

def test_paint():
	''' test printing to the screen '''
	for y in range(HEIGHT):
		setpos(0,y)
		for x in range(WIDTH):
			fgbg(((x%16)<<4) + (y%16));
			sys.stdout.write(chr(ord("A") + (x%26)))

	# character input and paintbrush movement 
	x = 0
	y = 0
	while 1:
		c = getchar()
		if c == "w" and y > 0:
			y -= 1 
		elif c == "a" and x > 0:
			x -= 1
		elif c == "s" and y < HEIGHT - 1:
			y += 1 
		elif c == "d" and x < WIDTH - 1:
			x += 1

		setpos(x, y)
		fgbg(0x0f)
		sys.stdout.write(' ')
		sys.stdout.flush()
			

def test_2():
	for i in range(0, 16):
		for j in range(0, 16):
			code = str(i * 16 + j)
			sys.stdout.write(u"\u001b[38;5;" + code + "m " + code.ljust(4))
		print("\u001b[0m")


def test3():
	sys.stdout.write("\\033[XXm")

	for i in range(30,37+1):
		sys.stdout.write(("\033[%dm%d\t\t\033[%dm%d" % (i,i,i+60,i+60)))

	sys.stdout.write("\033[39m\\033[39m - Reset colour")
	sys.stdout.write("\\033[2K - Clear Line")
	sys.stdout.write("\\033[<L>;<C>H OR \\033[<L>;<C>f puts the cursor at line L and column C.")
	sys.stdout.write("\\033[<N>A Move the cursor up N lines")
	sys.stdout.write("\\033[<N>B Move the cursor down N lines")
	sys.stdout.write("\\033[<N>C Move the cursor forward N columns")
	sys.stdout.write("\\033[<N>D Move the cursor backward N columns")
	sys.stdout.write("\\033[2J Clear the screen, move to (0,0)")
	sys.stdout.write("\\033[K Erase to end of line")
	sys.stdout.write("\\033[s Save cursor position")
	sys.stdout.write("\\033[u Restore cursor position")
	sys.stdout.write(" ")
	sys.stdout.write("\\033[4m  Underline on")
	sys.stdout.write("\\033[24m Underline off")
	sys.stdout.write("\\033[1m  Bold on")
	sys.stdout.write("\\033[21m Bold off")

def test_getchar():
	while 1:
		ch = getchar()
		print ('You pressed %c (%i)' % (ch, ord(ch)))


def draw_white(x, y):
	draw_color(x, y, 0x0f)

def draw_black(x, y):
	draw_color(x, y, 0x00)

def draw_blue(x, y):
	draw_color(x, y, 4)

def draw_color(x, y, color):
	setpos(x, y)
	fgbg(color)
	sys.stdout.write(' ')
	sys.stdout.flush()

def draw_score(side, num):

	num %= 10
	center_y = 6
	# left scoreboard
	if side == 0:	
		center_x = int(WIDTH * 3 / 8)

	# right scoreboard
	elif side == 1:
		center_x = int(WIDTH * 5 / 8)

	x = center_x
	y = center_y

	# blackout score area
	draw_black(x-1, y-2)
	draw_black(x-1, y-1)
	draw_black(x-1, y)
	draw_black(x-1, y+1)
	draw_black(x-1, y+2)

	draw_black(x, y-2)
	draw_black(x, y-1)
	draw_black(x, y)
	draw_black(x, y+1)
	draw_black(x, y+2)

	draw_black(x+1, y-2)
	draw_black(x+1, y-1)
	draw_black(x+1, y)
	draw_black(x+1, y+1)
	draw_black(x+1, y+2)

	draw_black(x+2, y-2)
	draw_black(x+2, y-1)
	draw_black(x+2, y)
	draw_black(x+2, y+1)
	draw_black(x+2, y+2)

	# digit zero
	if num == 0:


		# left bar
		draw_white(x-1,y-2)
		draw_white(x-1,y-1)
		draw_white(x-1,y)
		draw_white(x-1,y+1)
		draw_white(x-1,y+2)
		
		# right bar
		draw_white(x+2,y-2)
		draw_white(x+2,y-1)
		draw_white(x+2,y)
		draw_white(x+2,y+1)
		draw_white(x+2,y+2)

		# missing chunks
		draw_white(x, y-2)
		draw_white(x, y+2)
		draw_white(x+1, y-2)
		draw_white(x+1, y+2)

	# digit 1 
	elif num == 1:
		# middle bar
		draw_white(x,y-2)
		draw_white(x,y-1)
		draw_white(x,y)
		draw_white(x,y+1)
		draw_white(x,y+2)

	elif num == 2:
		# top bar
		draw_white(x, y-2)
		draw_white(x+1, y-2)
		draw_white(x+2, y-2)

		# middle bar
		draw_white(x, y)
		draw_white(x+1, y)
		draw_white(x+2, y)

		# bottom bar
		draw_white(x, y+2)
		draw_white(x+1, y+2)
		draw_white(x+2, y+2)

		# missing chunks
		draw_white(x+2, y-1)
		draw_white(x, y+1)

	elif num == 3:
		# top bar
		draw_white(x, y-2)
		draw_white(x+1, y-2)
		draw_white(x+2, y-2)

		# middle bar
		draw_white(x, y)
		draw_white(x+1, y)
		draw_white(x+2, y)

		# bottom bar
		draw_white(x, y+2)
		draw_white(x+1, y+2)
		draw_white(x+2, y+2)

		# missing chunks
		draw_white(x+2, y-1)
		draw_white(x+2, y+1)

	elif num == 4:

		# middle bar
		draw_white(x-1, y)
		draw_white(x, y)
		draw_white(x+1, y)
		draw_white(x+2, y)

		# right bar
		draw_white(x+2,y-2)
		draw_white(x+2,y-1)
		draw_white(x+2,y)
		draw_white(x+2,y+1)
		draw_white(x+2,y+2)

		# missing chunks
		draw_white(x-1, y-1)
		draw_white(x-1, y-2)

	elif num == 5:
		# top bar
		draw_white(x, y-2)
		draw_white(x+1, y-2)
		draw_white(x+2, y-2)

		# middle bar
		draw_white(x, y)
		draw_white(x+1, y)
		draw_white(x+2, y)

		# bottom bar
		draw_white(x, y+2)
		draw_white(x+1, y+2)
		draw_white(x+2, y+2)

		# missing chunks
		draw_white(x, y-1)
		draw_white(x+2, y+1)

	elif num == 6:

		# top bar
		draw_white(x, y-2)
		draw_white(x+1, y-2)
		draw_white(x+2, y-2)

		# left bar
		draw_white(x,y-2)
		draw_white(x,y-1)
		draw_white(x,y)
		draw_white(x,y+1)
		draw_white(x,y+2)

		# right bar
		draw_white(x+2, y)
		draw_white(x+2, y+1)
		draw_white(x+2, y+2)

		# missing chunks
		draw_white(x+1, y)
		draw_white(x+1, y+2)

	elif num == 7:

		# right bar
		draw_white(x+2,y-2)
		draw_white(x+2,y-1)
		draw_white(x+2,y)
		draw_white(x+2,y+1)
		draw_white(x+2,y+2)

		# missing chunks
		draw_white(x-1, y-2)
		draw_white(x, y-2)
		draw_white(x+1, y-2)

	elif num == 8:

		# left bar
		draw_white(x-1,y-2)
		draw_white(x-1,y-1)
		draw_white(x-1,y)
		draw_white(x-1,y+1)
		draw_white(x-1,y+2)
		
		# right bar
		draw_white(x+2,y-2)
		draw_white(x+2,y-1)
		draw_white(x+2,y)
		draw_white(x+2,y+1)
		draw_white(x+2,y+2)

		# missing chunks (zero)
		draw_white(x, y-2)
		draw_white(x, y+2)
		draw_white(x+1, y-2)
		draw_white(x+1, y+2)

		# missing chunks (eight)
		draw_white(x,y)
		draw_white(x+1, y)


	elif num == 9:

		# middle bar
		draw_white(x-1, y)
		draw_white(x, y)
		draw_white(x+1, y)
		draw_white(x+2, y)

		# right bar
		draw_white(x+2,y-2)
		draw_white(x+2,y-1)
		draw_white(x+2,y)
		draw_white(x+2,y+1)
		draw_white(x+2,y+2)

		# missing chunks
		draw_white(x-1, y-1)
		draw_white(x-1, y-2)
		draw_white(x, y-2)
		draw_white(x+1, y-2)


# defines the CENTER of the paddle

LEFT_PADDLE_Y = HEIGHT // 2
RIGHT_PADDLE_Y = HEIGHT // 2

def draw_paddles():
	# draw left paddle

	if TESTING:
		for y in range(HEIGHT):
			draw_white(0, y)

	y = LEFT_PADDLE_Y
	draw_white(0, y-2)
	draw_white(0, y-1)
	draw_white(0, y)
	draw_white(0, y+1)
	draw_white(0, y+2)

	y = RIGHT_PADDLE_Y
	draw_white(WIDTH - 1, y-2)
	draw_white(WIDTH - 1, y-1)
	draw_white(WIDTH - 1, y)
	draw_white(WIDTH - 1, y+1)
	draw_white(WIDTH - 1, y+2)

left_score = 0
right_score = 0

def blackout():
	fgbg(0)					# color black
	for y in range(HEIGHT):
		setpos(0,y)
		for x in range(WIDTH):
			sys.stdout.write(" ")

def init_pong():
	''' initialize the screen for the game'''
	
	# draw dotted line (middle)
	x = WIDTH // 2
	for y in range(HEIGHT):
		if y % 3 != 1 : 				# every third
			setpos(x, y)
			fgbg(0)
			sys.stdout.write(' ')
			sys.stdout.flush()
		else:
			setpos(x, y)
			fgbg(0x0f)
			sys.stdout.write(' ')
			sys.stdout.flush()

	# draw paddles (check testing)
	draw_paddles()

	# draw score (zeroes)
	draw_score(0, left_score)
	draw_score(1, right_score)

	# init ball
	# init_ball("LEFT")

BALL_X = 0
BALL_Y = 0
DX = -1 * randint(1,3)			# random integer from 0-3 INCLUSIVE (initialize moving left)
DY = randint(0,3)



def init_ball(side):
	global BALL_X 
	global BALL_Y

	# SET SPAWN LOCATION
	x = WIDTH // 2
	y = HEIGHT // 2 - 5

	if side == "LEFT":
		x -= 5 
	else:
		x += 5

	BALL_X = x
	BALL_Y = y

	# DRAW BALL
	draw_blue(x,y)
	draw_blue(x+1,y)


def move_paddle(side, dtion):
	global LEFT_PADDLE_Y
	global RIGHT_PADDLE_Y

	if side == "LEFT":
		x = 0
		y = LEFT_PADDLE_Y
	elif side == "RIGHT":
		x = WIDTH - 1
		y = RIGHT_PADDLE_Y


	# 1. blackout old spot edge pixel
	# 2. draw new edge pixel
	# 3. adjust paddle variable

	if dtion == "UP" and y-3 > 0:
		draw_black(x, y+2)
		draw_white(x, y-3)
		if side == "LEFT":
			LEFT_PADDLE_Y -= 1
		elif side == "RIGHT":
			RIGHT_PADDLE_Y -= 1


	elif dtion == "DOWN" and y+3 < HEIGHT:
		draw_black(x, y-2)
		draw_white(x, y+3)
		if side == "LEFT":
			LEFT_PADDLE_Y += 1
		elif side == "RIGHT":
			RIGHT_PADDLE_Y += 1

pause = 0

def gameloop():

	blackout()

	fgbg(9)
	setpos(WIDTH//3 +5 , HEIGHT//4 * 3)
	sys.stdout.write("press space to play")
	sys.stdout.flush()

	with KeyPoller() as keyPoller:
		while 1:
			char = keyPoller.poll()
			if char == " ":
				break

	blackout()
	init_ball("LEFT")

	while 1:
		# PAINT SCREEN
		init_pong()

		# CHARACTER INPUT
		ch = None
		with KeyPoller() as keyPoller:
			for i in range(5000):
				c = keyPoller.poll()
				if c:
					ch = c	

		# MOVE PADDLES
		if ch == "w" and not TESTING:
			move_paddle("LEFT", "UP")
		elif ch == "s" and not TESTING:
			move_paddle("LEFT", "DOWN")
		elif ch =="o":
			move_paddle("RIGHT", "UP")
		elif ch == "l":
			move_paddle("RIGHT", "DOWN")

		# MOVE BALL

		global DX, DY, BALL_X, BALL_Y, pause


		if pause != 4:
			pause += 1
			continue

		else:
			pause = 0 

		# bounce of walls for now
		if BALL_X + DX <= 0 or BALL_X + DX + 2 >= WIDTH:
			DX = -DX

		if BALL_Y + DY < 0 or BALL_Y + DY >= HEIGHT:
			DY = -DY

		new_x = BALL_X + DX 
		new_y = BALL_Y + DY

		draw_black(BALL_X, BALL_Y)
		draw_black(BALL_X+1, BALL_Y)

		draw_blue(new_x, new_y)
		draw_blue(new_x+1, new_y)

		BALL_X = new_x
		BALL_Y = new_y


if __name__ == '__main__':

	# init_pong()

	gameloop()
	# test_key2()

	# draw_paddles()	

	# test_paint()
	# test_getchar()

	# test3()
	# test_2()
