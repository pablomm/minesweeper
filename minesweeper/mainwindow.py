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

from PyQt4 import QtGui, QtCore
from PyQt4.phonon import Phonon
from PyQt4.QtCore import QTranslator
from buttonbar import ButtonBar
import menubar
import board


from PyQt4 import QtTest


class Sound(QtCore.QObject):

    def __init__(self, soundFile, parent):
        QtCore.QObject.__init__(parent)
        self.parent = parent
        self.soundFile = soundFile

        self.mediaObject = Phonon.MediaObject()
        self._audioOutput = Phonon.AudioOutput(Phonon.MusicCategory)
        self._path = Phonon.createPath(self.mediaObject, self._audioOutput)
        self.mediaSource = Phonon.MediaSource(soundFile)
        self.mediaObject.setCurrentSource(self.mediaSource)

    def play(self):
        if self.parent.settings.sound:
            self.mediaObject.stop()
            self.mediaObject.seek(0)
            self.mediaObject.play()


class MainWindow(QtGui.QMainWindow):
    def __init__(self, setting):
        QtGui.QMainWindow.__init__(self)

        self.settings = setting
        self.guiBoard = None

        self.setSizePolicy(QtGui.QSizePolicy(
            QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed))
        self.laught = Sound(self.settings.laught_file, self)
        self.applause = Sound(self.settings.applause_file, self)
        self.createMenuBar()

        self.markBar = ButtonBar(self)
        self.centralwidget = QtGui.QWidget()
        self.setCentralWidget(self.centralwidget)
        self.vLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.vLayout.addWidget(self.markBar)

        self.new_game()

        self.center()

    def getTime(self):
        if self.markBar:
            return self.markBar.clock.time
        return 0

    def dead(self):

        self.markBar.clock.stop()
        self.markBar.face.dead()
        self.laught.play()

    def win(self):

        if not self.settings.finished:
            self.settings.finished = True
            self.markBar.clock.stop()
            self.markBar.face.sunglasses()
            self.applause.play()

    def start_game(self):
        if self.settings.started:
            return

        self.settings.started = True
        self.markBar.face.thinking()
        self.markBar.clock.start()

    def updateSize(self, height, width):

        self.settings.b_height = height
        self.settings.b_width = width

        self.updateMines()

    def updateMines(self, mines_percent=None):

        if mines_percent:
            self.settings.mines_percent = mines_percent

        self.settings.n_mines = max(int(
            self.settings.mines_percent * self.settings.b_height * self.settings.b_width), 1)

        self.new_game()

    def new_game(self, old_board=None):

        resize = False

        self.settings.game_name = None
        if self.settings.b_height != self.settings.l_height or self.settings.b_width != self.settings.l_width:
            resize = True

        self.settings.l_height = self.settings.b_height
        self.settings.l_width = self.settings.b_width

        if resize:
            self.new_game_resized(old_board)
            return

        if self.settings.animation or self.settings.opening:
            self.settings.animation = False
            self.settings.opening = False
            QtTest.QTest.qWait(2 * self.settings.wait)

        if self.guiBoard:
            self.guiBoard.deleteLater()

        self.markBar.flags.start()
        self.settings.started = False
        self.settings.finished = False
        self.markBar.clock.stop()
        self.markBar.clock.reset()
        self.markBar.face.sleeping()

        if not old_board:
            self.guiBoard = board.Board(self, self.settings.safe_start)
        else:
            self.guiBoard = old_board

        self.vLayout.addWidget(self.guiBoard)
        self.guiBoard.updateGeometry()
        # self.vLayout.updateGeometry()
        self.centralwidget.updateGeometry()
        self.updateGeometry()
        self.centralwidget.setFixedSize(self.centralwidget.sizeHint())

        self.setFixedSize(self.sizeHint())

    def new_game_resized(self, old_board=None):

        if self.settings.animation:
            self.settings.animation = False
            QtTest.QTest.qWait(2 * self.settings.wait)

        self.settings.started = False
        self.settings.finished = False
        self.markBar.clock.stop()
        self.lastWidget = self.centralwidget

        if not old_board:
            self.guiBoard = board.Board(self)
        else:
            self.guiBoard = old_board

        self.markBar = ButtonBar(self)
        self.centralwidget = QtGui.QWidget()

        self.vLayout = QtGui.QVBoxLayout(self.centralwidget)

        self.vLayout.addWidget(self.markBar)

        self.vLayout.addWidget(self.guiBoard)

        self.setCentralWidget(self.centralwidget)
        self.setFixedSize(self.layout().sizeHint())

    def changeLanguage(self, name, file):
        self.settings.app.removeTranslator(self.settings.translator)
        self.settings.translator = QTranslator()
        if file:
            self.settings.translator.load(file)
        self.settings.app.installTranslator(self.settings.translator)
        self.settings.language = name
        self.setWindowTitle(self.tr('Minesweeper'))
        self.createMenuBar()

    def createMenuBar(self):

        self.menuBar().clear()
        self.menuBar().addMenu(menubar.FileMenu(self))
        self.menuBar().addMenu(menubar.GameMenu(self))
        self.menuBar().addMenu(menubar.OptionMenu(self))
        self.menuBar().addMenu(menubar.AboutMenu(self))

    def center(self):
        frameGm = self.frameGeometry()
        screen = QtGui.QApplication.desktop().screenNumber(
            QtGui.QApplication.desktop().cursor().pos())
        centerPoint = QtGui.QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())
