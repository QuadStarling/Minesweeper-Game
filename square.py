from enum import Enum


class SquareStatus(Enum):
    HIDDEN = 0
    PENDING = 1
    OPENED = 2


class MSSquare:
    def __init__(self):
        self.__has_mine = False
        self.__status = SquareStatus.HIDDEN
        self.__neighbor_mines = 0

    @property
    def has_mine(self):
        return self.__has_mine

    @property
    def status(self):
        return self.__status

    @property
    def neighbor_mines(self):
        return self.__neighbor_mines

    @has_mine.setter
    def has_mine(self, value):
        self.__has_mine = value

    @status.setter
    def status(self, value):
        self.__status = value

    @neighbor_mines.setter
    def neighbor_mines(self, value):
        self.__neighbor_mines = value
