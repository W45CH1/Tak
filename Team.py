
def calc_stone_count(board_size):
    assert board_size >= 3
    if 3 <= board_size <= 8:
        return [10, 15, 21, 30, 40, 50][board_size - 3]

    return (board_size - 3) * 10


def calc_cap_stones(board_size):
    assert board_size >= 3
    return (board_size - 3) // 2
class Team:
    def __init__(self, board_size, lives=None, time=None):
        self.__stones = calc_stone_count(board_size)
        self.__capstones = calc_cap_stones(board_size)
        self.__lives = lives
        self.__time = time

    def use_lives(self):
        self.__lives -=1

    def use_time(self,time):
        assert isinstance(time,float)
        assert time > 0
        self.__time -= time

    def get_lives(self):
        return self.__lives

    def get_time(self):
        return self.__time

    def get_stones(self):
        return self.__stones

    def get_capstone(self):
        return self.__capstones

    def has_piece(self):
        return self.has_stone() or self.has_capstone()

    def has_stone(self):
        return self.__stones > 0

    def has_capstone(self):
        return self.__capstones > 0

    def use_stone(self):
        self.__stones -= 1

    def use_capstone(self):
        self.__capstones -= 1
