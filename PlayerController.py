import io
import os.path
import sys
import time
import traceback
from tkinter import Frame, Text, filedialog, END, Label
from tkinter.ttk import Combobox

from Player import Player

SELECT_CUSTOM_STR = "select custom"
AUTO_LOAD_PATH = os.path.relpath("Players")


class GameEndException(Exception):
    def __init__(self, losing_team=None, winning_team=None,draw=None):
        assert losing_team or winning_team or draw
        assert draw != (losing_team or winning_team)
        self.losing_team = losing_team
        self.winning_team = winning_team
        self.draw = draw


class PlayerController:
    def __init__(self, master, row, column, team, opponent_team):
        frame = Frame(master)
        frame.grid(row=row, column=column, padx=20, pady=20)

        self.combobox = Combobox(frame, width=20)
        self.combobox.bind('<<ComboboxSelected>>', lambda event: self.update_selected())

        self.combobox['values'] = (SELECT_CUSTOM_STR,)
        self.combobox['state'] = 'readonly'

        self.combobox.grid(row=2)

        self.output = Text(frame, width=58, height=25)
        self.output['state'] = 'disabled'
        self.output.grid(row=3)

        self.team = team
        self.opponent_team = opponent_team

        self.time_label = Label(frame, width=20, text=f"{self.team.get_time()} s")
        self.time_label.grid(row=0)

        self.live_label = Label(frame, width=20, text=f"{self.team.get_lives()}♡")
        self.live_label.grid(row=1)



        self.players = {}
        self.selected_player = None
        for file in os.listdir(AUTO_LOAD_PATH):
            if file[-3:None] == ".py":
                try:
                    self.add_player(os.path.join(AUTO_LOAD_PATH, file))
                except KeyError or FileNotFoundError or ValueError as  err:
                    self.write_to_output("".join(traceback.format_exception(*sys.exc_info())))


    def update_selected(self):
        selected = self.combobox.get()
        if selected == SELECT_CUSTOM_STR:
            custom_file = filedialog.askopenfilename(filetypes=[("Python files", "*.py")], initialdir="\\ ")
            if custom_file == "":
                return
            self.selected_player = self.add_player(custom_file)
        else:
            self.selected_player = self.players[selected]

        self.start(self.team, self.opponent_team)

    def add_player(self, path):
        name = os.path.split(path)[1].replace(".py", "")
        player = Player(path)
        self.combobox['values'] = self.combobox['values'] + (name,)
        self.players[name] = player
        return player

    def write_to_output(self, text):
        self.output['state'] = "normal"
        self.output.insert(END, text)
        self.output['state'] = "disabled"

    def capture_output(self, func, *args):
        output_buffer = io.StringIO()
        real_buffer = sys.stdout
        sys.stdout = output_buffer
        now = time.time()
        out = func(*args)
        if self.team.get_time() is not None:
            self.team.use_time(time.time() - now)
            self.time_label['text'] = f"{self.team.get_time()} s"
            if self.team.get_time() <= 0:
                raise GameEndException(losing_team=self.team)
        sys.stdout = real_buffer
        self.write_to_output(output_buffer.getvalue())
        return out

    def start(self, team, opponent_team):
        return self.capture_output(self.selected_player.start, team, opponent_team)

    def step(self, board):
        return self.capture_output(self.selected_player.step, board)

    def punish(self, message):
        if self.team.get_lives() is not None:
            self.team.use_lives()
            self.live_label['text'] = f"{self.team.get_lives()}♡"
            if self.team.get_lives() <= 0:
                raise GameEndException(losing_team=self.team)

        self.write_to_output(f"punished for {message}")
