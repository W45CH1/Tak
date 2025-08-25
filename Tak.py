from PlayerController import GameEndException


def calc_stone_count(board_size):
    assert board_size >= 3
    if 3 <= board_size <= 8:
        return [10, 15, 21, 30, 40, 50][board_size - 3]

    return (board_size - 3) * 10


def calc_cap_stones(board_size):
    assert board_size >= 3
    return (board_size - 3) // 2


class Piece:
    def __init__(self, team, kind):
        assert isinstance(team, Team)
        self.team = team
        assert isinstance(kind, str)
        kind = kind.strip().replace(" ", "").replace("_", "").lower()
        assert kind == "stone" or kind == "wall" or kind == "capstone"
        self.kind = kind

        self.tag = set()  # Wichtig für feststellung wer Spiel gewonnen hat

    def copy(self):
        p = Piece(self.team, self.kind)
        p.tag = self.tag
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

    def __setitem__(self, item, value):
        if len(item) == 2:
            if item[0] in range(0, len(self.__board)):
                if item[1] in range(0, len(self.__board[item[0]])):
                    if type(value) == list:
                        self.__board[item[0]][item[1]] = value.copy()
                    elif type(value) == Piece:
                        self.__board[item[0]][item[1]] = [value]
                    else:
                        raise ValueError
        elif len(item) == 3:
            if item[0] in range(0, len(self.__board)):
                if item[1] in range(0, len(self.__board[item[0]])):
                    if item[2] in range(0, len(self.__board[item[0]][item[1]])):
                        assert type(value) == Piece
                        self.__board[item[0]][item[1]][item[2]] = [value]
        else:
            raise ValueError

    def __getitem__(self, item):
        if len(item) == 2:
            if item[0] in range(-len(self.__board), len(self.__board)):
                if item[1] in range(-len(self.__board[item[0]]), len(self.__board[item[0]])):
                    return self.__board[item[0]][item[1]]
            raise ValueError
        elif len(item) == 3:
            if item[0] in range(-len(self.__board), len(self.__board)):
                if item[1] in range(-len(self.__board[item[0]]), len(self.__board[item[0]])):
                    if item[2] in range(-len(self.__board[item[0]][item[1]]), len(self.__board[item[0]][item[1]])):
                        return self.__board[item[0]][item[1]][item[2]]
            raise ValueError
        else:
            raise ValueError

    def copy(self):
        out = Board(self.__board_size)

        for i in range(self.__board_size):
            for j in range(self.__board_size):
                out[i, j] = [p.copy() for p in self[i, j].copy()]
        return out

    def board_size(self):
        return self.__board_size


class Team:
    def __init__(self, stones, capstones):
        self.__stones = stones
        self.__capstones = capstones

    def get_stones(self):
        return self.__stones

    def get_capstone(self):
        return self.__capstones

    def has_stone(self):
        return self.__stones > 0

    def has_capstone(self):
        return self.__capstones > 0

    def use_stone(self):
        self.__stones -= 1

    def use_capstone(self):
        self.__capstones -= 1


class Tak:
    def __init__(self, board_size):
        stones = calc_stone_count(board_size)
        capstones = calc_cap_stones(board_size)
        self.board_size = board_size
        self.board = Board(board_size)
        self.team_white = Team(stones, capstones)
        self.team_black = Team(stones, capstones)

    def get_board(self):
        return self.board.copy()

    def place_stone(self, team, position):
        assert team is self.team_white or team is self.team_black
        assert position[0] in range(0, self.board_size)
        assert position[1] in range(0, self.board_size)
        assert self.board[position] == []
        assert team.has_stone()
        team.use_stone()
        self.board[position] = Piece(team, "stone")
        self.check_winning()

    def place_wall(self, team, position):
        assert team is self.team_white or team is self.team_black
        assert position[0] in range(0, self.board_size)
        assert position[1] in range(0, self.board_size)
        assert self.board[position] == []
        assert team.has_stone()
        team.use_stone()
        self.board[position] = Piece(team, "wall")
        self.check_winning()

    def place_capstone(self, team, position):
        assert team is self.team_white or team is self.team_black
        assert position[0] in range(0, self.board_size)
        assert position[1] in range(0, self.board_size)
        assert self.board[position] == []
        assert team.has_capstone()
        team.use_capstone()
        self.board[position] = Piece(team, "capstone")
        self.check_winning()

    def move(self, team, position_from, position_to):
        assert team is self.team_white or team is self.team_black
        assert len(position_from) == 2
        assert len(position_to) == 2
        assert position_from[0] in range(0, self.board_size)
        assert position_from[1] in range(0, self.board_size)
        assert position_to[0] in range(0, self.board_size)
        assert position_to[1] in range(0, self.board_size)
        assert len(self.board[position_from]) == 1
        assert self.board[position_from][0].team is team
        assert self.board[position_from][0].kind in {"stone", "capstone"}
        assert len(self.board[position_to]) == 0 or self.board[position_to, -1].kind == "stone"
        self.board[position_to].append(self.board[position_from][0])
        self.board[position_from] = []
        self.check_winning()

    def tumble(self, team, position_from, direction, tumble_count):
        assert team is self.team_white or team is self.team_black
        assert len(position_from) == 2
        assert position_from[0] in range(0, self.board_size)
        assert position_from[1] in range(0, self.board_size)
        assert direction in {(0, 1), (0, -1), (1, 0), (-1, 0)}
        assert len(self.board[position_from]) >= 1
        assert self.board[position_from, -1].kind in {"stone", "capstone"}
        assert self.board[position_from, -1].team is team
        position_to = (position_from[0], position_from[1])
        while len(tumble_count) != 0:
            position_to[0] += direction[0]
            position_to[1] += direction[1]
            assert position_to[0] in range(0, self.board_size)
            assert position_to[1] in range(0, self.board_size)
            assert len(self.board[position_to]) == 0 or self.board[position_to, -1].kind == "stone"

            self.board[position_to].extend(self.board[position_from][-tumble_count[0]:None])
            for _ in range(tumble_count[0]):
                self.board[position_from].pop()
            del tumble_count[0]
        self.check_winning()

    def check_winning(self):

        white = 0
        black = 0
        filled = 0
        for i in range(self.board_size):
            for j in range(self.board_size):
                cell = self.board[i, j]
                if not cell:
                    continue
                filled += 1
                if cell[-1].kind != "stone":
                    continue
                if cell[-1].team == self.team_white:
                    white += 1
                else:
                    black += 1

        if not self.team_white.has_stone() or not self.team_black.has_stone() or filled >= self.board_size ** 2:
            if white > black:
                raise GameEndException(winning_team=white, losing_team=black)
            elif black > white:
                raise GameEndException(winning_team=black, losing_team=white)
            else:
                raise GameEndException(draw=True)

        # Die Implementierung ist in O(n^3), ich weiß, das es besser geht
        board = self.board.copy()  # Damit ich nicht in dem Echten spielbrett tags setze
        for i in range(self.board_size):
            if board[i, 0]:
                board[i, 0, -1].tag.add("N")

            if board[0, i]:
                board[0, i, -1].tag.add("W")

        for k in range(self.board_size):
            for i in range(self.board_size):
                for j in range(self.board_size):
                    if not board[i, j]:
                        continue
                    team = board[i, j, -1].team
                    if i > 0 and board[i - 1, j] and board[i - 1, j, -1].team is team:
                        board[i - 1, j,-1].tag.update(board[i, j,-1].tag)
                    if j > 0 and board[i, j - 1] and board[i, j - 1, -1].team is team:
                        board[i, j - 1,-1].tag.update(board[i, j,-1].tag)
                    if i < self.board_size - 1 and board[i + 1, j] and board[i + 1, j, -1].team is team:
                        board[i + 1, j,-1].tag.update(board[i, j,-1].tag)
                    if j < self.board_size - 1 and board[i, j + 1] and board[i, j + 1, -1].team is team:
                        board[i, j + 1,-1].tag.update(board[i, j,-1].tag)

        white_winning = False
        black_winning = False
        for i in range(self.board_size):
            if board[i, -1] and "N" in board[i, -1, -1].tag:
                if board[i, -1, -1].team is self.team_white:
                    white_winning = True
                else:
                    black_winning = True
            if board[-1, i] and "W" in board[-1, i, -1].tag:
                if board[-1, i, -1].team is self.team_white:
                    white_winning = True
                else:
                    black_winning = True

        if white_winning and black_winning:
            raise GameEndException(draw=True)
        elif white_winning:
            raise GameEndException(winning_team=self.team_white, losing_team=self.team_black)
        elif black_winning:
            raise GameEndException(winning_team=self.team_black, losing_team=self.team_white)
