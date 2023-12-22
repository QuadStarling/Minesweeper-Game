import sys
from tkinter import messagebox
from BestTimes import *
from customWindow import *


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
        self.__gameMenu.add_radiobutton(label="Custom...", variable=self.__x, value=3, command=self.chooseDiff)
        self.__gameMenu.add_separator()

        self.__gameMenu.add_checkbutton(label="Sound", variable=self.__soundOnOff, onvalue=1, offvalue=0, command=self.toggle_sound)
        self.__gameMenu.add_separator()

        self.__gameMenu.add_command(label="Best Times...", command=self.show_Scores)
        self.__gameMenu.add_separator()

        self.__gameMenu.add_command(label="Exit", command=sys.exit)

        with open("Data/saveLastDifficulty.txt", 'r') as file:
            self.__diff = file.read()

        with open("Data/SoundToggleSave.txt", 'r') as file:
            sound = file.read()

        # Default Difficulty for when game starts first time
        if self.__diff == "BEGINNER":
            self.__game.Create_Game(*Difficulty.BEGINNER.value,
                                    Difficulty.BEGINNER)
            with open("Data/customDifficulty.txt", 'w') as file:
                file.write("9,9,10")
        elif self.__diff == "INTERMEDIATE":
            self.__x.set(1)
            self.__game.Create_Game(*Difficulty.INTERMEDIATE.value,
                                    Difficulty.INTERMEDIATE)
            with open("Data/customDifficulty.txt", 'w') as file:
                file.write("16,16,40")
        elif self.__diff == "EXPERT":
            self.__x.set(2)
            self.__game.Create_Game(*Difficulty.EXPERT.value,
                                    Difficulty.EXPERT)
            with open("Data/customDifficulty.txt", 'w') as file:
                file.write("30,16,99")
        else:
            self.__x.set(3)
            with open("Data/customDifficulty.txt", 'r') as file:
                data = file.read()
                diffList = [int(item) for item in data.split(',')]
            self.__game.Create_Game(*diffList, Difficulty.Custom)

        self.__soundOnOff.set(int(sound))
        self.toggle_sound()

        self.__helpMenu = tk.Menu(self.__menuBar, tearoff=0, font=("Arial", 10))
        self.__menuBar.add_cascade(label="Help", menu=self.__helpMenu)
        self.__helpMenu.add_command(label="How to Play", command=lambda: MenuBar.show_help('How to Play'))
        self.__helpMenu.add_separator()
        self.__helpMenu.add_command(label="About Minesweeper...",
                                    command=lambda: MenuBar.show_help('About Minesweeper'))

    def chooseDiff(self):
        if self.__x.get() != 3:
            self.__game.resetGame()

        if self.__x.get() == 0 and Difficulty.BEGINNER.name != self.__diff:
            with open("Data/saveLastDifficulty.txt", 'w') as file:
                file.write("BEGINNER")
            self.__game.Destroy()
            self.__game.Create_Game(*Difficulty.BEGINNER.value, Difficulty.BEGINNER)

            with open("Data/customDifficulty.txt", 'w') as file:
                file.write("9,9,10")

            self.__diff = "BEGINNER"

        elif self.__x.get() == 1 and Difficulty.INTERMEDIATE.name != self.__diff:
            with open("Data/saveLastDifficulty.txt", 'w') as file:
                file.write("INTERMEDIATE")
            self.__game.Destroy()
            self.__game.Create_Game(*Difficulty.INTERMEDIATE.value, Difficulty.INTERMEDIATE)
            with open("Data/customDifficulty.txt", 'w') as file:
                file.write("16,16,40")

            self.__diff = "INTERMEDIATE"

        elif self.__x.get() == 2 and Difficulty.EXPERT.name != self.__diff:
            with open("Data/saveLastDifficulty.txt", 'w') as file:
                file.write("EXPERT")
            self.__game.Destroy()
            self.__game.Create_Game(*Difficulty.EXPERT.value, Difficulty.EXPERT)
            with open("Data/customDifficulty.txt", 'w') as file:
                file.write("30,16,99")

            self.__diff = "EXPERT"

        elif self.__x.get() == 3:
            with open("Data/saveLastDifficulty.txt", 'w') as file:
                file.write("Custom")
            CustomWindow(self.__window, self.__game)
            self.__diff = "Custom"

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
        SoundVar = self.__soundOnOff.get()
        with open("Data/SoundToggleSave.txt", 'w') as file:
            file.write(str(SoundVar))
        self.__game.setSound_Toggle(SoundVar)
