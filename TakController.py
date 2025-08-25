from random import random
from tkinter import Canvas, Frame, Text, Label

from Tak import Tak


class TakController:
    def __init__(self, master, row, column, board_size=3):
        frame = Frame(master)
        frame.grid(row=row, column=column)

        self.info_team_white = Label(frame, text="", bg="white", fg="gray")
        self.info_team_white.grid(row=0, column=0, sticky="ew")

        self.info_team_black = Label(frame, text="", bg="black", fg="gray")
        self.info_team_black.grid(row=0, column=1, sticky="ew")

        self.canvas = Canvas(frame, width=400, height=400, bg="red", highlightthickness=0)
        self.canvas.grid(row=1, columnspan=2, sticky="ew", padx=0, pady=10)

        self.tak = Tak(board_size=board_size)

        self.board_size = board_size

        self.draw()

    def draw(self):
        self.info_team_white['text'] = f"Stones: {self.tak.team_white.get_stones()} Capstones:  {self.tak.team_white.get_capstone()}"
        self.info_team_black['text'] = f"Stones: {self.tak.team_black.get_stones()} Capstones:  {self.tak.team_black.get_capstone()}"

        cell_size = min(float(self.canvas['width']), float(self.canvas['height'])) / self.board_size
        for i in range(self.board_size):
            for j in range(self.board_size):
                fill = '#707070' if i % 2 + j % 2 == 1 else '#909090'
                self.canvas.create_rectangle(
                    i * cell_size,
                    j * cell_size,
                    (i + 1) * cell_size,
                    (j + 1) * cell_size,
                    fill=fill,
                    outline='',
                    tags="background"
                )

    def redraw(self):
        self.info_team_white['text'] = f"Stones: {self.tak.team_white.get_stones()} Capstones:  {self.tak.team_white.get_capstone()}"
        self.info_team_black['text'] = f"Stones: {self.tak.team_black.get_stones()} Capstones:  {self.tak.team_black.get_capstone()}"

        cell_size = min(float(self.canvas['width']), float(self.canvas['height'])) / self.board_size
        self.canvas.delete("pieces")
        for i in range(self.board_size):
            for j in range(self.board_size):
                pieces = self.tak.board[i, j]
                for index, piece in enumerate(pieces):
                    fill = "white" if piece.team == self.tak.team_white else "black"
                    size_adjustment = 0.5 * index / len(pieces)
                    if piece.kind == "stone":
                        self.canvas.create_rectangle(
                            (i + size_adjustment) * cell_size,
                            (j + size_adjustment) * cell_size,
                            (i + 1 - size_adjustment) * cell_size,
                            (j + 1 - size_adjustment) * cell_size,
                            fill=fill,
                            outline='#CCCCCC' if fill == "white" else "#333333",
                            tags="pieces"
                        )
                    elif piece.kind == "capstone":
                        self.canvas.create_oval(
                            (i + size_adjustment) * cell_size,
                            (j + size_adjustment) * cell_size,
                            (i + 1 - size_adjustment) * cell_size,
                            (j + 1 - size_adjustment) * cell_size,
                            fill=fill,
                            outline='',
                            tags="pieces"
                        )
                    elif piece.kind == "wall":
                        self.canvas.create_polygon(
                            (i + size_adjustment+  0.1) * cell_size,
                            (j+size_adjustment) * cell_size,
                            (i+size_adjustment) * cell_size,
                            (j + 0.1 + size_adjustment) * cell_size,
                            (i + 0.9 - size_adjustment) * cell_size,
                            (j + 1 - size_adjustment) * cell_size,
                            (i + 1 - size_adjustment) * cell_size,
                            (j + 0.9 - size_adjustment) * cell_size,
                            fill=fill,
                            outline='',
                            tags="pieces"
                        )

    def next_move(self,team,move):
        assert isinstance(move,str)
        move_args = move.strip().replace(" ","").replace(".",",").lower().split("#")
        move_type = move_args[0]

        if move_type == "ps":
            self.tak.place_stone(team,eval(move_args[1]))
        elif move_type == "pw":
            self.tak.place_wall(team,eval(move_args[1]))
        elif move_type == "pc":
            self.tak.place_capstone(team,eval(move_args[1]))
        elif move_type == "mo":
            self.tak.move(team, eval(move_args[1]), eval(move_args[2]), eval(move_args[3]))
        else:
            raise ValueError
