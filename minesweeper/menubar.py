# -*- coding: utf-8 -*-

from __future__ import division

from webbrowser import open as webopen

from PyQt4.QtGui import QMenu, QAction, QFormLayout, QLineEdit, QPushButton, QDialog, QActionGroup, QIntValidator
from PyQt4.QtCore import QString


class FileMenu(QMenu):
	def __init__(self, parent):
		QMenu.__init__(self,parent)

		self.parent = parent
		self.setTitle(self.tr('File'))

		#Load Action
		loadAction = QAction("&" + self.tr('Load'), self)
		loadAction.setShortcut('Ctrl+L')
		self.addAction(loadAction)

		#Save Action
		saveAction = QAction("&" + self.tr('Save'), self)
		saveAction.setShortcut('Ctrl+S')
		self.addAction(saveAction)

		#Exit action
		exitAction = QAction("&" + self.tr('Exit'), self)
		exitAction.triggered.connect(self.parent.close)
		exitAction.setShortcut('Ctrl+Q')
		self.addAction(exitAction)


class GameMenu(QMenu):
	def __init__(self, parent):

		QMenu.__init__(self,parent)
		self.setTitle(self.tr('Game'))
		self.parent = parent
		self.addMenu(SizeMenu(parent))
		self.addMenu(DifficultyMenu(parent))



class OptionMenu(QMenu):
	def __init__(self, parent):

		QMenu.__init__(self,parent)
		self.parent = parent
		self.setTitle(self.tr('Options'))

		sound = QAction("&" + self.tr('Sound'), self)
		sound.setCheckable(True)
		sound.setChecked(True)
		sound.triggered.connect(self.mute)
		self.addAction(sound)	

		self.addMenu(AnimationMenu(self))
		self.addMenu(LanguageMenu(self))


	def mute(self):
		self.parent.settings.sound = not self.parent.settings.sound


class AnimationMenu(QMenu):
	def __init__(self, parent):

		QMenu.__init__(self,parent)
		self.setTitle("&" + self.tr('Animation'))
		self.parent = parent

		slow = QAction("&" + self.tr('Slow'), self)
		slow.setCheckable(True)
		slow.triggered.connect(lambda: self.animation_speed(2))
		self.addAction(slow)

		medium = QAction("&" + self.tr('Medium'), self)
		medium.setCheckable(True)
		medium.setChecked(True)
		medium.triggered.connect(lambda: self.animation_speed(4))
		self.addAction(medium)

		fast = QAction("&" + self.tr('Fast'), self)
		fast.setCheckable(True)
		fast.triggered.connect(lambda: self.animation_speed(8))
		self.addAction(fast)

		disabled = QAction("&" + self.tr('Disabled'), self)
		disabled.setCheckable(True)
		disabled.triggered.connect(lambda: self.delay(False))
		self.addAction(disabled)

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
		QMenu.__init__(self,parent)
		self.setTitle(self.tr('About'))
		self.parent = parent

		license = QAction("&" + self.tr('License'), self)
		license.triggered.connect(lambda: webopen(self.parent.settings.license_web_page))
		self.addAction(license)

		github = QAction("&" + self.tr('Go to github'), self)
		github.triggered.connect(lambda: webopen(self.parent.settings.web_page))
		self.addAction(github)

class LanguageMenu(QMenu):
	def __init__(self, parent):
		QMenu.__init__(self,parent)
		self.parent = parent
		self.setTitle("&" + self.tr('Languages'))

		english = QAction("&" + self.tr('English'), self)
		english.setCheckable(True)
		english.setChecked(True)
		english.triggered.connect(self.parent.parent.settings.loadTranslation)
		self.addAction(english)	
		


		spanish = QAction("&" + self.tr('Spanish'), self)
		spanish.setCheckable(True)
		spanish.triggered.connect(self.parent.parent.settings.loadTranslation)
		self.addAction(spanish)	

		french = QAction("&" + self.tr('French'), self)
		french.setCheckable(True)
		french.triggered.connect(self.parent.parent.settings.loadTranslation)
		self.addAction(french)	


class SizeMenu(QMenu):

	def __init__(self,parent):
		QMenu.__init__(self,parent)
		self.setTitle("&" + self.tr('Size'))

		self.parent = parent
		smallGame = QAction("&" + self.tr('Small'), self)
		smallGame.setCheckable(True)
		smallGame.triggered.connect(lambda: parent.updateSize(parent.settings.small_height,parent.settings.small_width))
		self.addAction(smallGame)

		mediumGame = QAction("&" + self.tr('Medium'), self)
		mediumGame.setCheckable(True)
		mediumGame.setChecked(True)
		mediumGame.triggered.connect(lambda: parent.updateSize(parent.settings.medium_height,parent.settings.medium_width))
		self.addAction(mediumGame)

		bigGame = QAction("&" + self.tr('Big'), self)
		bigGame.setCheckable(True)
		bigGame.triggered.connect(lambda: parent.updateSize(parent.settings.big_height,parent.settings.big_width))
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

class SizePopUP(QDialog):
	def __init__(self,parent):
		QDialog.__init__(self,parent)

		self.parent = parent
		self.layout = QFormLayout(self)
		self.setWindowTitle(self.tr("Custom size"))
		self.onlyInt = QIntValidator(1,99)
		self.xInput = QLineEdit()
		self.xInput.setValidator(self.onlyInt)
		self.xInput.setPlaceholderText(QString(str(self.parent.parent.settings.b_height)))

		self.yInput = QLineEdit()
		self.yInput.setValidator(self.onlyInt)
		self.yInput.setPlaceholderText(QString(str(self.parent.parent.settings.b_width)))

		self.accept = QPushButton(self.tr("Accept"))
		self.accept.clicked.connect(self.submit)

		self.cancel = QPushButton(self.tr("Cancel"))
		self.cancel.clicked.connect(self.close)

		self.layout.addRow(self.xInput,self.yInput)
		self.layout.addRow(self.accept, self.cancel)



	def submit(self):

		self.parent.parent.updateSize(max(int(self.xInput.text()),7) if not self.xInput.text().isEmpty() else self.parent.parent.settings.b_height,int(self.yInput.text()) if not self.yInput.text().isEmpty() else self.parent.parent.settings.b_width)
		self.close()



class DifficultyMenu(QMenu):

	def __init__(self, parent):
		QMenu.__init__(self,parent)
		self.parent = parent
		self.setTitle("&" + self.tr('Difficulty'))


		easy = QAction("&" + self.tr('Easy'), self)
		easy.setCheckable(True)
		easy.triggered.connect(lambda: self.parent.updateMines(self.parent.settings.easy))
		self.addAction(easy)

		normal = QAction("&" + self.tr('Normal'), self)
		normal.setCheckable(True)
		normal.setChecked(True)
		normal.triggered.connect(lambda: self.parent.updateMines(self.parent.settings.normal))
		self.addAction(normal)

		hard = QAction("&" + self.tr('Hard'), self)
		hard.setCheckable(True)
		hard.triggered.connect(lambda: self.parent.updateMines(self.parent.settings.hard))
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



class DifficultyPopUP(QDialog):
	def __init__(self,parent):
		QDialog.__init__(self,parent)

		self.parent = parent
		self.layout = QFormLayout(self)
		self.setWindowTitle(self.tr("Porcentage of mines"))

		self.minesInput = QLineEdit()
		self.minesInput.setValidator(QIntValidator(1,100))
		self.minesInput.setPlaceholderText(QString(str(int(self.parent.parent.settings.mines_percent * 100)) + str('%')))

		self.accept = QPushButton(self.tr("Accept"))
		self.accept.clicked.connect(self.submit)

		self.cancel = QPushButton(self.tr("Cancel"))
		self.cancel.clicked.connect(self.close)

		self.layout.addRow(self.minesInput)
		self.layout.addRow(self.accept, self.cancel)



	def submit(self):

		self.parent.parent.updateMines(None if self.minesInput.text().isEmpty() else (float(self.minesInput.text())/100))
		self.close()




