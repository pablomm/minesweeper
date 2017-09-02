# -*- coding: utf-8 -*-

from PyQt4.QtCore import QTranslator
from PyQt4.QtGui import QIcon

class Settings:
	def __init__(self, app):

		# Qt Application
		self.app = app

		# Translator instance
		self.translator = QTranslator()
		self.translations = []

		# Folders
		self.resource = 'resource/'
		self.translate = 'translate/'

		# Predefined Sizes
		self.small_height = 20
		self.small_width = 16
		self.medium_height = 32
		self.medium_width = 16
		self.big_height = 40
		self.big_width = 20

		self.web_page = 'https://github.com/pablomm/minesweeper'


		# Last size
		self.l_height = self.medium_height
		self.l_width = self.medium_width

		# Actual size
		self.b_height = self.medium_height
		self.b_width = self.medium_width

		# Percentages of mines
		self.easy = 0.08
		self.normal = 0.15
		self.hard  = 0.24

		# Current percentage of mines
		self.mines_percent = self.normal

		# Actual amount of sizes
		self.n_mines = int(self.mines_percent * self.b_height * self.b_width)

		# Delay in ms opening
		self.wait = 1

		# Flag for opening delay
		self.open_delay = True
		self.delay_speed = 4

		# Game internal flags
		self.started = False
		self.finished = False
		self.opening = False
		self.animation = False

		# Color of LCDnumbers
		self.color = "#f9f2ec"
		self.number_color = [None, 'blue', 'green','red','darkblue','darkred','LightSeaGreen' ,'black', 'darkgrey' ]

		# Sound flag
		self.sound = True

		# Sound files
		self.laught_file = self.resource + "laught.mp3"
		self.applause_file = self.resource + "applause.mp3"
		self.use_text = False

		# Size of cells
		self.icon_size = 25

		# Size of face bar
		self.face_size = 40

		# Icons of the application
		self.empty_icon  = QIcon()
		self.window_icon =  QIcon(self.resource + 'mine.png')
		self.flag_icon  = QIcon(self.resource +  'flag.png')
		self.mine_icon  = QIcon(self.resource + 'mine.png')
		self.sleeping_icon = QIcon(self.resource + 'zzz.png')
		self.thinking_icon = QIcon(self.resource +'thinking.png')
		self.dead_icon = QIcon(self.resource +  'dead.png')
		self.sunglasses_icon = QIcon(self.resource + 'sunglasses.png')

		self.app.setWindowIcon(self.window_icon)


	def loadTranslation(self):
		self.translator.load(self.translate + "es_ES.qm")
		self.app.installTranslator(self.translator)



