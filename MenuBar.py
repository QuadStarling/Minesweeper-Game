import sys
import tkinter as tk
from Difficulties import *


class MenuBar:

    def __init__(self, window, game):
        self.__window = window
        self.__game = game

        self.__menuBar = tk.Menu(self.__window)
        self.__window.config(menu=self.__menuBar)

        self.__x = tk.IntVar()
        self.__difficulties = [Difficulty.BEGINNER, Difficulty.INTERMEDIATE, Difficulty.EXPERT]

        self.__gameMenu = tk.Menu(self.__menuBar, tearoff=0, font=("Arial", 10))
        self.__menuBar.add_cascade(label="Game", menu=self.__gameMenu)
        self.__gameMenu.add_command(label="New Game", command=self.__game.resetGame)
        self.__gameMenu.add_separator()
        self.__gameMenu.add_radiobutton(label="Beginner", variable=self.__x, value=0, command=self.chooseDiff)
        self.__gameMenu.add_radiobutton(label="Intermediate", variable=self.__x, value=1, command=self.chooseDiff)
        self.__gameMenu.add_radiobutton(label="Expert", variable=self.__x, value=2, command=self.chooseDiff)
        self.__gameMenu.add_separator()
        self.__gameMenu.add_command(label="Exit", command=sys.exit)

        self.__game.Create_Game(*Difficulty.BEGINNER.value)  # Default Difficulty for when game starts first time

    def chooseDiff(self):
        if (self.__x.get() == 0):
            self.__game.Destroy()
            self.__game.Create_Game(*Difficulty.BEGINNER.value)
            self.__game.resetGame()
        elif (self.__x.get() == 1):
            self.__game.Destroy()
            self.__game.Create_Game(*Difficulty.INTERMEDIATE.value)
            self.__game.resetGame()
        elif (self.__x.get() == 2):
            self.__game.Destroy()
            self.__game.Create_Game(*Difficulty.EXPERT.value)
            self.__game.resetGame()