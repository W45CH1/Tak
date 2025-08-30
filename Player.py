import inspect

class Player:
    def __init__(self,file_path):
        assert file_path[-3:None] == ".py", "Player file must be a python file"
        try:
            with  open(file_path) as file:
                namespace = {}
                exec(file.read(),namespace)
        except Exception as err:
            raise ValueError(f"Player file did not parse correctly! path: {file_path} error:{type(err)} {vars(err)}")

        try:
            start_func, step_func = namespace["start"], namespace["step"]
            assert callable(start_func)
            assert callable(step_func)
        except TypeError or AssertionError as err:
            raise ValueError(f"Player file does not return the correct functions: {err.__dict__}")

        self.start_func = start_func
        self.step_func = step_func
        self.namespace = namespace

    def start(self,team,opponent_team):
        signature = inspect.signature(self.start_func)
        num_args = len(signature.parameters)
        if num_args == 1:
            return self.start_func(team)
        else:
            return self.start_func(team,opponent_team)


    def step(self,board):
        return self.step_func(board)
