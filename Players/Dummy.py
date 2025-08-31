from random import random

from Tak import Board


def start(team):
    print("start Dummy")

def step(board):
    print("step Dummy")
    assert isinstance(board,Board)

    for i in range(board.board_size()):
        for j in range(board.board_size()):
            if not board[i, j]:
                if random() > 0.3:
                    return f"PS;({i},{j})"
                else:
                    return f"PW;({i},{j})"
