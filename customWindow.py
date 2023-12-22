import tkinter as tk
from tkinter import ttk
import winsound
from Difficulties import *


class CustomWindow:
    def __init__(self, window, game):
        self.__window = window
        self.__game = game
        self.__custom_window = tk.Toplevel(window)
        self.__custom_window.title("Custom Field")

        _, _, win_coords = window.geometry().partition('+')
        x_str, y_str = win_coords.split('+')
        x, y = int(x_str), int(y_str)

        self.__custom_window.geometry(f"+{x + 25}+{y + 120}")
        frame = tk.Frame(self.__custom_window)
        frame.pack(pady=23, padx=12)

        Label = tk.Label(frame)
        Label.pack(side=tk.LEFT)

        buttonsLabel = tk.Label(frame)
        buttonsLabel.pack(padx=(10, 0), side=tk.RIGHT)

        heightLabel = tk.Label(Label, text="Height:")
        heightLabel.grid(row=0, column=0)
        widthLabel = tk.Label(Label, text="Width:")
        widthLabel.grid(row=1, column=0)
        minesLabel = tk.Label(Label, text="Mines:")
        minesLabel.grid(row=2, column=0)

        validate_cmd = self.__custom_window.register(self.on_validate)
        lst = self.getDifficulty()
        self.__heightEntry = ttk.Entry(Label, validate='key', validatecommand=(validate_cmd, '%P'), width=5)
        self.__heightEntry.grid(row=0, column=1, pady=2, padx=(10, 10))
        self.__heightEntry.insert(0, str(lst[1]))

        self.__widthEntry = ttk.Entry(Label, validate='key', validatecommand=(validate_cmd, '%P'), width=5)
        self.__widthEntry.grid(row=1, column=1, pady=2, padx=(10, 10))
        self.__widthEntry.insert(0, str(lst[0]))

        self.__minesEntry = ttk.Entry(Label, validate='key', validatecommand=(validate_cmd, '%P'), width=5)
        self.__minesEntry.grid(row=2, column=1, pady=2, padx=(10, 10))
        self.__minesEntry.insert(0, str(lst[2]))

        okButton = ttk.Button(buttonsLabel, text="OK", width=8, command=self.setDifficulty, takefocus=False)
        okButton.pack(pady=10)
        cancelButton = ttk.Button(buttonsLabel, text="Cancel", width=8, command=self.Close_TopLevel, takefocus=False)
        cancelButton.pack(pady=10)

        self.__custom_window.resizable(False, False)
        window.wm_attributes("-disabled", True)
        self.__custom_window.transient(window)
        self.__custom_window.protocol("WM_DELETE_WINDOW", self.Close_TopLevel)

    @staticmethod
    def on_validate(P):
        if len(P) > 5:
            winsound.MessageBeep(1000)
        return len(P) <= 5

    def getEntryVars(self):
        height = int(self.__heightEntry.get())
        width = int(self.__widthEntry.get())
        mines = int(self.__minesEntry.get())

        return [min(max(width, 9), 30), min(max(height, 9), 24),
                min(max(mines, 1), width * height - 1)]

    def writeDifficultyToFile(self):
        EntryValList = self.getEntryVars()
        with open("Data/customDifficulty.txt", 'w') as file:
            file.write(str(EntryValList[0]) + ',' + str(EntryValList[1]) + ',' + str(EntryValList[2]))

        self.Close_TopLevel()

    def Close_TopLevel(self):
        self.__window.wm_attributes("-disabled", False)
        self.__custom_window.destroy()
        self.__game.resetGame()
        self.__game.Difficulty = Difficulty.Custom

    @staticmethod
    def getDifficulty():
        with open("Data/customDifficulty.txt", 'r') as file:
            data = file.read()
            diffList = [int(item) for item in data.split(',')]
        return diffList

    def setDifficulty(self):
        customDiffLst = self.getEntryVars()
        currDiff = self.__game.Difficulty

        if customDiffLst != currDiff:
            self.writeDifficultyToFile()
            self.__game.Destroy()
            self.__game.Create_Game(*customDiffLst, Difficulty.Custom)
        self.__game.Difficulty = Difficulty.Custom

        self.Close_TopLevel()
