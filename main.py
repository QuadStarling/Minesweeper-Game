import sys
import tkinter as tk
import tkinter.ttk as ttk

from Game import *
from MenuBar import *


def play():
    start_frame.pack_forget()
    start_frame.destroy()
    g = Game(main_window)
    MenuBar(main_window, g)


main_window = tk.Tk()
main_window.title("Minesweeper")

Icon = tk.PhotoImage(file="Images/gameIcon.gif")
main_window.iconphoto(True, Icon)

start_frame = tk.Frame(master=main_window, bg="red")
start_frame.pack(fill=tk.BOTH)


tk.Button(start_frame, text="Start Game", command=play).pack(side=tk.TOP, pady=10)
tk.Button(start_frame, text="Exit", command=sys.exit).pack()

main_window.mainloop()
