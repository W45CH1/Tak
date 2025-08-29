from PlayerController import GameEndException
from Team import Team


class Piece:
    def __init__(self, team, kind):
        assert isinstance(team, Team)
        self.team = team
        assert isinstance(kind, str)
        assert kind == "stone" or kind == "wall" or kind == "capstone"
        self.kind = kind

        self.tag = set()  # Wichtig für feststellung wer Spiel gewonnen hat

    def copy(self):
        p = Piece(self.team, self.kind)
        p.tag = self.tag.copy()
        return p


class Board:
    def __init__(self, board_size):
        assert isinstance(board_size, int)
        self.__board_size = board_size
        self.__board = []
        for i in range(board_size):
            self.__board.append([])
            for _ in range(board_size):
                self.__board[i].append([])

    def __setitem__(self, index, value):
        if len(index) == 2:
            if index[0] in range(0, len(self.__board)):
                if index[1] in range(0, len(self.__board[index[0]])):
                    if type(value) == list:
                        self.__board[index[0]][index[1]] = value.copy()
                        return
                    elif type(value) == Piece:
                        self.__board[index[0]][index[1]] = [value]
                        return
        elif len(index) == 3:
            if index[0] in range(0, len(self.__board)):
                if index[1] in range(0, len(self.__board[index[0]])):
                    if index[2] in range(0, len(self.__board[index[0]][index[1]])):
                        assert type(value) == Piece
                        self.__board[index[0]][index[1]][index[2]] = [value]
                        return
        raise ValueError

    def __getitem__(self, index):
        if len(index) == 2:
            if index[0] in range(-len(self.__board), len(self.__board)):
                if index[1] in range(-len(self.__board[index[0]]), len(self.__board[index[0]])):
                    return self.__board[index[0]][index[1]]
        elif len(index) == 3:
            if index[0] in range(-len(self.__board), len(self.__board)):
                if index[1] in range(-len(self.__board[index[0]]), len(self.__board[index[0]])):
                    if index[2] in range(-len(self.__board[index[0]][index[1]]), len(self.__board[index[0]][index[1]])):
                        return self.__board[index[0]][index[1]][index[2]]
        raise ValueError

    def copy(self):
        out = Board(self.board_size())

        for i in range(self.board_size()):
            for j in range(self.board_size()):
                out[i, j] = [p.copy() for p in self[i, j].copy()]
        return out

    def board_size(self):
        return self.__board_size




class Tak:
    def __init__(self, board_size,team_white,team_black):
        self.board_size = board_size
        self.board = Board(board_size)
        self.team_white = team_white
        self.team_black = team_black

    def get_board(self):
        return self.board.copy()

    def place_stone(self, team, position):
        assert team is self.team_white or team is self.team_black
        assert len(position) == 2
        assert position[0] in range(0, self.board_size)
        assert position[1] in range(0, self.board_size)
        assert self.board[position] == []
        assert team.has_stone()
        team.use_stone()
        self.board[position] = Piece(team, "stone")
        self.check_winning(team)

    def place_wall(self, team, position):
        assert team is self.team_white or team is self.team_black
        assert len(position) == 2
        assert position[0] in range(0, self.board_size)
        assert position[1] in range(0, self.board_size)
        assert self.board[position] == []
        assert team.has_stone()
        team.use_stone()
        self.board[position] = Piece(team, "wall")
        self.check_winning(team)

    def place_capstone(self, team, position):
        assert team is self.team_white or team is self.team_black
        assert len(position) == 2
        assert position[0] in range(0, self.board_size)
        assert position[1] in range(0, self.board_size)
        assert self.board[position] == []
        assert team.has_capstone()
        team.use_capstone()
        self.board[position] = Piece(team, "capstone")
        self.check_winning(team)


    def move(self, team, position_from, direction, drop_counts):
        if isinstance(drop_counts,int):
            drop_counts = (drop_counts,)
        drop_counts = list(drop_counts)
        assert team is self.team_white or team is self.team_black
        assert len(position_from) == 2
        assert position_from[0] in range(0, self.board_size)
        assert position_from[1] in range(0, self.board_size)
        direction_dict = {"n":(-1,0),"e":(0,1),"s":(1,0),"w":(0,-1)}
        assert direction in {"n","w","s","e"}
        direction = direction_dict[direction]
        assert len(self.board[position_from]) > 0
        assert self.board[position_from][-1].team is team
        count = sum(drop_counts)
        assert count <= len(self.board[position_from])
        assert count <= self.board_size
        new_board = self.board.copy() # We need this copy, so we don't end up in an invalid state, if we throw an exception
        taking = new_board[position_from][-count:None]
        new_board[position_from] = new_board[position_from][0:-count]
        position_to = [position_from[0], position_from[1]]
        while len(drop_counts) != 0:
            position_to[0] += direction[0]
            position_to[1] += direction[1]
            assert position_to[0] in range(0, self.board_size)
            assert position_to[1] in range(0, self.board_size)
            assert drop_counts[0] > 0
            if taking[-1].kind in {"stone","wall"} or sum(drop_counts) > 1:
                assert len(new_board[position_to]) == 0 or new_board[position_to][-1].kind == "stone"
            elif taking[-1].kind == "capstone":
                assert len(new_board[position_to]) == 0 or new_board[position_to][-1].kind in {"stone", "wall"}
                new_board[position_to][-1].kind = "stone"
            else:
                raise ValueError
            new_board[position_to] = new_board[position_to] + taking[0:drop_counts[0]]
            taking = taking[drop_counts[0]:None]
            del drop_counts[0]
        self.board = new_board
        self.check_winning(team)

    def check_winning(self,team):
        white = 0
        black = 0
        filled = 0
        for i in range(self.board_size):
            for j in range(self.board_size):
                cell = self.board[i, j]
                if not cell:
                    continue
                filled += 1
                if cell[-1].kind == "wall":
                    continue
                if cell[-1].team == self.team_white:
                    white += 1
                else:
                    black += 1

        if not self.team_white.has_piece() or not self.team_black.has_piece() or filled >= self.board_size ** 2:
            if white > black:
                raise GameEndException(winning_team=white, losing_team=black)
            elif black > white:
                raise GameEndException(winning_team=black, losing_team=white)
            else:
                raise GameEndException(draw=True)

        # Die Implementierung ist in O(n^3), ich weiß, das es besser geht
        board = self.board.copy()  # Damit ich nicht in dem Echten spielbrett tags setze
        for i in range(self.board_size):
            if board[i, 0] and board[i, 0, -1].kind != "wall":
                board[i, 0, -1].tag.add("W")

            if board[0, i] and board[0, i, -1].kind != "wall":
                board[0, i, -1].tag.add("N")

        for k in range(self.board_size ** 2):
            for i in range(self.board_size):
                for j in range(self.board_size):
                    if not board[i, j]:
                        continue
                    if board[i, j, -1].kind == "wall":
                        continue
                    current_team = board[i, j, -1].team
                    if i > 0 and board[i - 1, j] and board[i - 1, j, -1].team is current_team:
                        board[i - 1, j, -1].tag.update(board[i, j, -1].tag)
                    if j > 0 and board[i, j - 1] and board[i, j - 1, -1].team is current_team:
                        board[i, j - 1, -1].tag.update(board[i, j, -1].tag)
                    if i < self.board_size - 1 and board[i + 1, j] and board[i + 1, j, -1].team is current_team:
                        board[i + 1, j, -1].tag.update(board[i, j, -1].tag)
                    if j < self.board_size - 1 and board[i, j + 1] and board[i, j + 1, -1].team is current_team:
                        board[i, j + 1, -1].tag.update(board[i, j, -1].tag)

        white_winning = False
        black_winning = False
        for i in range(self.board_size):
            if board[i, -1] and "W" in board[i, -1, -1].tag:
                if board[i, -1, -1].team is self.team_white:
                    white_winning = True
                else:
                    black_winning = True
            if board[-1, i] and "N" in board[-1, i, -1].tag:
                if board[-1, i, -1].team is self.team_white:
                    white_winning = True
                else:
                    black_winning = True

        if white_winning and black_winning:
            raise GameEndException(winning_team=team)
        elif white_winning:
            raise GameEndException(winning_team=self.team_white, losing_team=self.team_black)
        elif black_winning:
            raise GameEndException(winning_team=self.team_black, losing_team=self.team_white)
