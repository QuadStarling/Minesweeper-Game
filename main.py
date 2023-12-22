from Game import *
from MenuBar import *

main_window = tk.Tk()
main_window.title("Minesweeper")
main_window.geometry("+700+220")

main_window.resizable(False, False)

Icon = tk.PhotoImage(file="Images/gameIcon.gif")
main_window.iconphoto(True, Icon)

g = Game(main_window)
MenuBar(main_window, g)
main_window.mainloop()
