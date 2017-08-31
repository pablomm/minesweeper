
from random import shuffle
from PyQt4 import QtGui, QtCore, Qt
import settings

from PyQt4 import QtTest

from sets import Set

class Cell(QtGui.QPushButton):

	def __init__(self, parent,x,y, bomb=False, size=20, adjacent=0):
		QtGui.QPushButton.__init__(self, " ")
		self.parent = parent
		self._bomb = bomb
		self.adjacent = adjacent
		self.opened = False
		self.marked = False
		self.size = size
		self.setFixedSize(self.parent.settings.icon_size,self.parent.settings.icon_size)
		self.x = x
		self.y = y
		self.explored = False

	@property
	def bomb(self):
		return self._bomb

	def flag_icon(self,flag=True):

		if flag and not self.parent.settings.use_text:
			# Sets flag icon
			self.setIcon(self.parent.settings.flag_icon)
			self.setIconSize(self.rect().size())

		elif flag:
			# Sets and ? if icon is disabled
			self.setText("?")

		elif self.parent.settings.use_text:
			# Clear the ? if icon is not enabled
			self.setText(" ")
		else:
			# Clears the icon
			self.setIcon(self.parent.settings.empty_icon)


	def open(self,game_over=False):

		# Check opening flag
		if not self.parent.settings.opening:
			return False

		# Start the chrono if needed
		if not self.parent.settings.started:
			self.parent.parent.start_game()


		if not self.opened:
			self.opened = True
			self.setFlat(True)

			if self._bomb:
				self.setIcon(self.parent.settings.mine_icon)

				if not game_over:
					self.parent.game_over()

			elif not self.adjacent:
				self.setIcon(self.parent.settings.empty_icon)
				self.parent.cell_open()
				if not game_over:
					self.parent.open_adjacents(self)

			else:
				self.parent.cell_open()
				self.setIcon(self.parent.settings.empty_icon)
				self.setText(str(self.adjacent))

			self.setEnabled(False)

			return self.adjacent if not self.bomb else -1

		return 1

	def mark(self):

		# Start the chrono if needed
		if not self.parent.settings.started:
			self.parent.parent.start_game()

		# Change the flag state
		self.marked = not self.marked

		if self.marked:
			# Decrease the flag counter and puts icon
			self.parent.parent.markBar.flags.decrease()
			self.flag_icon(True)
		else:
			# Increase the flag counter and clear icon
			self.parent.parent.markBar.flags.increase()
			self.flag_icon(False)

		return self.marked

	def mousePressEvent(self,event):

 		if self.parent.settings.finished:
			return

		if event.button() == QtCore.Qt.LeftButton:
			if not self.marked and not self.opened:
				self.parent.settings.opening = True
				QtGui.QPushButton.mousePressEvent(self,event)
				self.open()
				self.parent.settings.opening = False
			return

		elif event.button() == QtCore.Qt.RightButton:
			if not self.opened:
				QtGui.QPushButton.mousePressEvent(self,event)
				self.mark()
			return

		return False

		



class Board(QtGui.QWidget):

	def __init__(self, parent):
		QtGui.QWidget.__init__(self, parent)
		self.parent = parent
		self.settings = parent.settings
		self._x = self.settings.b_width
		self._y = self.settings.b_height
		self.n_bomb = self.settings.n_mines
		self.cells = []
		self.grid = QtGui.QGridLayout(self)
		self.grid.setSpacing(0)
		self.closed = self._x * self._y
		self.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Fixed))
		#self.setStyleSheet("QWidget {background-color: %s}" % "#e0e0d1")

		self.initialize_board()
		self.updateGeometry()



	def adjacents(self,x,y):
		
		cells = []
		for i in range(-1,2):
			for j in range(-1,2):
				if (i!=0 or j!=0) and x+i >= 0 and x+i < self._x and y+j >= 0 and y+j < self._y:
					cells.append(self.cells[x+i][y+j])

		return cells

	def cell_open(self):

		self.closed -= 1
		if self.closed == self.n_bomb:
			self.parent.win()

	def initialize_board(self):
		bombs = self.n_bomb * [True] + (self._x*self._y - self.n_bomb) * [False]

		shuffle(bombs)

		for i in range(self._x):
			self.cells.append(list())
			for j in range(self._y):

				cell = Cell(self,i,j,bombs[i*self._y + j])
				self.grid.addWidget(cell, i+1, j)

				self.cells[i].append(cell)

		self.initialize_cells()

	def open_adjacents(self, cell):

		self.parent.settings.animation = True

		cells_open = Set([cell])
		cells_explored = Set()

		while cells_open:
			c = cells_open.pop()
			if not c.explored:
				c.explored = True
				cells_explored.add(c)

				if not c.adjacent and not c.bomb:
					cells_open |= Set(self.adjacents(c.x,c.y))


		for c in cells_explored:
			c.explored = False

		#shuffle(cells)
		i = 0
		for c in cells_explored:
			i = (i+1) % self.parent.settings.delay_speed
			if not self.parent.settings.animation:
				break

			c.open(True)
			if self.settings.open_delay and not i:
				QtTest.QTest.qWait(self.settings.wait)

		self.parent.settings.animation = False

	def initialize_cells(self):
		for i in range(self._x):
			for j in range(self._y):
				self.cells[i][j].adjacent = sum(x.bomb for x in self.adjacents(i,j))

	def mark(self,x,y):
		return self.cells[x][y].mark()

	def game_over(self):

		self.parent.settings.finished = True
		self.parent.settings.animation = True
		self.parent.dead()

		to_open = []
		for row in self.cells:
			for c in row:
				to_open.append(c)

		shuffle(to_open)
		i = 0

		for a in to_open:

			i = (i+1) % self.parent.settings.delay_speed
			if not self.parent.settings.animation:
				break

			a.open(True)
			if self.parent.settings.open_delay and i:
				QtTest.QTest.qWait(self.settings.wait)

		self.parent.settings.animation = False
			
	
		

	def __str__(self):
		string = ""

		for i in range(self._x):
			string += "|"
			for j in range(self._y):
				string += str(self.cells[i][j]) + "|"

			string += "\n"

		return string

	@property
	def x(self):
		return self._x

	@property
	def y(self):
		return self._y








