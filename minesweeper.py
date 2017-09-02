#!/usr/bin/env python


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

	MainWindow(settings).show()

	exit(app.exec_())

