import tkinter as tk
from MSGame import *
from enum import Enum


class FirstSafeClick(Enum):
    ACTIVE = 0
    INACTIVE = 1


class Game:
    def __init__(self, window):
        self.__window = window
        self.__game_frame = tk.Frame(self.__window, bg="black", width=500, height=500, relief=tk.SUNKEN)
        self.__game_frame.grid(row=1, column=0)

        self.__stats_frame = tk.Frame(self.__window)
        self.__stats_frame.grid(row=0, column=0, pady=3)

        self.__coverFrame = tk.Frame(self.__window,
                                     bg='')  # Covers the game frame to block the player from clicking the buttons

        self.__buttons_list = None
        self.__game = None
        self.__resetButton = None

        self.__firstSafeClick = FirstSafeClick.ACTIVE  # Makes sure that the first click is not a mine

    def Create_Game(self, width, height, mines):
        self.__resetButton = tk.Button(self.__stats_frame, text="O   O\n\\___/", bd=4, bg="yellow")
        self.__resetButton.pack()
        self.__resetButton.bind("<Button-1>", lambda event: self.__resetButton.config(text="O   O\n\\___/"))
        self.__resetButton.bind("<ButtonRelease-1>", self.resetGame)

        self.__game = MSGame(width, height, mines)
        squares = (width * height)
        self.__buttons_list = [[] for _ in range(height)]

        for i in range(squares):
            button = tk.Button(self.__game_frame, bg="lightgray", width=2, height=1, relief=tk.FLAT)
            button.bind("<Button-1>", lambda event, btn=button: self.holding(btn))
            button.bind("<ButtonRelease-1>", lambda event, btn=button: self.show(btn))
            button.bind("<Button-3>", lambda event, btn=button: self.place_flag(btn))
            self.__buttons_list[i // height].append(button)
            button.grid(row=(i // height), column=i % width, pady=1, padx=1)

    def resetGame(self, event):
        self.__coverFrame.grid_forget()
        self.__game.clear_board()
        self.__firstSafeClick = FirstSafeClick.ACTIVE
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
        row = button.grid_info()['row']
        column = button.grid_info()['column']
        self.__resetButton.config(text="O   O\n\\___/")

        if (self.__firstSafeClick == FirstSafeClick.ACTIVE):
            self.__game.generate_minefield(row, column)
            self.__game.generate_neighbor_info()
            self.__firstSafeClick = FirstSafeClick.INACTIVE

        if (self.__game.get_board()[row][column].has_mine == True):
            self.__buttons_list[row][column].config(bg="red", text='x')
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
                        self.__buttons_list[i][j].config(bg="white",
                                                         text='',
                                                         disabledforeground="blue",
                                                         state=tk.DISABLED)
                        continue
                    self.__buttons_list[i][j].config(bg="white",
                                                     text=str(self.__game.get_board()[i][j].neighbor_mines),
                                                     disabledforeground="blue",
                                                     state=tk.DISABLED)

    def place_flag(self, button):
        row = button.grid_info()['row']
        col = button.grid_info()['column']
        if (self.__game.get_board()[row][col].status == SquareStatus.HIDDEN):
            current_color = button.cget("background")
            if (current_color == "orange"):
                button.config(bg="lightgray", state=tk.NORMAL)
                button.bind("<ButtonRelease-1>", lambda event: self.show(button))
                self.__game.get_board()[row][col].flagState = FlagStatus.OFF
            else:
                button.config(bg="orange", state=tk.DISABLED)
                button.bind("<ButtonRelease-1>", lambda event: self.__resetButton.config(text="O   O\n\\___/"))
                self.__game.get_board()[row][col].flagState = FlagStatus.ON
