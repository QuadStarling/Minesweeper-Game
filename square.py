from enum import Enum


class SquareStatus(Enum):
    HIDDEN = 0
    PENDING = 1
    OPENED = 2


class FlagStatus(Enum):
    ON = 0
    OFF = 1


class MSSquare:
    def __init__(self):
        self.__has_mine = False
        self.__status = SquareStatus.HIDDEN
        self.__neighbor_mines = 0
        self.__flagState = FlagStatus.OFF

    @property
    def has_mine(self):
        return self.__has_mine

    @property
    def status(self):
        return self.__status

    @property
    def neighbor_mines(self):
        return self.__neighbor_mines

    @property
    def flagState(self):
        return self.__flagState

    @has_mine.setter
    def has_mine(self, value):
        self.__has_mine = value

    @status.setter
    def status(self, value):
        self.__status = value

    @neighbor_mines.setter
    def neighbor_mines(self, value):
        self.__neighbor_mines = value

    @flagState.setter
    def flagState(self, value):
        self.__flagState = value
