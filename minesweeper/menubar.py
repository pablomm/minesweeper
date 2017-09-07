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

from __future__ import division

from webbrowser import open as webopen
from fnmatch import fnmatch
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from save import saveGame


class FileMenu(QMenu):
    def __init__(self, parent):
        QMenu.__init__(self, parent)

        self.parent = parent
        self.setTitle(self.tr('File'))

        # Load Action
        loadAction = QAction("&" + self.tr('Load'), self)
        loadAction.triggered.connect(self.loadFile)
        loadAction.setShortcut('Ctrl+L')
        self.addAction(loadAction)

        # Save Action
        saveAction = QAction("&" + self.tr('Save'), self)
        saveAction.setShortcut('Ctrl+S')
        saveAction.triggered.connect(self.saveFile)
        self.addAction(saveAction)

        # Save Action
        saveasAction = QAction("&" + self.tr('Save as'), self)
        saveasAction.setShortcut('Ctrl+A')
        saveasAction.triggered.connect(self.saveasFile)
        self.addAction(saveasAction)


        # Exit action
        exitAction = QAction("&" + self.tr('Exit'), self)
        exitAction.triggered.connect(self.parent.close)
        exitAction.setShortcut('Ctrl+Q')
        self.addAction(exitAction)

    def loadFile(self):

        dlg = QFileDialog(self)
        fname = dlg.getOpenFileName(self,self.tr('Load game'),self.parent.settings.save,self.parent.settings.save_files)

    def saveFile(self):
        if not self.parent.settings.game_name:
            self.saveasFile()
        else:

            saveGame(self.parent.settings.game_name,self.parent.guiBoard,self.parent.markBar.clock.time,self.parent.settings)

        

    def saveasFile(self):
        dlg = QFileDialog(self)
        fname = dlg.getSaveFileName(self,self.tr('Save as'),self.parent.settings.save,self.parent.settings.save_files)

        if fname:
            if not fnmatch(fname,str(self.parent.settings.save_files)):
                fname += ".sav"
            self.parent.settings.game_name = fname
            self.saveFile()

class GameMenu(QMenu):
    def __init__(self, parent):

        QMenu.__init__(self, parent)
        self.setTitle(self.tr('Game'))
        self.parent = parent
        self.addMenu(SizeMenu(parent))
        self.addMenu(DifficultyMenu(parent))

        start = QAction("&" + self.tr('Safe start'), self)
        start.setCheckable(True)
        start.setChecked(self.parent.settings.safe_start)
        start.triggered.connect(self.safe_start)
        self.addAction(start)

    def safe_start(self):
        self.parent.settings.safe_start = not self.parent.settings.safe_start


class OptionMenu(QMenu):
    def __init__(self, parent):

        QMenu.__init__(self, parent)
        self.parent = parent
        self.setTitle(self.tr('Options'))

        sound = QAction("&" + self.tr('Sound'), self)
        sound.setCheckable(True)
        sound.setChecked(self.parent.settings.sound)
        sound.triggered.connect(self.mute)
        self.addAction(sound)

        self.addMenu(AnimationMenu(self))
        self.addMenu(LanguageMenu(self))

    def mute(self):
        self.parent.settings.sound = not self.parent.settings.sound


class AnimationMenu(QMenu):
    def __init__(self, parent):

        QMenu.__init__(self, parent)
        self.setTitle("&" + self.tr('Animation'))
        self.parent = parent

        slow = QAction("&" + self.tr('Slow'), self)
        slow.setCheckable(True)
        slow.triggered.connect(lambda: self.animation_speed(2))
        self.addAction(slow)
        if self.parent.parent.settings.delay_speed == 2:
            slow.setChecked(True)

        medium = QAction("&" + self.tr('Medium'), self)
        medium.setCheckable(True)
        medium.triggered.connect(lambda: self.animation_speed(4))
        self.addAction(medium)
        if self.parent.parent.settings.delay_speed == 4:
            medium.setChecked(True)

        fast = QAction("&" + self.tr('Fast'), self)
        fast.setCheckable(True)
        fast.triggered.connect(lambda: self.animation_speed(8))
        self.addAction(fast)
        if self.parent.parent.settings.delay_speed == 8:
            fast.setChecked(True)

        disabled = QAction("&" + self.tr('Disabled'), self)
        disabled.setCheckable(True)
        disabled.triggered.connect(lambda: self.delay(False))
        self.addAction(disabled)
        if self.parent.parent.settings.open_delay == False:
            disabled.setChecked(True)

        self.newGameGroup = QActionGroup(self)
        self.newGameGroup.addAction(slow)
        self.newGameGroup.addAction(medium)
        self.newGameGroup.addAction(fast)
        self.newGameGroup.addAction(disabled)
        self.newGameGroup.setExclusive(True)

    def animation_speed(self, speed):
        self.delay(True)
        self.parent.parent.settings.delay_speed = speed

    def delay(self, value):
        self.parent.parent.settings.open_delay = value


class AboutMenu(QMenu):
    def __init__(self, parent):
        QMenu.__init__(self, parent)
        self.setTitle(self.tr('About'))
        self.parent = parent

        license = QAction("&" + self.tr('License'), self)
        license.triggered.connect(lambda: webopen(
            self.parent.settings.license_web_page))
        self.addAction(license)

        github = QAction("&" + self.tr('Go to github'), self)
        github.triggered.connect(
            lambda: webopen(self.parent.settings.web_page))
        self.addAction(github)


class LanguageMenu(QMenu):
    def __init__(self, parent):
        QMenu.__init__(self, parent)
        self.parent = parent
        self.setTitle("&" + self.tr('Languages'))

        if not self.parent.parent.settings.translations:
            empty = QAction('No languages avaible', self)
            empty.setEnabled(False)
            self.addAction(empty)
        else:

            self.languageGroup = QActionGroup(self)
            self.languageGroup.setExclusive(True)

            l = QAction(self.tr("Default"), self)
            l.triggered.connect(
                lambda: parent.parent.changeLanguage(None, None))
            l.setCheckable(True)
            if not self.parent.parent.settings.language:
                l.setChecked(True)
            self.languageGroup.addAction(l)
            self.addAction(l)

            for language in self.parent.parent.settings.translations:
                name, file, folder = language
                l = QAction(name, self)
                l.triggered.connect(
                    lambda: parent.parent.changeLanguage(name, folder + file))
                l.setCheckable(True)
                if name == self.parent.parent.settings.language:
                    l.setChecked(True)
                self.languageGroup.addAction(l)
                self.addAction(l)


class SizeMenu(QMenu):

    def __init__(self, parent):
        QMenu.__init__(self, parent)
        self.setTitle("&" + self.tr('Size'))

        self.parent = parent
        smallGame = QAction("&" + self.tr('Small'), self)
        smallGame.setCheckable(True)
        smallGame.triggered.connect(lambda: parent.updateSize(
            parent.settings.small_height, parent.settings.small_width))
        self.addAction(smallGame)

        mediumGame = QAction("&" + self.tr('Medium'), self)
        mediumGame.setCheckable(True)
        mediumGame.triggered.connect(lambda: parent.updateSize(
            parent.settings.medium_height, parent.settings.medium_width))
        self.addAction(mediumGame)

        bigGame = QAction("&" + self.tr('Big'), self)
        bigGame.setCheckable(True)
        bigGame.triggered.connect(lambda: parent.updateSize(
            parent.settings.big_height, parent.settings.big_width))
        self.addAction(bigGame)

        customGame = QAction("&" + self.tr('Custom'), self)
        customGame.setCheckable(True)
        customGame.triggered.connect(lambda: SizePopUP(self).show())
        self.addAction(customGame)

        self.newGameGroup = QActionGroup(self)
        self.newGameGroup.addAction(smallGame)
        self.newGameGroup.addAction(mediumGame)
        self.newGameGroup.addAction(bigGame)
        self.newGameGroup.addAction(customGame)
        self.newGameGroup.setExclusive(True)

        if parent.settings.small_height == parent.settings.b_height and parent.settings.small_width == parent.settings.b_width:
            smallGame.setChecked(True)
        elif parent.settings.medium_height == parent.settings.b_height and parent.settings.medium_width == parent.settings.b_width:
            mediumGame.setChecked(True)
        elif parent.settings.big_height == parent.settings.b_height and parent.settings.big_width == parent.settings.b_width:
            bigGame.setChecked(True)
        else:
            customGame.setChecked(True)


class SizePopUP(QDialog):
    def __init__(self, parent):
        QDialog.__init__(self, parent)

        self.parent = parent
        self.layout = QFormLayout(self)
        self.setWindowTitle(self.tr("Custom size"))
        self.onlyInt = QIntValidator(1, 99)
        self.xInput = QLineEdit()
        self.xInput.setValidator(self.onlyInt)
        self.xInput.setPlaceholderText(
            QString(str(self.parent.parent.settings.b_height)))

        self.yInput = QLineEdit()
        self.yInput.setValidator(self.onlyInt)
        self.yInput.setPlaceholderText(
            QString(str(self.parent.parent.settings.b_width)))

        self.accept = QPushButton(self.tr("Accept"))
        self.accept.clicked.connect(self.submit)

        self.cancel = QPushButton(self.tr("Cancel"))
        self.cancel.clicked.connect(self.close)

        self.layout.addRow(self.xInput, self.yInput)
        self.layout.addRow(self.accept, self.cancel)

    def submit(self):

        self.parent.parent.updateSize(max(int(self.xInput.text()), 7) if not self.xInput.text().isEmpty() else self.parent.parent.settings.b_height, int(
            self.yInput.text()) if not self.yInput.text().isEmpty() else self.parent.parent.settings.b_width)
        self.close()


class DifficultyMenu(QMenu):

    def __init__(self, parent):
        QMenu.__init__(self, parent)
        self.parent = parent
        self.setTitle("&" + self.tr('Difficulty'))

        easy = QAction("&" + self.tr('Easy'), self)
        easy.setCheckable(True)
        easy.triggered.connect(
            lambda: self.parent.updateMines(self.parent.settings.easy))
        self.addAction(easy)

        normal = QAction("&" + self.tr('Normal'), self)
        normal.setCheckable(True)
        normal.triggered.connect(
            lambda: self.parent.updateMines(self.parent.settings.normal))
        self.addAction(normal)

        hard = QAction("&" + self.tr('Hard'), self)
        hard.setCheckable(True)
        hard.triggered.connect(
            lambda: self.parent.updateMines(self.parent.settings.hard))
        self.addAction(hard)

        insane = QAction("&" + self.tr('Custom'), self)
        insane.triggered.connect(lambda: DifficultyPopUP(self).show())
        insane.setCheckable(True)
        self.addAction(insane)

        self.difficultyGroup = QActionGroup(self)
        self.difficultyGroup.addAction(easy)
        self.difficultyGroup.addAction(normal)
        self.difficultyGroup.addAction(hard)
        self.difficultyGroup.addAction(insane)
        self.difficultyGroup.setExclusive(True)

        if self.parent.settings.mines_percent == self.parent.settings.easy:
            easy.setChecked(True)

        elif self.parent.settings.mines_percent == self.parent.settings.normal:
            normal.setChecked(True)

        elif self.parent.settings.mines_percent == self.parent.settings.hard:
            hard.setChecked(True)
        else:
            insane.setChecked(True)


class DifficultyPopUP(QDialog):
    def __init__(self, parent):
        QDialog.__init__(self, parent)

        self.parent = parent
        self.layout = QFormLayout(self)
        self.setWindowTitle(self.tr("Porcentage of mines"))

        self.sl = QSlider(Qt.Horizontal)
        self.sl.setMinimum(1)
        self.sl.setMaximum(100)
        self.sl.setValue(int(self.parent.parent.settings.mines_percent*100))
        self.sl.setTickPosition(QSlider.TicksBelow)
        self.sl.setTickInterval(5)



        self.accept = QPushButton(self.tr("Accept"))
        self.accept.clicked.connect(self.submit)

        self.cancel = QPushButton(self.tr("Cancel"))
        self.cancel.clicked.connect(self.close)

        self.layout.addRow(self.sl)
        self.layout.addRow(self.accept, self.cancel)

    def submit(self):

        self.parent.parent.updateMines(self.sl.value()/100.0)
        self.close()
