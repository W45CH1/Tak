import sys
import traceback
from tkinter import Frame, Button

from PlayerController import PlayerController, GameEndException
from TakController import TakController


class GameController:
    def __init__(self, master, row, column, tak_controller, player_controller1, player_controller2):
        assert isinstance(tak_controller, TakController)
        assert isinstance(player_controller1, PlayerController)
        assert isinstance(player_controller2, PlayerController)

        self.master = master

        frame = Frame(master)
        frame.grid(row=row, column=column)

        self.is_running = False
        self.toggle_run_button = Button(frame, text="run", command=self.toggle_run)
        self.toggle_run_button.grid(row=0, column=0)
        Button(frame, text="step", command=self.step).grid(row=0, column=1)

        self.tak_controller = tak_controller
        self.player_controller_white = player_controller1
        self.player_controller_black = player_controller2

        self.white_next = True

    def toggle_run(self):
        if self.is_running:
            self.is_running = False
            self.toggle_run_button.config(text="run")
        else:
            self.is_running = True
            self.toggle_run_button.config(text="stop")
            self.run()

    def run(self):
        if self.step() and self.is_running:
            self.master.after(100, self.run)
        else:
            self.is_running = False
            self.toggle_run_button.config(text="run")

    def step(self):
        if self.white_next:
            player = self.player_controller_white
        else:
            player = self.player_controller_black
        try:
            self.tak_controller.next_move(player.team, player.step(self.tak_controller.tak.board.copy()))
            self.white_next = not self.white_next
        except GameEndException as end:
            self.player_controller_white.write_to_output("".join(traceback.format_exception(*sys.exc_info())))
            self.player_controller_black.write_to_output("".join(traceback.format_exception(*sys.exc_info())))
            return False
        except Exception as err:
            #raise err
            try:
                player.punish("".join(traceback.format_exception(*sys.exc_info())))
            except GameEndException as end:
                self.player_controller_white.write_to_output("".join(traceback.format_exception(*sys.exc_info())))
                self.player_controller_black.write_to_output("".join(traceback.format_exception(*sys.exc_info())))
                return False
        finally:
            self.tak_controller.redraw()
        return True
