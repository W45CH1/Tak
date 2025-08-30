from tkinter import *

from GameController import GameController
from PlayerController import PlayerController
from TakController import TakController
from Team import Team



root = Tk()
root.resizable(width=False, height=False)
root.title("Tak")
root.iconphoto(False, PhotoImage(file="Tak.png"))
root.iconbitmap("Tak.ico")
BOARD_SIZE = 5
tw = Team(BOARD_SIZE)
tb = Team(BOARD_SIZE)

pw = PlayerController(root, 0, 0, tw, tb)
pb = PlayerController(root, 0, 2, tb, tw)

t = TakController(root, 0, 1, tw, tb, board_size=BOARD_SIZE)

g = GameController(root, 1, 1, t, pw, pb)
t.next_move(t.tak.team_black, "ps;(0,1)")

t.next_move(t.tak.team_white, "ps;(0,0)")
t.next_move(t.tak.team_white, "mo;(0,0);E;1")
t.next_move(t.tak.team_white, "ps;(0,0)")
t.next_move(t.tak.team_white, "mo;(0,0);E;1")
t.next_move(t.tak.team_black, "ps;(0,0)")
t.next_move(t.tak.team_black, "mo;(0,0);E;1")
t.next_move(t.tak.team_black, "ps;(0,0)")
t.next_move(t.tak.team_black, "mo;(0,0);E;1")

t.next_move(t.tak.team_black, "mo;(0,1);S;(2 ,2)")
t.next_move(t.tak.team_black, "mo;(2,1);N;1")

t.redraw()

root.mainloop()
