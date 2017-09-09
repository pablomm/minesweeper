# -*- coding: utf-8 -*-
#
#	Minesweeper - Python implementation with PyQt4 of minesweeper game
#
#    Copyright (C) 2017
#        Pablo Marcos - pablo.marcosm@estudiante.uam.es
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
from struct import pack

def saveGame(filename, board, time,settings):


    with open(filename,'w') as f:
        f.write(saveBoard(board,settings))
        if not board.fake_start:
            f.write(saveCells(board))

def saveBoard(board,settings):

    time = board.parent.getTime()
    flags = 0
    flags |= board.fake_start
    flags |= (settings.started << 1)
    flags |= (settings.finished << 2)

    return pack('!IIIB',board.x,board.y, time,flags)

def saveCells(board):
    b = bytearray()
    w = 0
    k = 7
    for row in board.cells:
        for cell in row:
            for atr in [cell.opened, cell.marked, cell.bomb]:
                w |= (atr << k)
                k -= 1
                if k == -1:
                    k %= 8
                    b.append(w)
                    w = 0

    if k == 7:
        b.append(w)

    return b

