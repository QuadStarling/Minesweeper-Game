import tkinter as tk
from MSGame import *
from enum import Enum
from BestTimes import *


class FirstSafeClick(Enum):
    ACTIVE = 0
    INACTIVE = 1


class Game:
    def __init__(self, window):
        self.__bestTimes = None
        self.__id = None
        self.__window = window
        self.__game_frame = None
        self.__stats_frame = None
        self.__window.columnconfigure(0, weight=1)
        self.__coverFrame = None  # Covers the game frame to block the player from clicking the buttons
        self.__coverButtonFrame = None

        self.__buttons_list = None  # A list to store buttons
        self.__game = None
        self.__resetButton = None  # A button that resets the game

        self.__squareCounter = 0  # Counts how many squares have been opened up that are not mines
        self.__counter_label = None

        self.__flagsLeft = 0
        self.__flagsLeft_label = None
        self.__flagImage = tk.PhotoImage(file="Images/flag.gif")
        self.__pixel = None

        self.__smileyPics = [tk.PhotoImage(file="Images/smileyNormal.gif"), tk.PhotoImage(file="Images/smileyNervous.gif"), tk.PhotoImage(file="Images/smileyDead.gif"), tk.PhotoImage(file="Images/smileyCool.gif")]
        self.__minesPics = [tk.PhotoImage(file="Images/mine.gif"), tk.PhotoImage(file="Images/notMine.gif")]
        self.__numberPics = [tk.PhotoImage(file=f"Images/tile_{n}.gif") for n in range(1, 9)]

        self.__time_counter = 0  # A Counter for how many seconds passed since the start of the game
        self.__firstSafeClick = FirstSafeClick.ACTIVE  # Makes sure that the first click is not a mine

        self.__currButton = None
        self.__gameDifficulty = None

    def Create_Game(self, width, height, mines, difficulty):
        self.__gameDifficulty = difficulty

        self.__game_frame = tk.Frame(self.__window, bg="black", relief=tk.SUNKEN)
        self.__game_frame.grid(row=1, column=0)

        self.__stats_frame = tk.Frame(self.__window)
        self.__stats_frame.grid(row=0, column=0, sticky="wens")

        self.__coverFrame = tk.Frame(self.__window, bg='')

        self.__counter_label = tk.Label(self.__stats_frame, bg="black", fg="red", text=f"{self.__time_counter:03}", font=("Arial", 18), width=3)
        self.__counter_label.pack(side=tk.RIGHT, padx=(0, 10))

        self.__flagsLeft = mines
        self.__flagsLeft_label = tk.Label(self.__stats_frame, bg="black", fg="red", text=f"{min(self.__flagsLeft, 999):03}", font=("Arial", 18), width=3)
        self.__flagsLeft_label.pack(side=tk.LEFT, padx=(10, 0))

        self.__resetButton = tk.Button(self.__stats_frame, image=self.__smileyPics[0])
        self.__resetButton.pack(pady=10)
        self.__resetButton.bind("<Button-1>", lambda event: self.__resetButton.config(image=self.__smileyPics[0]))
        self.__resetButton.bind("<ButtonRelease-1>", lambda event: self.resetGame())

        self.__game = MSGame(width, height, mines)
        squares = (width * height)
        self.__buttons_list = [[] for _ in range(height)]
        self.__pixel = tk.PhotoImage(width=1, height=1)

        # places and creates the buttons on the frame
        # while also storing them in the list
        for i in range(squares):
            button = tk.Label(self.__game_frame, image=self.__pixel, bg="lightgray", width=20, height=20, relief=tk.FLAT)
            button.bind("<Button-1>", self.holdingClick)
            button.bind("<B1-Motion>", self.holdingMotion)
            button.bind("<ButtonRelease-1>", self.show)
            button.bind("<Button-3>", self.place_flag)
            self.__buttons_list[i // max(height, width)].append(button)

        for i, row_buttons in enumerate(self.__buttons_list):
            for j, button in enumerate(row_buttons):
                button.grid(row=i, column=j, pady=1, padx=1)

    def update_counter(self):
        self.__time_counter += 1
        self.__counter_label.config(text=f"{min(self.__time_counter, 999):03}")
        self.__id = self.__window.after(1000, self.update_counter)

    def resetGame(self):
        self.__coverFrame.grid_forget()
        self.__game.clear_board()
        self.__firstSafeClick = FirstSafeClick.ACTIVE
        self.__squareCounter = 0

        # stops and resets the timer
        self.__time_counter = 0
        self.__counter_label.config(text=f"{self.__time_counter:03}")
        if (self.__id is not None):
            self.__window.after_cancel(self.__id)
        self.__id = None

        # Reset how many flag left
        self.__flagsLeft = self.__game.mines
        self.__flagsLeft_label.config(text=f"{self.__flagsLeft:03}")

        for i in range(self.__game.height):
            for j in range(self.__game.width):
                if (self.__game.get_board()[i][j].flagState == FlagStatus.ON):
                    self.__game.get_board()[i][j].flagState = FlagStatus.OFF
                    self.__buttons_list[i][j].bind("<ButtonRelease-1>",
                                                   lambda e, btn=self.__buttons_list[i][j]: self.show(btn))
                    self.__buttons_list[i][j].config(bg="lightgray", image=self.__pixel, bd=2, width=20, height=20, relief=tk.FLAT)

                if (self.__game.get_board()[i][j].status == SquareStatus.OPENED):
                    self.__game.get_board()[i][j].status = SquareStatus.HIDDEN
                    self.__buttons_list[i][j].config(bg="lightgray", image=self.__pixel, bd=2, width=20, height=20, relief=tk.FLAT)

    def holdingClick(self, event):
        self.__resetButton.config(image=self.__smileyPics[1])
        self.__currButton = event.widget
        row = self.__currButton.grid_info()['row']
        col = self.__currButton.grid_info()['column']

        if (self.__game.get_board()[row][col].flagState == FlagStatus.OFF):
            self.__currButton.config(background="white")

    def holdingMotion(self, event):
        row, col = None, None
        x, y = event.x_root, event.y_root
        button = self.__window.winfo_containing(x, y)

        if (self.__currButton != None):
            row = self.__currButton.grid_info()['row']
            col = self.__currButton.grid_info()['column']

        # Get the coordinates of the frame
        frame_x, frame_y, frame_width, frame_height = self.__game_frame.winfo_rootx(), self.__game_frame.winfo_rooty(), self.__game_frame.winfo_width(), self.__game_frame.winfo_height()

        # Check if the mouse is outside the frame
        if (x < frame_x or x > frame_x + frame_width or y < frame_y or y > frame_y + frame_height):
            if (self.__currButton != None and self.__game.get_board()[row][col].status == SquareStatus.HIDDEN and self.__game.get_board()[row][col].flagState == FlagStatus.OFF):
                self.__currButton.config(bg="lightgray", image=self.__pixel, bd=2, width=20, height=20, relief=tk.FLAT)
                self.__currButton = None
            return

        if (isinstance(button, tk.Frame) or self.__currButton == button or button == None):
            return

        row2 = button.grid_info()['row']
        col2 = button.grid_info()['column']

        if (self.__currButton != None):
            if (self.__game.get_board()[row][col].status == SquareStatus.HIDDEN and self.__game.get_board()[row][col].flagState == FlagStatus.OFF):
                if (isinstance(self.__currButton, tk.Label) and self.__currButton != button and self.__currButton is not None):
                    self.__currButton.config(bg="lightgray", image=self.__pixel, bd=2, width=20, height=20, relief=tk.FLAT)

        if (self.__game.get_board()[row2][col2].flagState == FlagStatus.OFF):
            button.config(background="white")
        self.__currButton = button

    def show(self, event):
        self.__resetButton.config(image=self.__smileyPics[0])

        if (self.__currButton == None):
            return

        row = self.__currButton.grid_info()['row']
        column = self.__currButton.grid_info()['column']
        self.__currButton = None
        if (self.__game.get_board()[row][column].status == SquareStatus.OPENED or self.__game.get_board()[row][column].flagState == FlagStatus.ON):
            return

        if (self.__firstSafeClick == FirstSafeClick.ACTIVE):
            self.__game.generate_minefield(row, column)
            self.__game.generate_neighbor_info()
            self.update_counter()
            self.__firstSafeClick = FirstSafeClick.INACTIVE

        if (self.__game.get_board()[row][column].has_mine == True):
            self.__buttons_list[row][column].config(bg="red", image=self.__minesPics[0])
            self.__window.after_cancel(self.__id)
            for i in range(self.__game.height):
                for j in range(self.__game.width):
                    if (i == row and j == column):
                        continue

                    if (self.__game.get_board()[i][j].has_mine is True and self.__game.get_board()[i][j].flagState == FlagStatus.OFF):
                        self.__buttons_list[i][j].config(bg="white", image=self.__minesPics[0])
                        self.__game.get_board()[i][j].status = SquareStatus.OPENED

                    elif (self.__game.get_board()[i][j].has_mine is False and self.__game.get_board()[i][j].flagState == FlagStatus.ON):
                        self.__buttons_list[i][j].config(image=self.__minesPics[1])

            self.__game.get_board()[row][column].status = SquareStatus.OPENED
            self.__resetButton.config(image=self.__smileyPics[2])
            self.__coverFrame.grid(row=1, column=0, sticky="nsew")
            return

        self.__game.update_board(row, column)
        for i in range(self.__game.height):
            for j in range(self.__game.width):
                if (self.__game.get_board()[i][j].status == SquareStatus.PENDING):
                    self.__game.get_board()[i][j].status = SquareStatus.OPENED
                    if (self.__game.get_board()[i][j].neighbor_mines == 0):
                        self.__squareCounter += 1
                        self.__buttons_list[i][j].config(bg="white")
                    else:
                        self.__squareCounter += 1
                        self.__buttons_list[i][j].config(bg="white",
                                                         image=self.__numberPics[self.__game.get_board()[i][j].neighbor_mines - 1],
                                                         anchor=tk.CENTER)
                    if (self.__squareCounter == (self.__game.height * self.__game.width) - self.__game.mines):
                        self.youWin()
                        return

    def youWin(self):
        self.__resetButton.config(image=self.__smileyPics[3])
        self.__window.after_cancel(self.__id)
        for r in range(self.__game.height):
            for c in range(self.__game.width):
                if (self.__game.get_board()[r][c].has_mine is True and self.__game.get_board()[r][c].flagState == FlagStatus.OFF):
                    self.__buttons_list[r][c].config(image=self.__flagImage)
                    self.__game.get_board()[r][c].flagState = FlagStatus.ON
                    self.__flagsLeft -= 1
                    self.__flagsLeft_label.config(text=f"{max(self.__flagsLeft, -99):03}")

        self.__coverFrame.grid(row=1, column=0, sticky="nsew")

        self.__bestTimes = BestTimes(self.__window)
        if (self.__bestTimes.compare(self.__gameDifficulty, self.__time_counter)):
            newBestTimeWindow = tk.Toplevel(self.__window, relief=tk.RAISED, bd=2)
            newBestTimeWindow.overrideredirect(True)
            self.__window.wm_attributes("-disabled", True)

            # Get window coordinates
            _, _, win_coords = self.__window.geometry().partition('+')
            x_str, y_str = win_coords.split('+')
            x, y = int(x_str), int(y_str)

            newBestTimeWindow.geometry(f"+{x+25}+{y+120}")
            label = tk.Label(newBestTimeWindow)
            label.pack(pady=5, padx=15)

            if (self.__gameDifficulty == Difficulty.BEGINNER):
                label.config(text="You have the fastest time\n  for beginner level.\nPlease enter your name.")
            elif (self.__gameDifficulty == Difficulty.INTERMEDIATE):
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

            self.__window.bind("<Button-1>", lambda event: entry.focus_set())

    @staticmethod
    def on_validate(P):
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
        row = event.widget.grid_info()['row']
        col = event.widget.grid_info()['column']
        if (self.__game.get_board()[row][col].status == SquareStatus.HIDDEN):
            if (self.__game.get_board()[row][col].flagState == FlagStatus.ON):
                event.widget.config(bg="lightgray", image=self.__pixel)
                self.__game.get_board()[row][col].flagState = FlagStatus.OFF
                self.__flagsLeft += 1
                self.__flagsLeft_label.config(text=f"{self.__flagsLeft:03}")
            else:
                event.widget.config(image=self.__flagImage)
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
