import tkinter as tk
from tkinter import ttk

from Difficulties import *


class BestTimes:
    def __init__(self, window):
        self.__scores = None
        self.__window = window
        self.__bestTimesWindow = None

    def setScores(self, name, time, difficulty):
        scores = self.getDataFromFile()

        if (difficulty == Difficulty.BEGINNER):
            scores[0] = f"{'Beginner:':<15} {str(time) + ' seconds':<14} {name}\n"

        elif (difficulty == Difficulty.INTERMEDIATE):
            scores[1] = f"{'Intermediate:':<15} {str(time) + ' seconds':<14} {name}\n"

        else:
            scores[2] = f"{'Expert:':<15} {str(time) + ' seconds':<14} {name}\n"

        self.writeDataToFile(scores)

    @staticmethod
    def getDataFromFile():
        file = open("Data/bestTimesData.txt", 'r')
        data = file.readlines()
        file.close()
        return data

    @staticmethod
    def writeDataToFile(Scores):
        with open("Data/bestTimesData.txt", 'w') as file:
            file.write("".join(Scores))

    def compare(self, difficulty, time):
        scores = self.getDataFromFile()

        if (difficulty == Difficulty.BEGINNER):
            if (int(scores[0].split()[1]) > time):
                return True
            else:
                return False

        elif (difficulty == Difficulty.INTERMEDIATE):
            if (int(scores[1].split()[1]) > time):
                return True
            else:
                return False
        else:
            if (int(scores[2].split()[1]) > time):
                return True
            else:
                return False

    def ResetScores(self):
        defaultScores = list()

        line1 = f"{'Beginner:':<15} {'999 seconds':<14} Anonymous\n"
        line2 = f"{'Intermediate:':<15} {'999 seconds':<14} Anonymous\n"
        line3 = f"{'Expert:':<15} {'999 seconds':<14} Anonymous\n"

        defaultScores.append(line1)
        defaultScores.append(line2)
        defaultScores.append(line3)

        self.writeDataToFile(defaultScores)
        self.__scores.config(text="".join(defaultScores))

    def displayBestTimes(self):
        self.__bestTimesWindow = tk.Toplevel(self.__window)
        _, _, win_coords = self.__window.geometry().partition('+')
        x_str, y_str = win_coords.split('+')
        x, y = int(x_str), int(y_str)
        self.__bestTimesWindow.geometry(f"325x125+{x+5}+{y+110}")
        self.__bestTimesWindow.resizable(False, False)
        self.__window.wm_attributes("-disabled", True)
        self.__bestTimesWindow.transient(self.__window)

        self.__bestTimesWindow.protocol("WM_DELETE_WINDOW", self.Close_TopLevel)

        self.__bestTimesWindow.title("Fastest Mine Sweepers")

        data = self.getDataFromFile()
        self.__scores = tk.Label(self.__bestTimesWindow, width=45, text="".join(data), anchor='w', justify="left", font=("Cascadia Mono", 9))
        self.__scores.pack(pady=(15, 0), padx=(20, 0))
        style = ttk.Style()
        style.configure("TButton", font=("Helvetica", 9))
        buttonsLabel = tk.Label(self.__bestTimesWindow)
        buttonsLabel.pack(pady=(0, 10))
        okButton = ttk.Button(buttonsLabel, text="OK", width=5, command=self.Close_TopLevel, takefocus=False)
        okButton.pack(side=tk.RIGHT, padx=(40, 0))

        resetScoresButton = ttk.Button(buttonsLabel, text="Reset Scores", command=self.ResetScores, takefocus=False)
        resetScoresButton.pack(side=tk.LEFT, padx=(0, 40))

    def Close_TopLevel(self):
        self.__window.wm_attributes("-disabled", False)

        self.__bestTimesWindow.destroy()