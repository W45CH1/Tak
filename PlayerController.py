import io
import os.path
import sys
from tkinter import Frame, Text, filedialog, END
from tkinter.ttk import Combobox

from Player import Player

SELECT_CUSTOM_STR = "select custom"
AUTO_LOAD_PATH = os.path.relpath("Players")


class PlayerController:
    def __init__(self,master,row,column,team):
        frame = Frame(master)
        frame.grid(row=row, column=column, padx=20, pady=20)

        self.combobox = Combobox(frame, width=20)
        self.combobox.bind('<<ComboboxSelected>>',lambda event: self.update_selected())

        self.combobox['values'] = (SELECT_CUSTOM_STR,)
        self.combobox['state'] = 'readonly'

        self.combobox.grid(row=0)

        self.output = Text(frame, width=28, height=25)
        self.output['state'] = 'disabled'
        self.output.grid(row=1)

        self.team = team

        self.players = {}
        self.selected_player = None
        for file in os.listdir(AUTO_LOAD_PATH):
            if file[-3:None] == ".py":
                self.add_player(os.path.join(AUTO_LOAD_PATH,file))




    def update_selected(self):
        selected = self.combobox.get()
        if selected == SELECT_CUSTOM_STR:
            custom_file = filedialog.askopenfilename(filetypes=[("Python files","*.py")],initialdir="\\ ")
            if custom_file == "":
                return
            self.selected_player =  self.add_player(custom_file)
        else:
            self.selected_player = self.players[selected]

        self.start(self.team)

    def add_player(self,path):
        name = os.path.split(path)[1].replace(".py", "")
        self.combobox['values'] = self.combobox['values'] + (name,)
        player = Player(path)
        self.players[name] = player
        return player

    def write_to_output(self,text):
        self.output['state'] = "normal"
        self.output.insert(END,text)
        self.output['state'] = "disabled"

    def capture_output(self,func,*args):
        output_buffer = io.StringIO()
        real_buffer = sys.stdout
        sys.stdout = output_buffer

        out = func(*args)

        sys.stdout = real_buffer
        self.write_to_output(output_buffer.getvalue())
        return out

    def start(self,team):
        return self.capture_output(self.selected_player.start,team)

    def step(self,board):
        return self.capture_output(self.selected_player.step,board)


