#!/usr/bin/env python


from signal import signal, SIGINT, SIG_DFL
from sys import argv, exit

from PyQt4.QtGui import QApplication

from minesweeper.mainwindow import MainWindow
from minesweeper.settings import Settings

if __name__ == '__main__':


	signal(SIGINT, SIG_DFL)

	app = QApplication(argv)
	settings = Settings(app)

	MainWindow(settings).show()

	exit(app.exec_())

