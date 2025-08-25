from tkinter import *

from GameController import GameController
from PlayerController import PlayerController
from TakController import TakController

root = Tk()
root.resizable(width=False, height=False)
root.title("Tak")
root.iconphoto(False, PhotoImage(file="Tak.png"))
root.iconbitmap("Tak.ico")

t = TakController(root, 0, 1, board_size=5)

pw = PlayerController(root, 0, 0, t.tak.team_white)
pb = PlayerController(root, 0, 2, t.tak.team_black)

g = GameController(root, 1, 1, t, pw, pb)
t.next_move(t.tak.team_black,"ps#(0,1)")

t.next_move(t.tak.team_white,"ps#(0,0)")
t.next_move(t.tak.team_white,"mo#(0,0)#(0,1)#(1,)")
t.next_move(t.tak.team_white,"ps#(0,0)")
t.next_move(t.tak.team_white,"mo#(0,0)#(0,1)#(1,)")
t.next_move(t.tak.team_black,"ps#(0,0)")
t.next_move(t.tak.team_black,"mo#(0,0)#(0,1)#(1,)")
t.next_move(t.tak.team_black,"ps#(0,0)")
t.next_move(t.tak.team_black,"mo#(0,0)#(0,1)#(1,)")


t.next_move(t.tak.team_black,"mo#(0,1)#(1,0)#(2 ,2)")
t.next_move(t.tak.team_black,"mo#(2,1)#(-1,0)#(1)")

t.redraw()


root.mainloop()
