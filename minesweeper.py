#!/usr/bin/env python
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
