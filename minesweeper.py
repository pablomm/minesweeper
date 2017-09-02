#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import chdir, path
from signal import signal, SIGINT, SIG_DFL
from sys import argv, exit

from PyQt4.QtGui import QApplication

from minesweeper.mainwindow import MainWindow
from minesweeper.settings import Settings

if __name__ == '__main__':


	chdir(path.dirname(path.abspath(__file__)))
	signal(SIGINT, SIG_DFL)

	app = QApplication(argv)
	settings = Settings(app)

	window = MainWindow(settings)
	window.show()
	window.setWindowTitle(window.tr('Minesweeper'))

	exit(app.exec_())

