from square import *
import random


class MSGame:
    def __init__(self, width, height, mines):
        self.__width = width
        self.__height = height
        self.__mines = mines
        self.__board = [[MSSquare() for i in range(self.__width)] for j in range(self.__height)]

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

    @property
    def mines(self):
        return self.__mines

    def get_board(self):
        return self.__board

    def generate_minefield(self):
        for i in range(self.__mines):
            x = random.randint(0, self.__height - 1)  # Generate a random row
            y = random.randint(0, self.__width - 1)  # Generate a random column
            while (self.__board[x][y].has_mine == True):  # Check if it does not create the same coordinates twice
                x = random.randint(0, self.__height - 1)
                y = random.randint(0, self.__width - 1)
            self.__board[x][y].has_mine = True  # Now this square has a mine

    def generate_neighbor_info(self):
        for row in range(self.__height):
            for col in range(self.__width):
                if (self.__board[row][col].has_mine == True):  # Check if square has a mine
                    self.__board[row][col].neighbor_mines = 'x'  # Mark this square as a mine
                    continue  # Skip to the next square
                mines = 0  # Initialize default number for mines for every iteration

                # These loops checks for mines besides the square
                for x in range(row - 1, row + 2):
                    for y in range(col - 1, col + 2):
                        if ((x < 0) or (y < 0) or (x >= self.__height) or (y >= self.__width)):
                            continue

                        if (self.__board[x][y].has_mine == True):
                            mines += 1

                self.__board[row][col].neighbor_mines = mines

    def update_board(self, row, col):
        self.__board[row][col].status = SquareStatus.PENDING
        x = self.__board[row][col].neighbor_mines
        if (self.__board[row][col].neighbor_mines > 0):  # base case for the recursive method
            return

        # Check other squares
        for x in range(row - 1, row + 2):
            for y in range(col - 1, col + 2):
                if ((x < 0) or (y < 0) or (x >= self.__height) or (y >= self.__width)):  # Avoid going out of the board borders
                    continue

                if (self.__board[x][y].status == SquareStatus.PENDING or
                        self.__board[x][y].status == SquareStatus.OPENED or
                        self.__board[x][y].flagState == FlagStatus.ON):  # skip to the next square
                    continue

                self.update_board(x, y)  # Check the other squares using recursive

    def clear_board(self):
        for i in range(self.__height):
            for j in range(self.__width):
                if (self.__board[i][j].has_mine == True):
                    self.__board[i][j].neighbor_mines = 0

                self.__board[i][j].has_mine = False
