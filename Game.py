import tkinter as tk
from MSGame import *
from enum import Enum


class FirstSafeClick(Enum):
    ACTIVE = 0
    INACTIVE = 1


class Game:
    def __init__(self, window):
        self.__id = None
        self.__window = window
        self.__game_frame = tk.Frame(self.__window, bg="black", width=500, height=500, relief=tk.SUNKEN)
        self.__game_frame.grid(row=1, column=0)

        self.__stats_frame = tk.Frame(self.__window)
        self.__stats_frame.grid(row=0, column=0, sticky="wens")
        self.__window.columnconfigure(0, weight=1)

        self.__coverFrame = tk.Frame(self.__window, bg='')  # Covers the game frame to block the player from clicking the buttons

        self.__buttons_list = None  # A list to store buttons
        self.__game = None
        self.__resetButton = None  # A button that resets the game

        self.__squareCounter = 0  # Counts how many squares have been opened up that are not mines
        self.__counter_label = None

        self.__flagsLeft = 0
        self.__flagsLeft_label = None

        self.__time_counter = 0  # A Counter for how many seconds passed since the start of the game
        self.__firstSafeClick = FirstSafeClick.ACTIVE  # Makes sure that the first click is not a mine

    def Create_Game(self, width, height, mines):
        self.__counter_label = tk.Label(self.__stats_frame, bg="black", fg="red", text=f"{self.__time_counter:03}", font=("Arial", 18), width=3)
        self.__counter_label.pack(side=tk.RIGHT, padx=(0, 10))

        self.__flagsLeft = mines
        self.__flagsLeft_label = tk.Label(self.__stats_frame, bg="black", fg="red", text=f"{min(self.__flagsLeft, 999):03}", font=("Arial", 18), width=3)
        self.__flagsLeft_label.pack(side=tk.LEFT, padx=(10, 0))

        self.__resetButton = tk.Button(self.__stats_frame, text="O   O\n\\___/", bd=4, bg="yellow")
        self.__resetButton.pack(pady=10)
        self.__resetButton.bind("<Button-1>", lambda event: self.__resetButton.config(text="O   O\n\\___/"))
        self.__resetButton.bind("<ButtonRelease-1>", self.resetGame)

        self.__game = MSGame(width, height, mines)
        squares = (width * height)
        self.__buttons_list = [[] for _ in range(height)]

        # places and creates the buttons on the frame
        # while also storing them in the list
        for i in range(squares):
            button = tk.Button(self.__game_frame, bg="lightgray", width=2, height=1, relief=tk.FLAT)
            button.bind("<Button-1>", lambda event, btn=button: self.holding(btn))
            button.bind("<ButtonRelease-1>", lambda event, btn=button: self.show(btn))
            button.bind("<Button-3>", lambda event, btn=button: self.place_flag(btn))
            self.__buttons_list[i // height].append(button)
            button.grid(row=(i // height), column=i % width, pady=1, padx=1)

    def update_counter(self):
        self.__time_counter += 1
        self.__counter_label.config(text=f"{min(self.__time_counter, 999):03}")
        self.__id = self.__window.after(1000, self.update_counter)

    def resetGame(self, event):
        self.__coverFrame.grid_forget()
        self.__game.clear_board()
        self.__firstSafeClick = FirstSafeClick.ACTIVE
        self.__squareCounter = 0

        # stops and resets the timer
        self.__time_counter = 0
        self.__counter_label.config(text=f"{self.__time_counter:03}")
        if hasattr(self, "__id"):
            self.__window.after_cancel(self.__id)

        # Reset how many flag left
        self.__flagsLeft = self.__game.mines
        self.__flagsLeft_label.config(text=f"{self.__flagsLeft:03}")

        for i in range(self.__game.height):
            for j in range(self.__game.width):
                if (self.__game.get_board()[i][j].flagState == FlagStatus.ON):
                    self.__game.get_board()[i][j].flagState = FlagStatus.OFF
                    self.__buttons_list[i][j].bind("<ButtonRelease-1>",
                                                   lambda e, btn=self.__buttons_list[i][j]: self.show(btn))
                    self.__buttons_list[i][j].config(bg="lightgray", text='', width=2, height=1, relief=tk.FLAT,
                                                     state=tk.NORMAL)

                if (self.__game.get_board()[i][j].status == SquareStatus.OPENED):
                    self.__game.get_board()[i][j].status = SquareStatus.HIDDEN
                    self.__buttons_list[i][j].config(bg="lightgray", text='', width=2, height=1, relief=tk.FLAT,
                                                     state=tk.NORMAL)

    def holding(self, button):
        button.config(activebackground="white", bd=0, padx=3, pady=3)
        self.__resetButton.config(text="O   O\n O")

    def show(self, button):
        self.__resetButton.config(text="O   O\n\\___/")
        if (button['state'] == tk.DISABLED):
            return
        row = button.grid_info()['row']
        column = button.grid_info()['column']


        if (self.__firstSafeClick == FirstSafeClick.ACTIVE):
            self.__game.generate_minefield(row, column)
            self.__game.generate_neighbor_info()
            self.update_counter()
            self.__firstSafeClick = FirstSafeClick.INACTIVE

        if (self.__game.get_board()[row][column].has_mine == True):
            self.__buttons_list[row][column].config(bg="red", text='x')
            self.__window.after_cancel(self.__id)
            for i in range(self.__game.height):
                for j in range(self.__game.width):
                    if (i == row and j == column):
                        continue

                    if (self.__game.get_board()[i][j].has_mine == True and self.__game.get_board()[i][j].flagState == FlagStatus.OFF):
                        self.__buttons_list[i][j].config(bg="white", text='x')
                        self.__game.get_board()[i][j].status = SquareStatus.OPENED

                    elif (self.__game.get_board()[i][j].has_mine == False and self.__game.get_board()[i][j].flagState == FlagStatus.ON):
                        self.__buttons_list[i][j].config(bg="green")

            self.__game.get_board()[row][column].status = SquareStatus.OPENED
            self.__resetButton.config(text="X   X\n/``````\\")
            self.__coverFrame.grid(row=1, column=0, sticky="nsew")
            return

        self.__game.update_board(row, column)
        for i in range(self.__game.height):
            for j in range(self.__game.width):
                if (self.__game.get_board()[i][j].status == SquareStatus.PENDING):
                    self.__game.get_board()[i][j].status = SquareStatus.OPENED
                    if (self.__game.get_board()[i][j].neighbor_mines == 0):
                        self.__squareCounter += 1
                        self.__buttons_list[i][j].config(bg="white",
                                                         text='',
                                                         state=tk.DISABLED)
                    else:
                        self.__squareCounter += 1
                        self.__buttons_list[i][j].config(bg="white",
                                                         text=str(self.__game.get_board()[i][j].neighbor_mines),
                                                         disabledforeground="blue",
                                                         state=tk.DISABLED)
                    if (self.__squareCounter == (self.__game.height * self.__game.width) - self.__game.mines):
                        self.__resetButton.config(text="-   O\n\\___/")
                        self.__window.after_cancel(self.__id)
                        for r in range(self.__game.height):
                            for c in range(self.__game.width):
                                if (self.__game.get_board()[r][c].has_mine == True and self.__game.get_board()[r][c].flagState == FlagStatus.OFF):
                                    self.place_flag(self.__buttons_list[r][c])
                        self.__coverFrame.grid(row=1, column=0, sticky="nsew")
                        return

    def place_flag(self, button):
        row = button.grid_info()['row']
        col = button.grid_info()['column']
        if (self.__game.get_board()[row][col].status == SquareStatus.HIDDEN):
            current_color = button.cget("background")
            if (current_color == "orange"):
                button.config(bg="lightgray", state=tk.NORMAL)
                button.bind("<ButtonRelease-1>", lambda event: self.show(button))
                self.__game.get_board()[row][col].flagState = FlagStatus.OFF
                self.__flagsLeft += 1
                self.__flagsLeft_label.config(text=f"{self.__flagsLeft:03}")
            else:
                button.config(bg="orange", state=tk.DISABLED)
                button.bind("<ButtonRelease-1>", lambda event: self.__resetButton.config(text="O   O\n\\___/"))
                self.__game.get_board()[row][col].flagState = FlagStatus.ON
                self.__flagsLeft -= 1
                self.__flagsLeft_label.config(text=f"{max(self.__flagsLeft, -99):03}")
