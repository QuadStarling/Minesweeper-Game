import sys
from tkinter import messagebox
from BestTimes import *
import tkinter as tk
from tkinter import ttk


class MenuBar:

    def __init__(self, window, game):
        self.__window = window
        self.__game = game
        self.__menuBar = tk.Menu(window)
        self.__window.config(menu=self.__menuBar)

        self.__x = tk.IntVar()
        self.__soundOnOff = tk.IntVar()

        self.__gameMenu = tk.Menu(self.__menuBar, tearoff=0, font=("Arial", 10))
        self.__menuBar.add_cascade(label="Game", menu=self.__gameMenu)
        self.__gameMenu.add_command(label="New Game", command=self.__game.resetGame)
        self.__gameMenu.add_separator()

        self.__gameMenu.add_radiobutton(label="Beginner", variable=self.__x, value=0, command=self.chooseDiff)
        self.__gameMenu.add_radiobutton(label="Intermediate", variable=self.__x, value=1, command=self.chooseDiff)
        self.__gameMenu.add_radiobutton(label="Expert", variable=self.__x, value=2, command=self.chooseDiff)
        self.__gameMenu.add_separator()

        self.__gameMenu.add_checkbutton(label="Sound", variable=self.__soundOnOff, onvalue=1, offvalue=0, command=self.toggle_sound)
        self.__gameMenu.add_separator()

        self.__gameMenu.add_command(label="Best Times...", command=self.show_Scores)
        self.__gameMenu.add_separator()

        self.__gameMenu.add_command(label="Exit", command=sys.exit)

        self.__game.Create_Game(*Difficulty.BEGINNER.value,
                                Difficulty.BEGINNER)  # Default Difficulty for when game starts first time

        self.__helpMenu = tk.Menu(self.__menuBar, tearoff=0, font=("Arial", 10))
        self.__menuBar.add_cascade(label="Help", menu=self.__helpMenu)
        self.__helpMenu.add_command(label="How to Play", command=lambda: MenuBar.show_help('How to Play'))
        self.__helpMenu.add_separator()
        self.__helpMenu.add_command(label="About Minesweeper...",
                                    command=lambda: MenuBar.show_help('About Minesweeper'))

    def chooseDiff(self):
        if (self.__x.get() == 0):
            self.__game.Destroy()
            self.__game.Create_Game(*Difficulty.BEGINNER.value, Difficulty.BEGINNER)
            self.__game.resetGame()

        elif (self.__x.get() == 1):
            self.__game.Destroy()
            self.__game.Create_Game(*Difficulty.INTERMEDIATE.value, Difficulty.INTERMEDIATE)
            self.__game.resetGame()

        else:
            self.__game.Destroy()
            self.__game.Create_Game(*Difficulty.EXPERT.value, Difficulty.EXPERT)
            self.__game.resetGame()

    @staticmethod
    def show_help(help_type):
        help_text = ""
        if help_type == "How to Play":
            with open("Data/How_to_Play.txt", 'r') as file:
                help_text = file.read()

        elif help_type == "About Minesweeper":
            with open("Data/AboutMS.txt", 'r') as file:
                help_text = file.read()

        tk.messagebox.showinfo(help_type, help_text)

    def show_Scores(self):
        bestTimes = BestTimes(self.__window)
        bestTimes.displayBestTimes()

    def toggle_sound(self):
        self.__game.setSound_Toggle(self.__soundOnOff.get())
