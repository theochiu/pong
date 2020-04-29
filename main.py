
import time, sys

# constants
HEIGHT = 30
WIDTH = 118
CSI = "\033["
TESTING = True



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
		try:
			tty.setraw(sys.stdin.fileno())
			ch = sys.stdin.read(1)
		finally:
			termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
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
	setpos(x, y)
	fgbg(0x0f)
	sys.stdout.write(' ')
	sys.stdout.flush()

def draw_black(x, y):
	setpos(x, y)
	fgbg(0x00)
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

def init_pong():
	''' initialize the screen for the game'''
	# make everything black
	fgbg(0)					# color black
	for y in range(HEIGHT):
		setpos(0,y)
		for x in range(WIDTH):
			sys.stdout.write(" ")


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
	draw_score(0, 0)
	draw_score(1, 0)


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

def gameloop():

	while 1:
		ch = getchar()
		if ch == "w" and not TESTING:
			move_paddle("LEFT", "UP")
		elif ch == "s" and not TESTING:
			move_paddle("LEFT", "DOWN")
		elif ch =="o":
			move_paddle("RIGHT", "UP")
		elif ch == "l":
			move_paddle("RIGHT", "DOWN")



if __name__ == '__main__':

	init_pong()

	gameloop()

	# draw_paddles()	

	# test_paint()
	# test_getchar()

	# test3()
	# test_2()
