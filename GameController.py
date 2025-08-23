from tkinter import Frame, Button

from PlayerController import PlayerController, GameEndException
from TakController import TakController


class GameController:
    def __init__(self, master, row, column, tak_controller, player_controller1, player_controller2):
        assert isinstance(tak_controller, TakController)
        assert isinstance(player_controller1, PlayerController)
        assert isinstance(player_controller2, PlayerController)

        frame = Frame(master)
        frame.grid(row=row, column=column)

        Button(frame, text="run", command=self.run).grid(row=0, column=0)
        Button(frame, text="step", command=self.step).grid(row=0, column=1)

        self.tak_controller = tak_controller
        self.player_controller_white = player_controller1
        self.player_controller_black = player_controller2

        self.white_next = True

    def run(self):
        while self.step():
            pass

    def step(self):
        if self.white_next:
            player = self.player_controller_white
        else:
            player = self.player_controller_black
        try:
            self.tak_controller.next_move(player.team, player.step(self.tak_controller.tak.board.copy()))
        except GameEndException as end:
            self.player_controller_white.write_to_output(end)
            self.player_controller_black.write_to_output(end)
            return False
        except Exception as err:
            try:
                raise err
                player.punish(f"exception thrown {err.args}")
            except GameEndException as end:
                self.player_controller_white.write_to_output(end)
                self.player_controller_black.write_to_output(end)
                return False
        self.white_next = not self.white_next
        return True
