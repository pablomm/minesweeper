# -*- coding: utf-8 -*-
#
#	Minesweeper - Python implementation with PyQt4 of minesweeper game
#
#    Copyright (C) 2017  
#			Pablo Marcos - pablo.marcosm@estudiante.uam.es
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from math import log10
from PyQt4 import QtGui, QtCore

class Clock(QtGui.QLCDNumber):
	def __init__(self,parent):
		QtGui.QLCDNumber.__init__(self,parent)
		self.parent = parent
		self.time = 0
		self.timer = QtCore.QTimer(self)
		self.timer.timeout.connect(self.update)
		self.reset()
		self.setStyleSheet("QWidget {background-color: %s}" % self.parent.settings.color)

	def reset(self):
		self.time = 0
		self.timer.stop()
		self.display(QtCore.QString("000"))

	def start(self):
		self.timer.start(1000)

	def stop(self):
		self.timer.stop()

	def update(self):
		self.time += 1

		if self.time < 100:
			self.display(QtCore.QString("%1").arg(self.time, 3, 10, QtCore.QChar('0')))
		else:
			self.display(self.time)

class Flags(QtGui.QLCDNumber):
	def __init__(self,parent):
		QtGui.QLCDNumber.__init__(self,parent)
		self.parent = parent
		self.n = 0
		self.max = 0
		self.setStyleSheet("QWidget {background-color: %s}" % self.parent.settings.color)
		self.start()

	def start(self):

		self.max = int(log10(max(self.parent.settings.n_mines,1))) + 2

		self.number(self.parent.settings.n_mines)

	def number(self,n):
		self.n = n
		self.display(QtCore.QString("%1").arg(n, self.max, 10, QtCore.QChar('0')))

	def increase(self):
		self.number(self.n + 1)
		

	def decrease(self):
		self.number(self.n - 1)


class FaceButton(QtGui.QPushButton):
	def __init__(self,parent, mainWindow):
		QtGui.QPushButton.__init__(self,parent)
		self.parent = mainWindow
		self.setFixedSize(self.parent.settings.face_size, self.parent.settings.face_size)
		self.setIcon(self.parent.settings.sleeping_icon)
		self.clicked.connect(self.new_game)

	def new_game(self):
		self.parent.new_game()

	def dead(self):
		self.setIcon(self.parent.settings.dead_icon)

	def sunglasses(self):
		self.setIcon(self.parent.settings.sunglasses_icon)

	def thinking(self):
		self.setIcon(self.parent.settings.thinking_icon)

	def sleeping(self):
		self.setIcon(self.parent.settings.sleeping_icon)

class ButtonBar(QtGui.QWidget):
	def __init__(self,parent):
		QtGui.QWidget.__init__(self,parent)
		self.parent = parent


		self.face = FaceButton(self, self.parent)
		self.clock = Clock(self.parent)
		self.flags = Flags(self.parent)

		self.layout = QtGui.QHBoxLayout(self)
		self.layout.addWidget(self.clock)
		self.layout.addWidget(self.face)
		self.layout.addWidget(self.flags)
		self.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Fixed))


