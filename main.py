from tkinter import *

from GameController import GameController
from PlayerController import PlayerController
from TakController import TakController

root = Tk()
root.resizable(width=False,height=False)
root.title("Tak")
root.iconphoto(False, PhotoImage(file="Tak.png"))
root.iconbitmap("Tak.ico")

t = TakController(root,0,1,board_size=5)

pw = PlayerController(root,0,0)
pb = PlayerController(root,0,2)


g = GameController(root,1,1, t,pw,pb)
root.mainloop()
