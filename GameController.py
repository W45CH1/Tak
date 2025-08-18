from tkinter import Frame, Button

from PlayerController import PlayerController
from TakController import TakController


class GameController:
    def __init__(self,master,row,column,tak_controller,player_controller1,player_controller2):
        assert isinstance(tak_controller,TakController)
        assert isinstance(player_controller1,PlayerController)
        assert isinstance(player_controller2,PlayerController)

        frame = Frame(master)
        frame.grid(row=row, column=column, padx=20, pady=20)

        Button(frame,text = "start",command=self.run).grid(column=0)
        Button(frame,text= "step",command=self.step).grid(column=0)

        self.tak_controller = tak_controller
        self.player_controller_white = player_controller1
        self.player_controller_black = player_controller2

    def run(self):
        while True:
            self.tak_controller.next_move(self.player_controller_white.step(self.tak_controller.tak.board.copy()))
            self.tak_controller.next_move(self.player_controller_black.step(self.tak_controller.tak.board.copy()))

    def step(self):
        self.tak_controller.next_move(self.player_controller_white.step(self.tak_controller.tak.board.copy()))
        self.tak_controller.next_move(self.player_controller_black.step(self.tak_controller.tak.board.copy()))