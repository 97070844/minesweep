import random
from tkinter import *
from functools import partial
from tkinter import messagebox
from tkinter import font

class MineSweep:
    def __init__(self):
        self.board = None
        self.size = None
        self.MINE = 1
        self.CLEAN = 0

    def create_board(self, size=10):
        self.size = size
        self.board = [[random.randint(self.CLEAN, self.MINE) for _ in range(self.size)] for _ in range(self.size)]


class GameState(MineSweep):
    def __init__(self):
        super().__init__()
        self.LIFECOUNT = 3
        self.COUNT = 5

    def is_mine(self, row, col):
        if self.board[row][col] == self.MINE:
            return True
        else:
            return False

    def is_alive(self):
        if self.LIFECOUNT <= 0:
            return False
        else:
            return True

    def get_lifecount(self):
        return self.LIFECOUNT

    def set_lifecount(self, val):
        self.LIFECOUNT = val

    def set_count(self, val):
        self.COUNT = val

    def get_count(self):
        return self.COUNT

    def reset(self):
        self.set_count(5)
        self.set_lifecount(3)
        self.create_board()
    
    
class GameScreen(Tk):
    def __init__(self):
        super().__init__()
        self.geometry("380x450")
        self.resizable(False, False)
        self.title("MineSweep")
        # self.iconbitmap("icon.ico")

        self.bomb = PhotoImage(file="icons/bomb.GIF")
        self.smile = PhotoImage(file="icons/smile.GIF")
        self.explo = PhotoImage(file="icons/explo.GIF")
        self.heart = PhotoImage(file="icons/heart.GIF")
        self.noheart = PhotoImage(file="icons/no_heart.GIF")
        self.button = list()
        self.label = list()

        #create gamestate instance
        self.gamestate = GameState()
        self.gamestate.create_board()

        ###########Top Frame (For showing lifecount images) ##########
        self.lifecount_frame = Frame(self, bg="white", border=1)
        self.lifecount_frame.pack(side="top", fill="x", padx=10, pady=(10, 0))

        for _ in range(3):
            self.label.append(Label(self.lifecount_frame, image=self.heart))
            self.label[-1].pack(side="left", padx=5, pady=5)

        self.text = Label(self.lifecount_frame, text="Welcome!", font=font.Font(size=10, weight="bold"))
        self.text.pack(side="right", padx=5, pady=5)

        #########Button Frame (For showing game grid 10x10) #########
        self.btn_frame = Frame(self)
        self.btn_frame.pack(fill="both", padx=10, pady=10)

        for row in range(10):
            for col in range(10):
                self.button.append(Button(self.btn_frame, image=self.bomb, command=partial(self.is_mine, row, col)))
                self.button[-1].grid(row=row, column=col)

    def is_mine(self, row, col):
        if self.gamestate.get_count() > 0 and self.gamestate.get_lifecount() > 0:
            # if user clicked mine, explo img will be shown, else smile img will be shown
            if self.gamestate.is_mine(row, col):
                self.button[(row * 10) + col].config(image=self.explo)
                self.remove_heart()
            else:
                self.button[(row * 10) + col].config(image=self.smile)

            # count -1
            self.gamestate.set_count(self.gamestate.get_count() - 1)
            self.text.config(text="{} count remaining..".format(self.gamestate.get_count()))

        if not self.gamestate.is_alive():
            self.ask("You Lost! Game Over\nWant to Play again?")

        if self.gamestate.get_count() == 0:
            self.ask("You Win!\nWant to Play again?")

    def remove_heart(self):
        self.label[self.gamestate.get_lifecount() - 1].config(image=self.noheart)
        self.gamestate.set_lifecount(self.gamestate.get_lifecount() - 1)

    def reset(self):
        self.gamestate.reset()

        ###Grid UI Reset###
        for row in range(10):
            for col in range(10):
                self.button[(row * 10) + col].config(image=self.bomb)

        ###Heart UI Reset###
        for i in range(3):
            self.label[i].config(image=self.heart)

        self.text.config(text="Welcome again!")

    def ask(self, msg):
        choice = messagebox.askyesno(title="Game Over", message=msg)
        if choice == True:
            self.reset()
        else:
            self.destroy()


if __name__ == '__main__':
    screen = GameScreen()
    screen.mainloop()
