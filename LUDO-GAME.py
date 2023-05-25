# Ludo Game
# autor: Martin Klokočík


import random
import sys
import tkinter
import tkinter.messagebox
from tkinter import *

from PIL import Image, ImageTk


class Menu:
    def __init__(self):
        self.menu = Tk()
        self.menu.title("Menu")
        self.menu.geometry("500x500")

        self.num_of_players = IntVar()
        self.entryn = []
        self.player_names = []
        self.previous_name = []

        bg = PhotoImage(file="./pictures/menu.png")
        label1 = Label(self.menu, image=bg)
        label1.place(x=0, y=0)

        self.load_previous_names()

        Label(self.menu, text="Choose the number of players\nand type your nickname",
              font=('Comic Sans MS', 10, "bold"), padx=0,
              width=25, height=2, pady=0).place(anchor=CENTER, x=250, y=50)
        scale = Scale(self.menu, variable=self.num_of_players, from_=0, to=4, orient=HORIZONTAL,
                      command=self.player_name, bg="violet", relief=tkinter.RAISED, bd=0, activebackground="grey")
        scale.place(anchor=CENTER, x=250, y=100)

        self.button = Button(text="SUBMIT", command=self.submit, bg="light green", activebackground="dark green",
                             relief=tkinter.RAISED, bd=2, width=10, height=1)
        self.button.place(anchor=CENTER, x=250, y=(172 + len(self.entryn) * 22))

        self.menu.mainloop()

    def load_previous_names(self):
        with open('./data/previous_games.txt', 'r') as f:
            last_line = f.readlines()[-1]

        self.data = last_line.split()
        helping = ''

        for i in range(len(self.data)):
            if '/' not in self.data[i]:
                helping += self.data[i] + " "
            else:
                helping += self.data[i][:-1]
                self.previous_name.append(helping)
                helping = ''

    def player_name(self, number):
        colours = ['green', 'red', 'blue', 'yellow']
        self.button.place_forget()
        g = len(self.entryn) - 1
        while g >= 0:
            self.entryn[g].place_forget()
            self.entryn.pop(g)
            self.player_names.pop(g)
            g -= 1

        for i in range(self.num_of_players.get()):
            self.entryn.append(Entry(self.menu, fg=colours[i], background='grey'))
            self.player_names.append(self.entryn[i])
            self.entryn[i].insert(i, self.previous_name[i])
            self.entryn[i].place(anchor=CENTER, x=250, y=(150 + i * 22))

        self.button.place(anchor=CENTER, x=250, y=(172 + len(self.entryn) * 22))

    def submit(self):
        for i in range(len(self.entryn)):
            self.player_names[i] = self.player_names[i].get()
        if len(self.player_names) < 2:
            result = tkinter.messagebox.askyesno(f'Not enough players.',
                                                 "Not enough players. Choose again or press no to exit.")
            if result:
                pass
            else:
                sys.exit()
        else:
            self.menu.destroy()


class Clovece(Menu):
    def __init__(self):
        super().__init__()

        self.canvas = tkinter.Canvas()
        self.canvas.pack()

        self.definovanie_policok_a_pozicii()
        self.nacitanie_obrazkov()
        self.desk()

        self.hodkockou = tkinter.Button(image=self.roll_dice_image, command=self.roll)
        self.hodkockou.place(x=875, y=550)

        tkinter.mainloop()

    def definovanie_policok_a_pozicii(self):
        for j in range(4):
            if j >= self.num_of_players.get():
                self.player_names.append("Not playing")
            elif (j < self.num_of_players.get()) and (len(self.player_names[j]) == 0) or (
                    self.player_names[j] == 'Change your name here: '):
                self.player_names[j] = "Player n. " + str(j + 1)

        self.pozicia = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.pocet_vo_finale = [0, 0, 0, 0]
        self.pred_domcekom = [False, False, False, False, False, False, False, False, False, False, False, False, False,
                              False, False, False]
        self.na_startovnom = [False, False, False, False, False, False, False, False, False, False, False, False, False,
                              False, False, False]
        self.colors = ['Green', 'Red', 'Blue', 'Yellow']
        self.kills = [0, 0, 0, 0]
        self.hrac_na_rade = 1
        self.neutralne_policka = {
            1: (100, 350),
            2: (150, 350),
            3: (200, 350),
            4: (250, 350),
            5: (300, 350),
            6: (350, 300),
            7: (350, 250),
            8: (350, 200),
            9: (350, 150),
            10: (350, 100),
            11: (350, 50),
            12: (400, 50),
            13: (450, 50),
            14: (450, 100),
            15: (450, 150),
            16: (450, 200),
            17: (450, 250),
            18: (450, 300),
            19: (500, 350),
            20: (550, 350),
            21: (600, 350),
            22: (650, 350),
            23: (700, 350),
            24: (750, 350),
            25: (750, 400),
            26: (750, 450),
            27: (700, 450),
            28: (650, 450),
            29: (600, 450),
            30: (550, 450),
            31: (500, 450),
            32: (450, 500),
            33: (450, 550),
            34: (450, 600),
            35: (450, 650),
            36: (450, 700),
            37: (450, 750),
            38: (400, 750),
            39: (350, 750),
            40: (350, 700),
            41: (350, 650),
            42: (350, 600),
            43: (350, 550),
            44: (350, 500),
            45: (300, 450),
            46: (250, 450),
            47: (200, 450),
            48: (150, 450),
            49: (100, 450),
            50: (50, 450),
            51: (50, 400),
            52: (50, 350)
        }
        self.pozicie_domceky = {
            0: (107.5, 107.5),
            1: (217.5, 107.5),
            2: (107.5, 217.5),
            3: (217.5, 217.5),
            4: (582.5, 107.5),
            5: (692.5, 107.5),
            6: (582.5, 217.5),
            7: (692.5, 217.5),
            8: (582.5, 582.5),
            9: (692.5, 582.5),
            10: (582.5, 692.5),
            11: (692.5, 692.5),
            12: (107.5, 582.5),
            13: (217.5, 582.5),
            14: (107.5, 692.5),
            15: (217.5, 692.5),
        }
        self.pozicie_zaciatky = [1, 1, 1, 1, 14, 14, 14, 14, 27, 27, 27, 27, 40, 40, 40, 40]
        self.cielove_zelene = {
            52: (100, 400),
            53: (150, 400),
            54: (200, 400),
            55: (250, 400),
            56: (300, 400),
        }
        self.uplny_ciel_zeleny = {
            57: (350, 400),
        }
        self.cielove_cervene = {
            13: (400, 100),
            14: (400, 150),
            15: (400, 200),
            16: (400, 250),
            17: (400, 300),
        }
        self.uplny_ciel_cerveny = {
            18: (400, 350),
        }
        self.celove_modre = {
            26: (700, 400),
            27: (650, 400),
            28: (600, 400),
            29: (550, 400),
            30: (500, 400),
        }
        self.uplny_ciel_modry = {
            31: (450, 400),
        }
        self.celove_zlte = {
            39: (400, 700),
            40: (400, 650),
            41: (400, 600),
            42: (400, 550),
            43: (400, 500),
        }
        self.uplny_ciel_zlty = {
            44: (400, 450),
        }

    def nacitanie_obrazkov(self):
        figure_otvor = Image.open('./pictures/BLUE-final.png')
        figure_otvor = figure_otvor.resize((35, 35))
        self.blue_figure = ImageTk.PhotoImage(figure_otvor)
        figure_otvor.close()

        figure_otvor = Image.open('./pictures/GREEN-final.png')
        figure_otvor = figure_otvor.resize((35, 35))
        self.green_figure = ImageTk.PhotoImage(figure_otvor)
        figure_otvor.close()

        figure_otvor = Image.open('./pictures/RED-final.png')
        figure_otvor = figure_otvor.resize((35, 35))
        self.red_figure = ImageTk.PhotoImage(figure_otvor)
        figure_otvor.close()

        figure_otvor = Image.open('./pictures/YELLOW-final.png')
        figure_otvor = figure_otvor.resize((35, 35))
        self.yellow_figure = ImageTk.PhotoImage(figure_otvor)
        figure_otvor.close()

        self.possible_dice_option = [None, None, None, None, None, None, None]
        kocka_otvor = Image.open('./pictures/Dice-1.png')
        kocka_otvor = kocka_otvor.resize((225, 225))
        self.possible_dice_option[1] = ImageTk.PhotoImage(kocka_otvor)
        kocka_otvor.close()

        kocka_otvor = Image.open('./pictures/Dice-2.png')
        kocka_otvor = kocka_otvor.resize((225, 225))
        self.possible_dice_option[2] = ImageTk.PhotoImage(kocka_otvor)
        kocka_otvor.close()

        kocka_otvor = Image.open('./pictures/Dice-3.png')
        kocka_otvor = kocka_otvor.resize((225, 225))
        self.possible_dice_option[3] = ImageTk.PhotoImage(kocka_otvor)
        kocka_otvor.close()

        kocka_otvor = Image.open('./pictures/Dice-4.png')
        kocka_otvor = kocka_otvor.resize((225, 225))
        self.possible_dice_option[4] = ImageTk.PhotoImage(kocka_otvor)
        kocka_otvor.close()

        kocka_otvor = Image.open('./pictures/Dice-5.png')
        kocka_otvor = kocka_otvor.resize((225, 225))
        self.possible_dice_option[5] = ImageTk.PhotoImage(kocka_otvor)
        kocka_otvor.close()

        kocka_otvor = Image.open('./pictures/Dice-6.png')
        kocka_otvor = kocka_otvor.resize((225, 225))
        self.possible_dice_option[6] = ImageTk.PhotoImage(kocka_otvor)
        kocka_otvor.close()

        roll_otvor = Image.open('./pictures/Roll-dice.png')
        roll_otvor = roll_otvor.resize((150, 80))
        self.roll_dice_image = ImageTk.PhotoImage(roll_otvor)
        roll_otvor.close()

        pozadie = Image.open('./pictures/background2.jpg')
        pozadie = pozadie.resize((1200, 800))
        self.pozadie2 = ImageTk.PhotoImage(pozadie)
        pozadie.close()

    def desk(self):
        self.canvas.configure(width=1200, height=800)
        self.canvas.create_image(600, 400, image=self.pozadie2)

        # políčka na pohybovanie
        for i in range(6):
            if i == 1:
                self.canvas.create_rectangle(25 + (i * 50), 325, 75 + (i * 50), 375, fill='green')
                self.canvas.create_rectangle(25 + (i * 50), 375, 75 + (i * 50), 425, fill='green')
            elif i == 0:
                self.canvas.create_rectangle(25 + (i * 50), 325, 75 + (i * 50), 375, fill='white')
                self.canvas.create_rectangle(25 + (i * 50), 375, 75 + (i * 50), 425, fill='white')
            else:
                self.canvas.create_rectangle(25 + (i * 50), 325, 75 + (i * 50), 375, fill='white')
                self.canvas.create_rectangle(25 + (i * 50), 375, 75 + (i * 50), 425, fill='green')

            self.canvas.create_rectangle(25 + (i * 50), 425, 75 + (i * 50), 475, fill='white')

        for i in range(6):
            if i == 1:
                self.canvas.create_rectangle(425, 25 + (i * 50), 475, 75 + (i * 50), fill='red')
                self.canvas.create_rectangle(375, 25 + (i * 50), 425, 75 + (i * 50), fill='red')
            elif i == 0:
                self.canvas.create_rectangle(425, 25 + (i * 50), 475, 75 + (i * 50), fill='white')
                self.canvas.create_rectangle(375, 25 + (i * 50), 425, 75 + (i * 50), fill='white')
            else:
                self.canvas.create_rectangle(425, 25 + (i * 50), 475, 75 + (i * 50), fill='white')
                self.canvas.create_rectangle(375, 25 + (i * 50), 425, 75 + (i * 50), fill='red')

            self.canvas.create_rectangle(325, 25 + (i * 50), 375, 75 + (i * 50), fill='white')

        for i in range(6):
            if i == 1:
                self.canvas.create_rectangle(775 - (i * 50), 425, 725 - (i * 50), 475, fill='blue')
                self.canvas.create_rectangle(775 - (i * 50), 375, 725 - (i * 50), 425, fill='blue')
            elif i == 0:
                self.canvas.create_rectangle(775 - (i * 50), 425, 725 - (i * 50), 475, fill='white')
                self.canvas.create_rectangle(775 - (i * 50), 375, 725 - (i * 50), 425, fill='white')
            else:
                self.canvas.create_rectangle(775 - (i * 50), 425, 725 - (i * 50), 475, fill='white')
                self.canvas.create_rectangle(775 - (i * 50), 375, 725 - (i * 50), 425, fill='blue')

            self.canvas.create_rectangle(775 - (i * 50), 325, 725 - (i * 50), 375, fill='white')

        for i in range(6):
            if i == 1:
                self.canvas.create_rectangle(325, 775 - (i * 50), 375, 725 - (i * 50), fill='yellow')
                self.canvas.create_rectangle(375, 775 - (i * 50), 425, 725 - (i * 50), fill='yellow')
            elif i == 0:
                self.canvas.create_rectangle(325, 775 - (i * 50), 375, 725 - (i * 50), fill='white')
                self.canvas.create_rectangle(375, 775 - (i * 50), 425, 725 - (i * 50), fill='white')
            else:
                self.canvas.create_rectangle(325, 775 - (i * 50), 375, 725 - (i * 50), fill='white')
                self.canvas.create_rectangle(375, 775 - (i * 50), 425, 725 - (i * 50), fill='yellow')

            self.canvas.create_rectangle(425, 775 - (i * 50), 475, 725 - (i * 50), fill='white')

        # trojuholníky vo vnútri
        self.canvas.create_polygon(325, 325, 400, 400, 325, 475, fill='green', outline='black', width=1)
        self.canvas.create_polygon(325, 325, 400, 400, 475, 325, fill='red', outline='black', width=1)
        self.canvas.create_polygon(475, 325, 400, 400, 475, 475, fill='blue', outline='black', width=1)
        self.canvas.create_polygon(325, 475, 400, 400, 475, 475, fill='yellow', outline='black', width=1)

        # Zelený štart
        self.canvas.create_rectangle(50, 50, 275, 275, fill='white', outline='green', width=8)

        self.canvas.create_rectangle(75, 75, 140, 140, fill='white', outline='green', width=6)
        self.canvas.create_rectangle(75, 185, 140, 250, fill='white', outline='green', width=6)
        self.canvas.create_rectangle(185, 75, 250, 140, fill='white', outline='green', width=6)
        self.canvas.create_rectangle(185, 185, 250, 250, fill='white', outline='green', width=6)

        self.canvas.create_text(162.5, 162.5, text=str(self.player_names[0]), font=('Copperplate Gothic Bold', 20))

        # Červený štart
        self.canvas.create_rectangle(525, 50, 750, 275, fill='white', outline='red', width=8)

        self.canvas.create_rectangle(550, 75, 615, 140, fill='white', outline='red', width=6)
        self.canvas.create_rectangle(550, 185, 615, 250, fill='white', outline='red', width=6)
        self.canvas.create_rectangle(660, 75, 735, 140, fill='white', outline='red', width=6)
        self.canvas.create_rectangle(660, 185, 735, 250, fill='white', outline='red', width=6)

        self.canvas.create_text(637.5, 162.5, text=str(self.player_names[1]), font=('Copperplate Gothic Bold', 20))

        # Žltý štart
        self.canvas.create_rectangle(50, 525, 275, 750, fill='white', outline='yellow', width=8)

        self.canvas.create_rectangle(75, 550, 140, 615, fill='white', outline='yellow', width=6)
        self.canvas.create_rectangle(75, 660, 140, 725, fill='white', outline='yellow', width=6)
        self.canvas.create_rectangle(185, 550, 250, 615, fill='white', outline='yellow', width=6)
        self.canvas.create_rectangle(185, 660, 250, 725, fill='white', outline='yellow', width=6)

        self.canvas.create_text(162.5, 637.5, text=str(self.player_names[3]), font=('Copperplate Gothic Bold', 20))

        # Modrý štart
        self.canvas.create_rectangle(525, 525, 750, 750, fill='white', outline='blue', width=8)

        self.canvas.create_rectangle(550, 550, 615, 615, fill='white', outline='blue', width=6)
        self.canvas.create_rectangle(550, 660, 615, 725, fill='white', outline='blue', width=6)
        self.canvas.create_rectangle(660, 550, 735, 615, fill='white', outline='blue', width=6)
        self.canvas.create_rectangle(660, 660, 735, 725, fill='white', outline='blue', width=6)

        self.canvas.create_text(637.5, 637.5, text=str(self.player_names[2]), font=('Copperplate Gothic Bold', 20))

        # Zelený štart figúrky
        self.figures = [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        self.figures[0] = self.canvas.create_image(self.pozicie_domceky[0][0], self.pozicie_domceky[0][1],
                                                   image=self.green_figure, tags='green_figure_1')
        self.figures[1] = self.canvas.create_image(self.pozicie_domceky[1][0], self.pozicie_domceky[1][1],
                                                   image=self.green_figure, tags='green_figure_2')
        self.figures[2] = self.canvas.create_image(self.pozicie_domceky[2][0], self.pozicie_domceky[2][1],
                                                   image=self.green_figure, tags='green_figure_3')
        self.figures[3] = self.canvas.create_image(self.pozicie_domceky[3][0], self.pozicie_domceky[3][1],
                                                   image=self.green_figure, tags='green_figure_4')

        # Červený štart figúrky
        self.figures[4] = self.canvas.create_image(self.pozicie_domceky[4][0], self.pozicie_domceky[4][1],
                                                   image=self.red_figure, tags='red_figure_1')
        self.figures[5] = self.canvas.create_image(self.pozicie_domceky[5][0], self.pozicie_domceky[5][1],
                                                   image=self.red_figure, tags='red_figure_2')
        self.figures[6] = self.canvas.create_image(self.pozicie_domceky[6][0], self.pozicie_domceky[6][1],
                                                   image=self.red_figure, tags='red_figure_3')
        self.figures[7] = self.canvas.create_image(self.pozicie_domceky[7][0], self.pozicie_domceky[7][1],
                                                   image=self.red_figure, tags='red_figure_4')

        # Modrý štart figúrky
        self.figures[8] = self.canvas.create_image(self.pozicie_domceky[8][0], self.pozicie_domceky[8][1],
                                                   image=self.blue_figure, tags='blue_figure_1')
        self.figures[9] = self.canvas.create_image(self.pozicie_domceky[9][0], self.pozicie_domceky[9][1],
                                                   image=self.blue_figure, tags='blue_figure_2')
        self.figures[10] = self.canvas.create_image(self.pozicie_domceky[10][0], self.pozicie_domceky[10][1],
                                                    image=self.blue_figure, tags='blue_figure_3')
        self.figures[11] = self.canvas.create_image(self.pozicie_domceky[11][0], self.pozicie_domceky[11][1],
                                                    image=self.blue_figure, tags='blue_figure_4')

        # Žltý štart figúrky
        self.figures[12] = self.canvas.create_image(self.pozicie_domceky[12][0], self.pozicie_domceky[12][1],
                                                    image=self.yellow_figure, tags='yellow_figure_1')
        self.figures[13] = self.canvas.create_image(self.pozicie_domceky[13][0], self.pozicie_domceky[13][1],
                                                    image=self.yellow_figure, tags='yellow_figure_2')
        self.figures[14] = self.canvas.create_image(self.pozicie_domceky[14][0], self.pozicie_domceky[14][1],
                                                    image=self.yellow_figure, tags='yellow_figure_3')
        self.figures[15] = self.canvas.create_image(self.pozicie_domceky[15][0], self.pozicie_domceky[15][1],
                                                    image=self.yellow_figure, tags='yellow_figure_4')

        # Ukazovač kto je na rade
        self.whoisnext = self.canvas.create_text(950, 200,
                                                 text=str(self.player_names[self.hrac_na_rade - 1]) + "'s turn",
                                                 font=('Copperplate Gothic Bold', 25), fill='white')
        self.hodene = self.canvas.create_image(950, 400, image=self.possible_dice_option[1], tags='rolled_dice')
        self.info = self.canvas.create_text(950, 250, text="Roll the dice", font=('Copperplate Gothic Bold', 20),
                                            fill='white')

        self.finale = [None, None, None, None]
        self.finale[0] = self.canvas.create_text(340, 430, text=self.pocet_vo_finale[0],
                                                 font=('Copperplate Gothic Bold', 15))
        self.finale[1] = self.canvas.create_text(430, 340, text=self.pocet_vo_finale[1],
                                                 font=('Copperplate Gothic Bold', 15))
        self.finale[2] = self.canvas.create_text(460, 430, text=self.pocet_vo_finale[2],
                                                 font=('Copperplate Gothic Bold', 15))
        self.finale[3] = self.canvas.create_text(430, 460, text=self.pocet_vo_finale[3],
                                                 font=('Copperplate Gothic Bold', 15))

    def roll(self):
        self.hodkockou.configure(state='disabled')
        self.canvas.delete(self.info)
        self.info = self.canvas.create_text(950, 250, text="Rolling...",
                                            font=('Copperplate Gothic Bold', 20), fill='white')
        hod = 0
        self.canvas.update()
        rand_num = random.randint(1, 40)
        rychlost = 200 / rand_num
        for i in range(rand_num):
            self.canvas.delete(self.hodene)
            hod = random.randint(1, 6)
            self.canvas.delete(self.hodene)
            self.hodene = self.canvas.create_image(950, 400, image=self.possible_dice_option[hod], tags='rolled_dice')
            self.canvas.after(int(rychlost))
            self.canvas.update()
            rychlost += 200 / rand_num

        self.tah(hod)

    def tah(self, hodene):
        if self.hrac_na_rade == 1:
            c = 0
            for i in range(0, 4):
                if ((self.pozicia[i] + hodene) > 57) or (self.pozicia[i] == 0 and hodene != 6):
                    c += 1
            if c == 4:
                self.help_vyhodnotenia(False)
            else:
                self.canvas.delete(self.info)
                self.info = self.canvas.create_text(950, 250, text="Click on figure to move",
                                                    font=('Copperplate Gothic Bold', 20), fill='white')
            self.canvas.update()
            self.canvas.tag_bind('green_figure_1', '<Button-1>', lambda event: self.check(0, hodene))
            self.canvas.tag_bind('green_figure_2', '<Button-1>', lambda event: self.check(1, hodene))
            self.canvas.tag_bind('green_figure_3', '<Button-1>', lambda event: self.check(2, hodene))
            self.canvas.tag_bind('green_figure_4', '<Button-1>', lambda event: self.check(3, hodene))

        elif self.hrac_na_rade == 2:
            c = 0
            for i in range(4, 8):
                if (self.pred_domcekom[i] is True and (self.pozicia[i] + hodene > 18)) or (
                        self.pozicia[i] == 0 and hodene != 6):
                    c += 1
            if c == 4:
                self.help_vyhodnotenia(False)

            else:
                self.canvas.delete(self.info)
                self.info = self.canvas.create_text(950, 250, text="Click on figure to move",
                                                    font=('Copperplate Gothic Bold', 20), fill='white')
            self.canvas.update()
            self.canvas.tag_bind('red_figure_1', '<Button-1>', lambda event: self.check(4, hodene))
            self.canvas.tag_bind('red_figure_2', '<Button-1>', lambda event: self.check(5, hodene))
            self.canvas.tag_bind('red_figure_3', '<Button-1>', lambda event: self.check(6, hodene))
            self.canvas.tag_bind('red_figure_4', '<Button-1>', lambda event: self.check(7, hodene))

        elif self.hrac_na_rade == 3:
            c = 0
            for i in range(8, 12):
                if (self.pred_domcekom[i] is True and (self.pozicia[i] + hodene > 31)) or (
                        self.pozicia[i] == 0 and hodene != 6):
                    c += 1
            if c == 4:
                self.help_vyhodnotenia(False)

            else:
                self.canvas.delete(self.info)
                self.info = self.canvas.create_text(950, 250, text="Click on figure to move",
                                                    font=('Copperplate Gothic Bold', 20), fill='white')
            self.canvas.update()
            self.canvas.tag_bind('blue_figure_1', '<Button-1>', lambda event: self.check(8, hodene))
            self.canvas.tag_bind('blue_figure_2', '<Button-1>', lambda event: self.check(9, hodene))
            self.canvas.tag_bind('blue_figure_3', '<Button-1>', lambda event: self.check(10, hodene))
            self.canvas.tag_bind('blue_figure_4', '<Button-1>', lambda event: self.check(11, hodene))

        elif self.hrac_na_rade == 4:
            c = 0
            for i in range(12, 16):
                if (self.pred_domcekom[i] is True and (self.pozicia[i] + hodene > 44)) or (
                        self.pozicia[i] == 0 and hodene != 6):
                    c += 1
            if c == 4:
                self.help_vyhodnotenia(False)
            else:
                self.canvas.delete(self.info)
                self.info = self.canvas.create_text(950, 250, text="Click on figure to move",
                                                    font=('Copperplate Gothic Bold', 20), fill='white')
            self.canvas.update()
            self.canvas.tag_bind('yellow_figure_1', '<Button-1>', lambda event: self.check(12, hodene))
            self.canvas.tag_bind('yellow_figure_2', '<Button-1>', lambda event: self.check(13, hodene))
            self.canvas.tag_bind('yellow_figure_3', '<Button-1>', lambda event: self.check(14, hodene))
            self.canvas.tag_bind('yellow_figure_4', '<Button-1>', lambda event: self.check(15, hodene))

    def check(self, id, hodene):
        urobil = False
        if hodene == 6 and self.pozicia[id] == 0:
            self.pozicia[id] = self.pozicie_zaciatky[id]
            self.canvas.coords(self.figures[id], self.neutralne_policka[self.pozicie_zaciatky[id]][0],
                               self.neutralne_policka[self.pozicie_zaciatky[id]][1])
            self.canvas.update()
            urobil = True
            self.na_startovnom[id] = True
        elif self.pozicia[id] != 0 and self.hrac_na_rade == 1:
            if (self.pozicia[id] + hodene) <= 57:
                if 56 >= (self.pozicia[id] + hodene) >= 52:
                    self.less_figure_check(id)
                    self.pozicia[id] += hodene
                    self.canvas.coords(self.figures[id], self.cielove_zelene[self.pozicia[id]][0],
                                       self.cielove_zelene[self.pozicia[id]][1])
                    self.canvas.update()
                    urobil = True
                    self.pred_domcekom[id] = True
                    if self.na_startovnom[id] == True:
                        self.na_startovnom[id] = False
                elif (self.pozicia[id] + hodene) == 57:
                    self.less_figure_check(id)
                    self.pozicia[id] += hodene
                    self.canvas.coords(self.figures[id], self.uplny_ciel_zeleny[self.pozicia[id]][0],
                                       self.uplny_ciel_zeleny[self.pozicia[id]][1])
                    self.canvas.update()
                    urobil = True
                    self.pred_domcekom[id] = True
                    self.pocet_vo_finale[self.hrac_na_rade - 1] += 1
                    self.canvas.delete(self.finale[0])
                    self.finale[0] = self.canvas.create_text(340, 430, text=self.pocet_vo_finale[0],
                                                             font=('Copperplate Gothic Bold', 15))
                    self.canvas.update()
                    self.win_check()
                    if self.na_startovnom[id] == True:
                        self.na_startovnom[id] = False
                else:
                    self.less_figure_check(id)
                    self.pozicia[id] += hodene
                    self.canvas.coords(self.figures[id], self.neutralne_policka[self.pozicia[id]][0],
                                       self.neutralne_policka[self.pozicia[id]][1])
                    self.more_figures_check(id)
                    self.canvas.update()
                    urobil = True
                    if self.na_startovnom[id] == True:
                        self.na_startovnom[id] = False

        elif self.pozicia[id] != 0 and self.hrac_na_rade == 2:
            if self.pred_domcekom[id] is False:
                if self.pozicia[id] <= 12:
                    if 12 < (self.pozicia[id] + hodene) <= 17:
                        self.less_figure_check(id)
                        self.pozicia[id] += hodene
                        self.canvas.coords(self.figures[id], self.cielove_cervene[self.pozicia[id]][0],
                                           self.cielove_cervene[self.pozicia[id]][1])
                        self.canvas.update()
                        self.pred_domcekom[id] = True
                        urobil = True
                        if self.na_startovnom[id] is True:
                            self.na_startovnom[id] = False
                    elif (self.pozicia[id] + hodene) == 18:
                        self.less_figure_check(id)
                        self.pozicia[id] += hodene
                        self.canvas.coords(self.figures[id], self.uplny_ciel_cerveny[self.pozicia[id]][0],
                                           self.uplny_ciel_cerveny[self.pozicia[id]][1])
                        self.canvas.update()
                        self.pred_domcekom[id] = True
                        urobil = True
                        self.pocet_vo_finale[self.hrac_na_rade - 1] += 1
                        self.canvas.delete(self.finale[1])
                        self.finale[1] = self.canvas.create_text(430, 340, text=self.pocet_vo_finale[1],
                                                                 font=('Copperplate Gothic Bold', 15))
                        self.canvas.update()
                        self.win_check()
                        if self.na_startovnom[id] is True:
                            self.na_startovnom[id] = False
                    elif (self.pozicia[id] + hodene) <= 12:
                        self.less_figure_check(id)
                        self.pozicia[id] += hodene
                        self.canvas.coords(self.figures[id], self.neutralne_policka[self.pozicia[id]][0],
                                           self.neutralne_policka[self.pozicia[id]][1])
                        self.more_figures_check(id)
                        self.canvas.update()
                        urobil = True
                        if self.na_startovnom[id] is True:
                            self.na_startovnom[id] = False
                elif self.pozicia[id] > 12:
                    if (self.pozicia[id] + hodene) > 52:
                        self.less_figure_check(id)
                        self.pozicia[id] = ((self.pozicia[id] + hodene) - 52)
                        self.canvas.coords(self.figures[id], self.neutralne_policka[self.pozicia[id]][0],
                                           self.neutralne_policka[self.pozicia[id]][1])
                        self.more_figures_check(id)
                        self.canvas.update()
                        urobil = True
                        if self.na_startovnom[id] == True:
                            self.na_startovnom[id] = False
                    else:
                        self.less_figure_check(id)
                        self.pozicia[id] += hodene
                        self.canvas.coords(self.figures[id], self.neutralne_policka[self.pozicia[id]][0],
                                           self.neutralne_policka[self.pozicia[id]][1])
                        self.more_figures_check(id)
                        self.canvas.update()
                        urobil = True
                        if self.na_startovnom[id] == True:
                            self.na_startovnom[id] = False

            elif self.pred_domcekom[id] is True:
                if (self.pozicia[id] + hodene) <= 17:
                    self.less_figure_check(id)
                    self.pozicia[id] += hodene
                    self.canvas.coords(self.figures[id], self.cielove_cervene[self.pozicia[id]][0],
                                       self.cielove_cervene[self.pozicia[id]][1])
                    self.canvas.update()
                    urobil = True
                elif (self.pozicia[id] + hodene) == 18:
                    self.less_figure_check(id)
                    self.pozicia[id] += hodene
                    self.canvas.coords(self.figures[id], self.uplny_ciel_cerveny[self.pozicia[id]][0],
                                       self.uplny_ciel_cerveny[self.pozicia[id]][1])
                    self.canvas.update()
                    urobil = True
                    self.pocet_vo_finale[self.hrac_na_rade - 1] += 1
                    self.canvas.delete(self.finale[1])
                    self.finale[1] = self.canvas.create_text(430, 340, text=self.pocet_vo_finale[1],
                                                             font=('Copperplate Gothic Bold', 15))
                    self.canvas.update()
                    self.win_check()

        elif self.pozicia[id] != 0 and self.hrac_na_rade == 3:
            if self.pred_domcekom[id] == False:
                if self.pozicia[id] <= 25:
                    if 25 < (self.pozicia[id] + hodene) <= 30:
                        self.less_figure_check(id)
                        self.pozicia[id] += hodene
                        self.canvas.coords(self.figures[id], self.celove_modre[self.pozicia[id]][0],
                                           self.celove_modre[self.pozicia[id]][1])
                        self.canvas.update()
                        self.pred_domcekom[id] = True
                        urobil = True
                        if self.na_startovnom[id] == True:
                            self.na_startovnom[id] = False
                    elif (self.pozicia[id] + hodene) == 31:
                        self.less_figure_check(id)
                        self.pozicia[id] += hodene
                        self.canvas.coords(self.figures[id], self.uplny_ciel_modry[self.pozicia[id]][0],
                                           self.uplny_ciel_modry[self.pozicia[id]][1])
                        self.canvas.update()
                        self.pred_domcekom[id] = True
                        urobil = True
                        self.pocet_vo_finale[self.hrac_na_rade - 1] += 1
                        self.canvas.delete(self.finale[2])
                        self.finale[2] = self.canvas.create_text(460, 430, text=self.pocet_vo_finale[2],
                                                                 font=('Copperplate Gothic Bold', 15))
                        self.canvas.update()
                        self.win_check()

                        if self.na_startovnom[id] == True:
                            self.na_startovnom[id] = False
                    elif (self.pozicia[id] + hodene) <= 25:
                        self.less_figure_check(id)
                        self.pozicia[id] += hodene
                        self.canvas.coords(self.figures[id], self.neutralne_policka[self.pozicia[id]][0],
                                           self.neutralne_policka[self.pozicia[id]][1])
                        self.more_figures_check(id)
                        self.canvas.update()
                        urobil = True
                        if self.na_startovnom[id] == True:
                            self.na_startovnom[id] = False
                elif self.pozicia[id] > 25:
                    if (self.pozicia[id] + hodene) > 52:
                        self.less_figure_check(id)
                        self.pozicia[id] = ((self.pozicia[id] + hodene) - 52)
                        self.canvas.coords(self.figures[id], self.neutralne_policka[self.pozicia[id]][0],
                                           self.neutralne_policka[self.pozicia[id]][1])
                        self.more_figures_check(id)
                        self.canvas.update()
                        urobil = True
                        if self.na_startovnom[id] == True:
                            self.na_startovnom[id] = False
                    else:
                        self.less_figure_check(id)
                        self.pozicia[id] += hodene
                        self.canvas.coords(self.figures[id], self.neutralne_policka[self.pozicia[id]][0],
                                           self.neutralne_policka[self.pozicia[id]][1])
                        self.more_figures_check(id)
                        self.canvas.update()
                        urobil = True
                        if self.na_startovnom[id] == True:
                            self.na_startovnom[id] = False
            elif self.pred_domcekom[id] is True:
                if (self.pozicia[id] + hodene) <= 30:
                    self.less_figure_check(id)
                    self.pozicia[id] += hodene
                    self.canvas.coords(self.figures[id], self.celove_modre[self.pozicia[id]][0],
                                       self.celove_modre[self.pozicia[id]][1])
                    self.canvas.update()
                    urobil = True
                elif (self.pozicia[id] + hodene) == 31:
                    self.less_figure_check(id)
                    self.pozicia[id] += hodene
                    self.canvas.coords(self.figures[id], self.uplny_ciel_modry[self.pozicia[id]][0],
                                       self.uplny_ciel_modry[self.pozicia[id]][1])
                    self.canvas.update()
                    urobil = True
                    self.pocet_vo_finale[self.hrac_na_rade - 1] += 1
                    self.canvas.delete(self.finale[2])
                    self.finale[2] = self.canvas.create_text(460, 430, text=self.pocet_vo_finale[2],
                                                             font=('Copperplate Gothic Bold', 15))
                    self.canvas.update()
                    self.win_check()

        elif self.pozicia[id] != 0 and self.hrac_na_rade == 4:
            if self.pred_domcekom[id] == False:
                if self.pozicia[id] <= 38:
                    if 38 < (self.pozicia[id] + hodene) <= 43:
                        self.less_figure_check(id)
                        self.pozicia[id] += hodene
                        self.canvas.coords(self.figures[id], self.celove_zlte[self.pozicia[id]][0],
                                           self.celove_zlte[self.pozicia[id]][1])
                        self.canvas.update()
                        self.pred_domcekom[id] = True
                        urobil = True
                        if self.na_startovnom[id] == True:
                            self.na_startovnom[id] = False
                    elif (self.pozicia[id] + hodene) == 44:
                        self.less_figure_check(id)
                        self.pozicia[id] += hodene
                        self.canvas.coords(self.figures[id], self.uplny_ciel_zlty[self.pozicia[id]][0],
                                           self.uplny_ciel_zlty[self.pozicia[id]][1])
                        self.canvas.update()
                        self.pred_domcekom[id] = True
                        urobil = True
                        self.pocet_vo_finale[self.hrac_na_rade - 1] += 1
                        self.canvas.delete(self.finale[3])
                        self.finale[3] = self.canvas.create_text(430, 460, text=self.pocet_vo_finale[3],
                                                                 font=('Copperplate Gothic Bold', 15))
                        self.canvas.update()
                        self.win_check()
                        if self.na_startovnom[id] == True:
                            self.na_startovnom[id] = False
                    elif (self.pozicia[id] + hodene) <= 38:
                        self.less_figure_check(id)
                        self.pozicia[id] += hodene
                        self.canvas.coords(self.figures[id], self.neutralne_policka[self.pozicia[id]][0],
                                           self.neutralne_policka[self.pozicia[id]][1])
                        self.more_figures_check(id)
                        self.canvas.update()
                        urobil = True
                        if self.na_startovnom[id] == True:
                            self.na_startovnom[id] = False
                elif self.pozicia[id] > 38:
                    if (self.pozicia[id] + hodene) > 52:
                        self.less_figure_check(id)
                        self.pozicia[id] = ((self.pozicia[id] + hodene) - 52)
                        self.canvas.coords(self.figures[id], self.neutralne_policka[self.pozicia[id]][0],
                                           self.neutralne_policka[self.pozicia[id]][1])
                        self.more_figures_check(id)
                        self.canvas.update()
                        urobil = True
                        if self.na_startovnom[id] == True:
                            self.na_startovnom[id] = False
                    else:
                        self.less_figure_check(id)
                        self.pozicia[id] += hodene
                        self.canvas.coords(self.figures[id], self.neutralne_policka[self.pozicia[id]][0],
                                           self.neutralne_policka[self.pozicia[id]][1])
                        self.more_figures_check(id)
                        self.canvas.update()
                        urobil = True
                        if self.na_startovnom[id] == True:
                            self.na_startovnom[id] = False
            elif self.pred_domcekom[id] is True:
                if (self.pozicia[id] + hodene) <= 43:
                    self.less_figure_check(id)
                    self.pozicia[id] += hodene
                    self.canvas.coords(self.figures[id], self.celove_zlte[self.pozicia[id]][0],
                                       self.celove_zlte[self.pozicia[id]][1])
                    self.canvas.update()
                    urobil = True
                elif (self.pozicia[id] + hodene) == 44:
                    self.less_figure_check(id)
                    self.pozicia[id] += hodene
                    self.canvas.coords(self.figures[id], self.uplny_ciel_zlty[self.pozicia[id]][0],
                                       self.uplny_ciel_zlty[self.pozicia[id]][1])
                    self.canvas.update()
                    urobil = True
                    self.pocet_vo_finale[self.hrac_na_rade - 1] += 1
                    self.canvas.delete(self.finale[3])
                    self.finale[3] = self.canvas.create_text(430, 460, text=self.pocet_vo_finale[3],
                                                             font=('Copperplate Gothic Bold', 15))
                    self.canvas.update()
                    self.win_check()

        if urobil is True:
            self.can_kill(id)
            if hodene == 6:
                self.help_vyhodnotenia(True)
            else:
                self.help_vyhodnotenia(False)

    def help_vyhodnotenia(self, can):
        self.canvas.tag_bind('green_figure_1', '<Button-1>', lambda event: None)
        self.canvas.tag_bind('green_figure_2', '<Button-1>', lambda event: None)
        self.canvas.tag_bind('green_figure_3', '<Button-1>', lambda event: None)
        self.canvas.tag_bind('green_figure_4', '<Button-1>', lambda event: None)
        self.canvas.tag_bind('red_figure_1', '<Button-1>', lambda event: None)
        self.canvas.tag_bind('red_figure_2', '<Button-1>', lambda event: None)
        self.canvas.tag_bind('red_figure_3', '<Button-1>', lambda event: None)
        self.canvas.tag_bind('red_figure_4', '<Button-1>', lambda event: None)
        self.canvas.tag_bind('blue_figure_1', '<Button-1>', lambda event: None)
        self.canvas.tag_bind('blue_figure_2', '<Button-1>', lambda event: None)
        self.canvas.tag_bind('blue_figure_3', '<Button-1>', lambda event: None)
        self.canvas.tag_bind('blue_figure_4', '<Button-1>', lambda event: None)
        self.canvas.tag_bind('yellow_figure_1', '<Button-1>', lambda event: None)
        self.canvas.tag_bind('yellow_figure_2', '<Button-1>', lambda event: None)
        self.canvas.tag_bind('yellow_figure_3', '<Button-1>', lambda event: None)
        self.canvas.tag_bind('yellow_figure_4', '<Button-1>', lambda event: None)

        if can is False:
            if self.hrac_na_rade == self.num_of_players.get():
                self.hrac_na_rade = 1
            else:
                self.hrac_na_rade += 1
            self.canvas.after(500)
            self.canvas.delete(self.whoisnext)
            self.canvas.delete(self.info)
            self.canvas.update()
            self.whoisnext = self.canvas.create_text(950, 200,
                                                     text=str(self.player_names[self.hrac_na_rade - 1]) + "'s turn",
                                                     font=('Copperplate Gothic Bold', 25), fill='white')
            self.info = self.canvas.create_text(950, 250, text="Roll the dice", font=('Copperplate Gothic Bold', 20),
                                                fill='white')
            self.canvas.update()
            self.hodkockou.configure(state='normal')
        elif can is True:
            self.canvas.delete(self.info)
            self.info = self.canvas.create_text(950, 250, text="Roll the dice", font=('Copperplate Gothic Bold', 20),
                                                fill='white')
            self.canvas.update()
            self.hodkockou.configure(state='normal')

    def can_kill(self, id):
        vyhodeni_hraci = []
        if self.hrac_na_rade == 1:
            for i in range(4, 16):
                if (self.pozicia[id] == self.pozicia[i]) and (self.pred_domcekom[i] is False) and (
                        self.na_startovnom[i] is False) and (self.pred_domcekom[id] is False):
                    vyhodeni_hraci.append(i)
            self.kill(id, vyhodeni_hraci)

        elif self.hrac_na_rade == 2:
            for i in range(0, 4):
                if (self.pozicia[id] == self.pozicia[i]) and (self.pred_domcekom[i] is False) and (
                        self.na_startovnom[i] is False) and (self.pred_domcekom[id] is False):
                    vyhodeni_hraci.append(i)
            for i in range(8, 16):
                if (self.pozicia[id] == self.pozicia[i]) and (self.pred_domcekom[i] is False) and (
                        self.na_startovnom[i] is False) and (self.pred_domcekom[id] is False):
                    vyhodeni_hraci.append(i)
            self.kill(id, vyhodeni_hraci)

        elif self.hrac_na_rade == 3:
            for i in range(0, 8):
                if (self.pozicia[id] == self.pozicia[i]) and (self.pred_domcekom[i] is False) and (
                        self.na_startovnom[i] is False) and (self.pred_domcekom[id] is False):
                    vyhodeni_hraci.append(i)
            for i in range(12, 16):
                if (self.pozicia[id] == self.pozicia[i]) and (self.pred_domcekom[i] is False) and (
                        self.na_startovnom[i] is False) and (self.pred_domcekom[id] is False):
                    vyhodeni_hraci.append(i)
            self.kill(id, vyhodeni_hraci)

        elif self.hrac_na_rade == 4:
            for i in range(0, 12):
                if (self.pozicia[id] == self.pozicia[i]) and (self.pred_domcekom[i] is False) and (
                        self.na_startovnom[i] is False) and (self.pred_domcekom[id] is False):
                    vyhodeni_hraci.append(i)
            self.kill(id, vyhodeni_hraci)

    def kill(self, id, vyhodeni_hraci):
        for i in range(len(vyhodeni_hraci)):
            self.pozicia[vyhodeni_hraci[i]] = 0
            self.canvas.coords(self.figures[vyhodeni_hraci[i]], self.pozicie_domceky[vyhodeni_hraci[i]][0],
                               self.pozicie_domceky[vyhodeni_hraci[i]][1])
            self.less_figure_check(id)
            self.canvas.update()
            self.kills[self.hrac_na_rade - 1] += 1

    def more_figures_check(self, id):
        zdvojeni_hraci = []
        zdvojeni_hraci.append(id)
        pocty = [0, 0, 0, 0]
        for i in range(len(self.pozicia)):
            if (self.pozicia[i] == self.pozicia[id]) and (self.pred_domcekom[i] is False):
                if i <= 3:
                    pocty[0] += 1
                elif i <= 7:
                    pocty[1] += 1
                elif i <= 11:
                    pocty[2] += 1
                elif i <= 15:
                    pocty[3] += 1
        c = 0
        for i in range(len(pocty)):
            if pocty[i] > 0:
                c += 1
        if c > 1:
            for i in range(len(self.pozicia)):
                if (self.pozicia[i] == self.pozicia[id]) and (self.pred_domcekom[i] is False):
                    if i <= 3:
                        self.canvas.coords(self.figures[i], self.neutralne_policka[self.pozicia[id]][0] - 12.5,
                                           self.neutralne_policka[self.pozicia[id]][1] + 12.5)
                    elif i <= 7:
                        self.canvas.coords(self.figures[i], self.neutralne_policka[self.pozicia[id]][0] + 12.5,
                                           self.neutralne_policka[self.pozicia[id]][1] + 12.5)
                    elif i <= 11:
                        self.canvas.coords(self.figures[i], self.neutralne_policka[self.pozicia[id]][0] - 12.5,
                                           self.neutralne_policka[self.pozicia[id]][1] - 12.5)
                    elif i <= 15:
                        self.canvas.coords(self.figures[i], self.neutralne_policka[self.pozicia[id]][0] + 12.5,
                                           self.neutralne_policka[self.pozicia[id]][1] - 12.5)
            if id <= 3:
                self.canvas.coords(self.figures[id], self.neutralne_policka[self.pozicia[id]][0] - 12.5,
                                   self.neutralne_policka[self.pozicia[id]][1] + 12.5)
            elif id <= 7:
                self.canvas.coords(self.figures[id], self.neutralne_policka[self.pozicia[id]][0] + 12.5,
                                   self.neutralne_policka[self.pozicia[id]][1] + 12.5)
            elif id <= 11:
                self.canvas.coords(self.figures[id], self.neutralne_policka[self.pozicia[id]][0] - 12.5,
                                   self.neutralne_policka[self.pozicia[id]][1] - 12.5)
            elif id <= 15:
                self.canvas.coords(self.figures[id], self.neutralne_policka[self.pozicia[id]][0] + 12.5,
                                   self.neutralne_policka[self.pozicia[id]][1] - 12.5)
            self.canvas.update()

    def less_figure_check(self, id):
        pocty = [0, 0, 0, 0]
        for i in range(len(self.pozicia)):
            if (self.pozicia[i] == self.pozicia[id]) and (self.pred_domcekom[i] is False) and (i != id):
                if i <= 3:
                    pocty[0] += 1
                elif i <= 7:
                    pocty[1] += 1
                elif i <= 11:
                    pocty[2] += 1
                elif i <= 15:
                    pocty[3] += 1
        c = 0
        for i in range(len(pocty)):
            if pocty[i] > 0:
                c += 1
        if c <= 1:
            for i in range(len(self.pozicia)):
                if (self.pozicia[i] == self.pozicia[id]) and (self.pred_domcekom[i] is False):
                    self.canvas.coords(self.figures[i], self.neutralne_policka[self.pozicia[id]][0],
                                       self.neutralne_policka[self.pozicia[id]][1])

    def zapis(self, id):
        with open("./data/the_most_wins.txt", "r") as f:
            data = f.read()
        data = data.split()

        data[id] = int(data[id])
        data[id] += 1
        data[id] = str(data[id])
        data = " ".join(data)
        with open("./data/the_most_wins.txt", "w") as f:
            f.write(data)
        with open("./data/previous_games.txt", "r") as f:
            data = f.read()
        data += "\n" + "/ ".join(self.player_names) + "/ " + self.player_names[id] + " " + self.colors[id] + " " + str(
            self.kills[id])
        with open("./data/previous_games.txt", "w") as f:
            f.write(data)

    def win_check(self):
        for i in range(0, 4):
            if self.pocet_vo_finale[i] == 4:
                self.zapis(i)
                self.canvas.destroy()
                EndScreen(i, self.player_names)


class EndScreen:
    def __init__(self, hrac, player_names):
        self.endscreen = tkinter.Canvas()
        self.endscreen.pack()
        self.endscreen.configure(width=750, height=750)
        self.picture_load()
        self.mala_f = [self.mala_f_green, self.mala_f_red, self.mala_f_blue, self.mala_f_yellow]
        self.colours = [self.colours_green, self.colours_red, self.colours_blue, self.colours_yellow]

        self.endscreen.create_image(375, 375, image=self.background_obrazok)

        self.endscreen.create_text(350, 75, text=player_names[hrac] + " wins the game!",
                                   font=('Comic Sans MS', 40, "bold"), fill="white")
        self.endscreen.create_image(375, 250, image=self.colours[hrac])
        self.endscreen.create_line(25, 550, 725, 550, fill='grey', width=5)
        self.endscreen.create_text(150, 570, text="The most wins as a colour:", font=('Comic Sans MS', 15, "bold"),
                                   fill="white")
        self.endscreen.create_image(150, 650, image=self.mala_f[self.position])
        self.endscreen.create_text(525, 600, text="The last 5 games", font=('Comic Sans MS', 20, "bold"),
                                   fill="black")
        self.endscreen.create_text(500, 625,
                                   text="(Name1/Name2/Name3/Name4/Winner/Colour/Number of kills)",
                                   font=('Comic Sans MS', 11, "bold"),
                                   fill="black")
        self.endscreen.create_text(475, 700,
                                   text=self.retazec,
                                   font=('Comic Sans MS', 11, "bold"),
                                   fill="white")

        self.button = Button(text="QUIT", command=self.submit, bg="red", activebackground="red",
                             relief=tkinter.RAISED, bd=2, width=12, height=3, fg="white")
        self.button.place(anchor=CENTER, x=375, y=500)

        self.endscreen.mainloop()

    def picture_load(self):
        figure_otvor = Image.open('./pictures/BLUE-final.png')
        figure_otvor = figure_otvor.resize((75, 100))
        self.mala_f_blue = ImageTk.PhotoImage(figure_otvor)
        figure_otvor = figure_otvor.resize((225, 275))
        self.colours_blue = ImageTk.PhotoImage(figure_otvor)
        figure_otvor.close()

        figure_otvor = Image.open('./pictures/GREEN-final.png')
        figure_otvor = figure_otvor.resize((75, 100))
        self.mala_f_green = ImageTk.PhotoImage(figure_otvor)
        figure_otvor = figure_otvor.resize((225, 275))
        self.colours_green = ImageTk.PhotoImage(figure_otvor)
        figure_otvor.close()

        figure_otvor = Image.open('./pictures/RED-final.png')
        figure_otvor = figure_otvor.resize((75, 100))
        self.mala_f_red = ImageTk.PhotoImage(figure_otvor)
        figure_otvor = figure_otvor.resize((225, 275))
        self.colours_red = ImageTk.PhotoImage(figure_otvor)
        figure_otvor.close()

        figure_otvor = Image.open('./pictures/YELLOW-final.png')
        figure_otvor = figure_otvor.resize((75, 100))
        self.mala_f_yellow = ImageTk.PhotoImage(figure_otvor)
        figure_otvor = figure_otvor.resize((225, 275))
        self.colours_yellow = ImageTk.PhotoImage(figure_otvor)
        figure_otvor.close()

        background = Image.open('./pictures/menu2.png')
        background = background.resize((750, 750))
        self.background_obrazok = ImageTk.PhotoImage(background)
        background.close()

        with open("./data/the_most_wins.txt", "r") as f:
            data = f.read()
        data = data.split()
        highest = 0
        self.position = None
        for i in range(len(data)):
            if int(data[i]) > highest:
                self.position = i

        self.retazec = ''
        with open('./data/previous_games.txt', 'r') as f:
            lines = f.readlines()
            num_lines = len(lines)
            for i in range(num_lines - 5, num_lines):
                self.retazec += lines[i]

    def submit(self):
        sys.exit()


Clovece()
