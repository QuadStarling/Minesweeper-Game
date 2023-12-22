import tkinter as tk

import winsound

from MSGame import *
from enum import Enum
from BestTimes import *
from pygame import mixer

import threading
import time


class FirstSafeClick(Enum):
    ACTIVE = 0
    INACTIVE = 1


class Game:
    def __init__(self, window):
        self.__bestTimes = None
        self.__id = None
        self.__window = window
        self.__game_frame = None
        self.__canvas = None
        self.__stats_frame = None
        self.__window.columnconfigure(0, weight=1)
        self.__coverFrame = None  # Covers the game frame to block the player from clicking the buttons
        self.__FocusCoverFrame = None  # Used when you focus out of the game and in
        self.__coverButtonFrame = None  # Covers the resetButton when the window is out of focus

        self.__tiles_list = None  # A list to store buttons
        self.__game = None
        self.__resetButton = None  # A button that resets the game
        self.__resButtCurrImage = None  # Stores the current image of the reset image

        self.__squareCounter = 0  # Counts how many squares have been opened up that are not mines
        self.__counter_label = None

        self.__flagsLeft = 0
        self.__flagsLeft_label = None
        self.__flagImage = tk.PhotoImage(file="Images/flag.gif")

        self.__smileyPics = [tk.PhotoImage(file="Images/smileyNormal.gif"), tk.PhotoImage(file="Images/smileyNervous.gif"), tk.PhotoImage(file="Images/smileyDead.gif"), tk.PhotoImage(file="Images/smileyCool.gif")]
        self.__minesPics = [tk.PhotoImage(file="Images/mine.gif"), tk.PhotoImage(file="Images/notMine.gif")]
        self.__numberPics = [tk.PhotoImage(file=f"Images/tile_{n}.gif") for n in range(1, 9)]

        self.__time_counter = 0  # A Counter for how many seconds passed since the start of the game
        self.__firstSafeClick = FirstSafeClick.ACTIVE  # Makes sure that the first click is not a mine

        self.__currButton = None
        self.__gameDifficulty = None

        self.__prevWindowState = None

        # Initialize the mixer
        mixer.init()
        self.__soundOnOff = 0  # When the variable is 0 it means the sound is off

    def Create_Game(self, width, height, mines, difficulty):
        self.__gameDifficulty = difficulty
        with open("Data/saveLastDifficulty.txt", 'w') as file:
            file.write(difficulty.name)

        # The frame contains the canvas inside it
        self.__game_frame = tk.Frame(self.__window)
        self.__game_frame.grid(row=1, column=0)

        self.__canvas = tk.Canvas(self.__game_frame, width=width*26 + 1, height=height*26 + 1, relief=tk.SUNKEN, bd=10)
        self.__canvas.pack()

        self.__stats_frame = tk.Frame(self.__window, bd=10, relief=tk.SUNKEN)
        self.__stats_frame.grid(row=0, column=0, sticky="wens")

        self.__coverFrame = tk.Frame(self.__window, bg='')
        self.__FocusCoverFrame = tk.Frame(self.__window, bg='')
        self.__coverButtonFrame = tk.Frame(self.__window, bg='')

        self.__counter_label = tk.Label(self.__stats_frame, bg="black", fg="red", text=f"{self.__time_counter:03}", font=("Arial", 18), width=3, relief=tk.SUNKEN, bd=3)
        self.__counter_label.pack(side=tk.RIGHT, padx=(0, 10))

        self.__flagsLeft = mines
        self.__flagsLeft_label = tk.Label(self.__stats_frame, bg="black", fg="red", text=f"{min(self.__flagsLeft, 999):03}", font=("Arial", 18), width=3, relief=tk.SUNKEN, bd=3)
        self.__flagsLeft_label.pack(side=tk.LEFT, padx=(10, 0))

        self.__resetButton = tk.Button(self.__stats_frame, image=self.__smileyPics[0])
        self.__resetButton.pack(pady=10)
        self.__resetButton.bind("<Button-1>", self.holdingResetButton)
        self.__resetButton.bind("<B1-Motion>", self.holdingResetButtonMotion)
        self.__resetButton.bind("<ButtonRelease-1>", self.handle_button_click)

        self.__game = MSGame(width, height, mines)

        # Create a 2D array to store rectangle IDs
        self.__tiles_list = [[] for _ in range(height)]

        self.__window.bind("<FocusOut>", self.focusOut)
        self.__window.bind("<FocusIn>", self.focusIn)

        # Bind mouse events to the Canvas
        self.__canvas.bind("<Button-1>", self.holdingClick)
        self.__canvas.bind("<B1-Motion>", self.holdingMotion)
        self.__canvas.bind("<ButtonRelease-1>", self.show)
        self.__canvas.bind("<Button-3>", self.place_flag)

        for i in range(height):
            for j in range(width):
                x1, y1 = j * 26 + 12, i * 26 + 12
                x2, y2 = x1 + 26, y1 + 26
                rect_id = self.__canvas.create_rectangle(x1, y1, x2, y2, fill="lightgray", outline="black")
                self.__tiles_list[i].append(rect_id)

    def handle_button_click(self, event):
        widget = self.__window.winfo_containing(event.x_root, event.y_root)
        if isinstance(widget, tk.Button):
            self.resetGame()

        elif self.__firstSafeClick == FirstSafeClick.INACTIVE:
            self.update_counter()

    def holdingResetButton(self, event):
        self.__resButtCurrImage = self.__resetButton['image']
        self.__resetButton.config(image=self.__smileyPics[0])
        if self.__id is not None:
            self.__window.after_cancel(self.__id)
        self.__id = None

    def holdingResetButtonMotion(self, event):
        widget = self.__window.winfo_containing(event.x_root, event.y_root)
        if not isinstance(widget, tk.Button):
            self.__resetButton.config(image=self.__resButtCurrImage)
        else:
            self.__resetButton.config(image=self.__smileyPics[0])

    def add_cover(self):
        time.sleep(0.1)
        self.__coverFrame.grid(row=1, column=0, sticky="nsew")

    def focusOut(self, event):
        # Adds a cover after you minimised and then maximised the game
        if self.__window.state() == "iconic":
            self.__coverFrame.grid_forget()
        elif self.__prevWindowState == "iconic":
            threading.Thread(target=self.add_cover).start()  # used threading to solve the cover frame bug not being transparent after you maximise the game

        self.__FocusCoverFrame.grid(row=1, column=0, sticky="news")
        self.__coverButtonFrame.place(in_=self.__resetButton, relwidth=1, relheight=1)
        self.__prevWindowState = self.__window.state()

    def focusIn(self, event):
        self.__FocusCoverFrame.grid_forget()
        self.__coverButtonFrame.place_forget()

    @property
    def Difficulty(self):
        value = self.__gameDifficulty.value
        if value is not None:
            return value

        with open("Data/customDifficulty.txt", 'r') as file:
            data = file.read()

        return [int(item) for item in data.split(',')]

    @Difficulty.setter
    def Difficulty(self, value):
        self.__gameDifficulty = value

    def setSound_Toggle(self, value):
        if value == 0:
            mixer.music.stop()
        self.__soundOnOff = value

    @staticmethod
    def getRowAndColumn(event):
        return (event.y - 12) // 26, (event.x - 12) // 26

    def get_coordinates(self, button):
        coordinates = self.__canvas.coords(button)
        x, y = coordinates[0], coordinates[1]
        return round(x), round(y)

    def update_counter(self):
        if self.__soundOnOff == 1:
            mixer.music.play()
        self.__time_counter += 1
        self.__counter_label.config(text=f"{min(self.__time_counter, 999):03}")
        self.__id = self.__window.after(1000, self.update_counter)

    def resetGame(self):
        self.__resetButton.config(image=self.__smileyPics[0])

        self.__coverFrame.grid_forget()
        self.__game.clear_board()
        self.__firstSafeClick = FirstSafeClick.ACTIVE
        self.__squareCounter = 0

        # stops and resets the timer
        self.__time_counter = 0
        self.__counter_label.config(text=f"{self.__time_counter:03}")
        mixer.music.stop()

        if self.__id is not None:
            self.__window.after_cancel(self.__id)
        self.__id = None

        # Reset how many flag left
        self.__flagsLeft = self.__game.mines
        self.__flagsLeft_label.config(text=f"{self.__flagsLeft:03}")

        for i in range(self.__game.height):
            for j in range(self.__game.width):
                if self.__game.get_board()[i][j].flagState == FlagStatus.ON:
                    self.__game.get_board()[i][j].flagState = FlagStatus.OFF
                    self.__canvas.itemconfig(self.__tiles_list[i][j], fill="lightgray")
                    self.__canvas.delete(f"flag_image{i},{j}")

                elif self.__game.get_board()[i][j].status == SquareStatus.OPENED:
                    self.__game.get_board()[i][j].status = SquareStatus.HIDDEN
                    self.__canvas.itemconfig(self.__tiles_list[i][j], fill="lightgray")
                    self.__canvas.delete(f"image{i},{j}")

    def holdingClick(self, event):
        self.__resetButton.config(image=self.__smileyPics[1])

        # Check if the mouse is outside the board
        if event.x < 12 or event.x >= self.__canvas.winfo_reqwidth() - 13 or event.y < 12 or event.y >= self.__canvas.winfo_reqheight() - 13:
            return

        row, col = self.getRowAndColumn(event)  # Get row and column for the button clicked
        button = self.__tiles_list[row][col]
        self.__currButton = button
        if self.__game.get_board()[row][col].flagState == FlagStatus.OFF:
            self.__canvas.itemconfig(button, fill="white")

    def holdingMotion(self, event):
        row, col = None, None

        if self.__currButton is not None:
            x2, y2 = self.get_coordinates(self.__currButton)
            row, col = (y2 - 12) // 26, (x2 - 12) // 26

        # Check if the mouse is outside the board
        if event.x < 12 or event.x >= self.__canvas.winfo_reqwidth()-13 or event.y < 12 or event.y >= self.__canvas.winfo_reqheight() - 13:
            if self.__currButton is not None and self.__game.get_board()[row][col].status == SquareStatus.HIDDEN and self.__game.get_board()[row][col].flagState == FlagStatus.OFF:
                self.__canvas.itemconfig(self.__currButton, fill="lightgray")
                self.__currButton = None
            return

        x, y = self.getRowAndColumn(event)  # Get row and column for the button clicked
        button = self.__tiles_list[x][y]

        if self.__currButton == button:
            return

        if self.__currButton is not None:
            if self.__game.get_board()[row][col].status == SquareStatus.HIDDEN and self.__game.get_board()[row][col].flagState == FlagStatus.OFF:
                self.__canvas.itemconfig(self.__currButton, fill="lightgray")

        if self.__game.get_board()[x][y].flagState == FlagStatus.OFF:
            self.__canvas.itemconfig(button, fill="white")
        self.__currButton = button

    def show(self, event):
        self.__resetButton.config(image=self.__smileyPics[0])

        if self.__currButton is None:
            return

        row, column = self.getRowAndColumn(event)
        self.__currButton = None
        if (
            row < 0 or
            column < 0 or
            row >= self.__game.height or
            column >= self.__game.width or
            self.__game.get_board()[row][column].status == SquareStatus.OPENED or
            self.__game.get_board()[row][column].flagState == FlagStatus.ON
        ):
            return

        if self.__firstSafeClick == FirstSafeClick.ACTIVE:
            self.__game.generate_minefield(row, column)
            self.__game.generate_neighbor_info()
            mixer.music.load("Sounds/Tick.mp3")
            self.update_counter()
            self.__firstSafeClick = FirstSafeClick.INACTIVE

        if self.__game.get_board()[row][column].has_mine:
            self.__firstSafeClick = FirstSafeClick.ACTIVE
            mixer.music.load("Sounds/Lose.mp3")
            if self.__soundOnOff == 1:
                mixer.music.play()

            self.__canvas.itemconfig(self.__tiles_list[row][column], fill="red")
            x, y = self.get_coordinates(self.__tiles_list[row][column])
            self.__canvas.create_image(x + 13, y + 13, image=self.__minesPics[0], tags=f"image{row},{column}")
            self.__window.after_cancel(self.__id)
            for i in range(self.__game.height):
                for j in range(self.__game.width):
                    if i == row and j == column:
                        continue

                    x, y = self.get_coordinates(self.__tiles_list[i][j])
                    if self.__game.get_board()[i][j].has_mine is True and self.__game.get_board()[i][j].flagState == FlagStatus.OFF:
                        self.__canvas.itemconfig(self.__tiles_list[i][j], fill="white")
                        self.__canvas.create_image(x + 13, y + 13, image=self.__minesPics[0], tags=f"image{i},{j}")
                        self.__game.get_board()[i][j].status = SquareStatus.OPENED

                    elif self.__game.get_board()[i][j].has_mine is False and self.__game.get_board()[i][j].flagState == FlagStatus.ON:
                        self.__canvas.delete(f"flag_image{i},{j}")
                        self.__game.get_board()[i][j].flagState = FlagStatus.OFF
                        self.__game.get_board()[i][j].status = SquareStatus.OPENED
                        self.__canvas.create_image(x + 13, y + 13, image=self.__minesPics[1], tags=f"image{i},{j}")

            self.__game.get_board()[row][column].status = SquareStatus.OPENED
            self.__resetButton.config(image=self.__smileyPics[2])
            self.__coverFrame.grid(row=1, column=0, sticky="nsew")
            return

        self.__game.update_board(row, column)
        for i in range(self.__game.height):
            for j in range(self.__game.width):
                if self.__game.get_board()[i][j].status == SquareStatus.PENDING:
                    self.__game.get_board()[i][j].status = SquareStatus.OPENED
                    if self.__game.get_board()[i][j].neighbor_mines == 0:
                        self.__squareCounter += 1
                        self.__canvas.itemconfig(self.__tiles_list[i][j], fill="white")
                    else:
                        self.__squareCounter += 1
                        self.__canvas.itemconfig(self.__tiles_list[i][j], fill="white")
                        x, y = self.get_coordinates(self.__tiles_list[i][j])
                        self.__canvas.create_image(x + 13, y + 13, image=self.__numberPics[self.__game.get_board()[i][j].neighbor_mines - 1], tags=f"image{i},{j}")

                    if self.__squareCounter == (self.__game.height * self.__game.width) - self.__game.mines:
                        self.youWin()
                        return

    def youWin(self):
        self.__firstSafeClick = FirstSafeClick.ACTIVE
        mixer.music.load("Sounds/Win.mp3")
        if self.__soundOnOff == 1:
            mixer.music.play()

        self.__resetButton.config(image=self.__smileyPics[3])
        self.__window.after_cancel(self.__id)
        for r in range(self.__game.height):
            for c in range(self.__game.width):
                if self.__game.get_board()[r][c].has_mine is True and self.__game.get_board()[r][c].flagState == FlagStatus.OFF:
                    x, y = self.get_coordinates(self.__tiles_list[r][c])
                    self.__canvas.create_image(x + 13, y + 13, image=self.__flagImage, tags=f"flag_image{r},{c}")
                    self.__game.get_board()[r][c].flagState = FlagStatus.ON
                    self.__flagsLeft -= 1
                    self.__flagsLeft_label.config(text=f"{max(self.__flagsLeft, -99):03}")

        self.__coverFrame.grid(row=1, column=0, sticky="nsew")  # Prevents the player from the clicking the game

        self.__bestTimes = BestTimes(self.__window)
        if self.__bestTimes.compare(self.__gameDifficulty, self.__time_counter) and self.__gameDifficulty != Difficulty.Custom:
            newBestTimeWindow = tk.Toplevel(self.__window, relief=tk.RAISED, bd=2)
            newBestTimeWindow.attributes("-topmost", True)
            newBestTimeWindow.overrideredirect(True)
            self.__window.wm_attributes("-disabled", True)

            # Get window coordinates
            geo, _, win_coords = self.__window.geometry().partition('+')
            x_str, y_str = win_coords.split('+')
            x, y = int(x_str), int(y_str)

            w, _, h = geo.partition('x')
            wid, hei = int(w)//2 - 75, int(h)//2 - 25
            newBestTimeWindow.geometry(f"+{x+wid}+{y+hei}")
            label = tk.Label(newBestTimeWindow)
            label.pack(pady=5, padx=15)

            if self.__gameDifficulty == Difficulty.BEGINNER:
                label.config(text="You have the fastest time\n  for beginner level.\nPlease enter your name.")
            elif self.__gameDifficulty == Difficulty.INTERMEDIATE:
                label.config(text="You have the fastest time\n  for intermediate level.\nPlease enter your name.")
            else:
                label.config(text="You have the fastest time\n  for expert level.\nPlease enter your name.")

            # Register the validation function
            validate_cmd = newBestTimeWindow.register(self.on_validate)

            # Create an Entry widget with character limit
            entry = ttk.Entry(newBestTimeWindow, validate="key", validatecommand=(validate_cmd, "%P"), width=20)
            entry.pack(pady=(40, 5))

            okButton = ttk.Button(newBestTimeWindow, text="OK", width=7, padding=2, command=lambda: self.Close_TopLevel(newBestTimeWindow, entry))
            okButton.pack(pady=(5, 22))

    @staticmethod
    def on_validate(P):
        if len(P) > 18:
            winsound.MessageBeep(1000)
        # P is the value of the entry at the moment of validation
        return len(P) <= 18

    def Close_TopLevel(self, w, entry):
        name = entry.get()
        self.__window.wm_attributes("-disabled", False)
        w.destroy()
        self.__bestTimes.setScores(name, self.__time_counter, self.__gameDifficulty)
        self.__bestTimes.displayBestTimes()
        self.__window.unbind("<Button-1>")

    def place_flag(self, event):
        # Check if the mouse is outside the board
        if event.x < 12 or event.x >= self.__canvas.winfo_reqwidth() - 13 or event.y < 12 or event.y >= self.__canvas.winfo_reqheight() - 13:
            return

        row, col = self.getRowAndColumn(event)
        if self.__game.get_board()[row][col].status == SquareStatus.HIDDEN:
            if self.__game.get_board()[row][col].flagState == FlagStatus.ON:
                self.__canvas.delete(f"flag_image{row},{col}")
                self.__game.get_board()[row][col].flagState = FlagStatus.OFF
                self.__flagsLeft += 1
                self.__flagsLeft_label.config(text=f"{self.__flagsLeft:03}")
            else:
                x, y = self.get_coordinates(self.__tiles_list[row][col])
                self.__canvas.create_image(x + 13, y + 13, image=self.__flagImage, tags=f"flag_image{row},{col}")
                self.__game.get_board()[row][col].flagState = FlagStatus.ON
                self.__flagsLeft -= 1
                self.__flagsLeft_label.config(text=f"{max(self.__flagsLeft, -99):03}")

    def Destroy(self):
        self.__game_frame.grid_forget()
        self.__game_frame.destroy()

        self.__stats_frame.grid_forget()
        self.__stats_frame.destroy()

        self.__coverFrame.grid_forget()
        self.__coverFrame.destroy()
