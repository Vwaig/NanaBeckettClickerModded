import pygame
import ctypes
import math
import ast
import time
from threading import Thread
from collections import Counter

#--------------------------------------------------------------------------#
#--------------------------------------------------------------------------#
#| |       _   _                      ____    __  __           _        | |#
#| |      | \ | | __ _ _ __   __ _   | __ )  |  \/  | ___   __| |       | |#
#| |      |  \| |/ _` | '_ \ / _` |  |  _ \  | |\/| |/ _ \ / _` |       | |#
#| |      | |\  | (_| | | | | (_| |  | |_) | | |  | | (_) | (_| |       | |#
#| |      |_| \_|\__,_|_| |_|\__,_|  |____/  |_|  |_|\___/ \__,_|       | |#
#| |                                                                    | |#
#--------------------------------------------------------------------------#
#                          Status - Up to date                             #
#--------------------------------------------------------------------------#

#'ClickValue' is the amount of currency per click
#Default = 1

ClickValue = 1

#--------------------------------------------------------------------------#

#'AutoSpeed_Draw' is the speed of the 'Draw' auto clicker
#Default = 0.2

AutoSpeed_Draw = 0.2

#--------------------------------------------------------------------------#

#'AutoSpeed_Tree' is the speed of the 'Draw' auto clicker
#Default = 1

AutoSpeed_Tree = 1

#--------------------------------------------------------------------------#

#'AutoSpeed_Cave' is the speed of the 'Draw' auto clicker
#Default = 10

AutoSpeed_Cave = 10

#--------------------------------------------------------------------------#

#'BackgroundCustom' will change the background colour/style
# 1 = Default
# 2 = White
# 3 = Black
# 4 = Rainbow

BackgroundCustom = 1

#--------------------------------------------------------------------------#

#'CurrencyDisplayName' is the name of the currency displayed
#Default = 'Nana's Silver Spoons'

CurrencyDisplayName = "Nana's Silver Spoons"

#--------------------------------------------------------------------------#

#'GuiQuality' Changes the default gui with an improved gui
# 0 = Default
# 1 = Improved quality

GuiQuality = 0

#--------------------------------------------------------------------------#
#--------------------------------------------------------------------------#
#--------------------------------------------------------------------------#
#--------------------------------------------------------------------------#
#                                                                          #                       
#                            __  __           _                            #                      
#                          |  \/  | ___   __| |                            #                
#                          | |\/| |/ _ \ / _` |                            #
#                          | |  | | (_) | (_| |                            #
#                          |_|  |_|\___/ \__,_|                            #
#                                                                          #
#                             _                                            #
#                            | |__  _   _                                  #
#                            | '_ \| | | |                                 #
#                            | |_) | |_| |                                 #
#                            |_.__/ \__, |                                 #
#                                   |___/                                  #
#       __  __                                                             #
#      /\ \/\ \                                   __                       #
#      \ \ \ \ \      __  __  __         __      /\_\       __             # 
#       \ \ \ \ \    /\ \/\ \/\ \     /'__`\    \/\ \      /'_ `\          #
#        \ \ \_/ \   \ \ \_/ \_/ \   /\ \L\.\_   \ \ \    /\ \L\ \         #
#         \ `\___/    \ \___x___/'   \ \__/.\_\   \ \_\   \ \____ \        # 
#          `\/__/      \/__//__/      \/__/\/_/    \/_/    \/___L\ \       #
#                                                            /\____/       #
#                                                            \_/__/        #
#                                                                          #
#--------------------------------------------------------------------------#
#--------------------------------------------------------------------------#
#--------------------------------------------------------------------------#
#--------------------------------------------------------------------------#
user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
sx, sy = screensize
screen_middle = (sx / 2, sy / 2)
# pygame stuff
win = pygame.display.set_mode((screensize))
pygame.display.set_caption("Clicker")

pygame.init()

clock = pygame.time.Clock()

WidthLine = 0

if GuiQuality == 0:
    WidthLine = 5
    XLine = 250
else:
    WidthLine = 2
    XLine = 265.1

# Load Start Up
if BackgroundCustom == 1:
    background_small = pygame.image.load("images/Backgrounds/background.png")
elif BackgroundCustom == 2:
    background_small = pygame.image.load("images/Backgrounds/background2.png")
elif BackgroundCustom == 3:
    background_small = pygame.image.load("images/Backgrounds/background3.png")
elif BackgroundCustom == 4:
    background_small = pygame.image.load("images/Backgrounds/background4.gif")
else:
    background_small = pygame.image.load("images/Backgrounds/background_error.png")   
background = pygame.transform.scale(background_small, screensize)
win.blit(background,(0, 0))
pygame.display.update()

# Load Images
nana_bek_small = pygame.image.load("images/Nana_bek.png")
nana_bek = pygame.transform.scale(nana_bek_small, (462, 561))
nana_bek_rect = nana_bek.get_rect()
x, y = screen_middle
nana_bek_rect.move_ip(x - 231, y - 280.5)

nana_click = pygame.image.load("images/click.png")
nana_click = pygame.transform.scale(nana_click, (23, 28))


# Load Auto Images
if GuiQuality == 0:
    auto_title_img = pygame.image.load("images/Autos/Title.png")
else:
    auto_title_img = pygame.image.load("images/Autos/Title2.png")

if GuiQuality == 0:
    auto_spoon_draw_img = pygame.image.load("images/Autos/spoon_draw.png")
    auto_spoon_tree_img = pygame.image.load("images/Autos/spoon_tree.png")
    auto_spoon_cave_img = pygame.image.load("images/Autos/spoon_cave.png")
else:
    auto_spoon_draw_img = pygame.image.load("images/Autos/spoon_draw2.png")
    auto_spoon_tree_img = pygame.image.load("images/Autos/spoon_tree2.png")
    auto_spoon_cave_img = pygame.image.load("images/Autos/spoon_cave2.png")
  
# def stuff
balance = 0



# Encoding and Decoding for money and other stored Data
code = [10, "abcdefghijklmnopqrstuvwxyz0123456789+-. _*/\[](){},':;!@$฿%^&<>?=~`"] # character code

def encode(val, charset):
    encoded = ""
    for idx in range(len(str(val))):
        tempEnc = encoded
        encoded = tempEnc + str(charset[0] + charset[1].index(str(val[idx])))
    return encoded


def decode(val, charset):
    charNum = 0
    decoded = ""
    for index in range(math.ceil(len(str(val)) / 2)):
        idy = str(val)[charNum] + str(val)[charNum + 1]
        charNum += 2
        tempDc = decoded
        decoded = tempDc + charset[1][int(idy) - 10]
    return decoded

def set_text(string, coordx, coordy, fontSize): #Function to set text

    font = pygame.font.Font('freesansbold.ttf', fontSize)
    text = font.render(string, True, (0, 0, 0))
    textRect = text.get_rect()
    textRect.center = (coordx, coordy)
    return (text, textRect)

# Define Autos / Buildings / do clicking for you

class Autos():
    def __init__(self, datalist):
        total,  autos_all, name = datalist
        autos_stuff = datalist[1]
        self.total_autos = int(total)
        self.tautos = 0
        self.autos = autos_all
        self.autos_xy = []
        self.auto_data = []

        # Set all upgrades to 1
        self.up_spoon_tree = 1
        self.up_spoon_draw = 1
        self.up_spoon_cave = 1



        self.auto_rects = []
        self.username = name

        print("Auto Class Made")

    def New_Auto(self, Name, Cost, NSPps): # image files must be 50 x 50 pixels and JUST say the image name aka Clicker.png
        global sx
        y_coord = self.tautos * 50
        x_coord = sx - XLine
        self.autos_xy.append((Name, Cost, x_coord, y_coord))
        self.auto_data.append((Name, NSPps, Cost))
        self.tautos += 1
        x_pos = x_coord
        y_pos = y_coord
        height = 50
        width = 50
        
        # make the rectangle variable
        rectangle = pygame.Rect(x_pos, y_pos, width, height)
        self.auto_rects.append(rectangle)
        print("Generated New Auto Named '" + Name + "', Costing: " + str(Cost) + " Silver Spoons")
    

    def BLIT(self):


        for auto in self.autos_xy:
            N, C, x, y = auto

            if N == "title":
                win.blit(auto_title_img, (x, y))
            if N == "spoon_draw":
                win.blit(auto_spoon_draw_img, (x, y))
                s = set_text(str(C), sx - 150, y + 25, 20)
                win.blit(s[0], s[1])
                s = set_text(str(self.autos.count("spoon_draw")), sx - 50, y + 25, 20)
                win.blit(s[0], s[1])
            if N == "spoon_tree":
                win.blit(auto_spoon_tree_img, (x,y))
                s = set_text(str(C), sx - 150, y + 25, 20)
                win.blit(s[0], s[1])
                s = set_text(str(self.autos.count("spoon_tree")), sx - 50, y + 25, 20)
                win.blit(s[0], s[1])
            if N == "spoon_cave":
                win.blit(auto_spoon_cave_img, (x, y))
                s = set_text(str(C), sx - 150, y + 25, 20)
                win.blit(s[0], s[1])
                s = set_text(str(self.autos.count("spoon_cave")), sx - 50, y + 25, 20)
                win.blit(s[0], s[1])


            if not y == 0:
                pygame.draw.line(win, (0, 0 ,0), (sx - 100, y), (sx - 100, y + 50), int(WidthLine))


    def check_click(self, x, y):
        max_x, max_y = screensize
        if nana_bek_rect.collidepoint(x, y): # quickly check they are not just clicking for spoons to save some time.
            pass
        else:

            i = 0
            for button in self.auto_rects:
                if button.collidepoint(x, y):
                    Clicked = i

                i += 1
            try:
                i += Clicked # Test if Anything Is clicked
                name, NSSps, Cost = self.auto_data[Clicked]
                global balance
                if name == "spoon_draw":
                    if balance >= Cost:
                        balance -= Cost
                        self.autos.append("spoon_draw")
                        self.total_autos += 1
                if name == "spoon_tree":
                    if balance >= Cost:
                        balance -= Cost
                        self.autos.append("spoon_tree")
                        self.total_autos += 1
                if name == "spoon_cave":
                    if balance >= Cost:
                        balance -= Cost
                        self.autos.append("spoon_cave")
                        self.total_autos += 1




            except Exception as e:
                #print(e)
                pass

    def Get_Data(self):
        data_list = [self.total_autos, self.autos, self.username]
        return data_list

    def Tick(self):
        global balance
        tickrate = 20
        for auto in self.autos:
            if auto == "spoon_draw":
                balance += (AutoSpeed_Draw * self.up_spoon_draw) / tickrate

            if auto == "spoon_tree":
                balance += (AutoSpeed_Tree * self.up_spoon_tree) / tickrate

            if auto == "spoon_cave":
                balance += (AutoSpeed_Cave * self.up_spoon_tree) / tickrate



    def Check_Other(self):
        # check for milestones
        self.milestones = ["1000spoon", "1234"]

# How To Add A Auto:
# 1) Call The New_Auto function,
# 2) make 50 by 50 pixel image and call it the correct name,
# 3) Add it to check_click and BLIT and Tick functions,
# 4) Add A self.up_NAME to the .init function.


def save(auto):
    # Save Money
    global balance
    cbalance = balance.__round__()
    encoded = encode(str(cbalance), code)
    f = open("Data/money.txt", "w")
    f.write(encoded)
    f.close()

    # Save Data On Autos
    data = auto.Get_Data()
    encoded = encode(str(data), code)
    f = open("Data/datalist.txt", "w")
    f.write(encoded)
    f.close()






def display_info(balance):
    global screen_middle
    balance = balance.__round__()
    x = screen_middle[0]
    if balance <= 1:
        bal = str(balance) + " " + CurrencyDisplayName
    else:
        bal = str(balance) + " " + CurrencyDisplayName
    s = set_text(bal, x, 100, 20)
    win.blit(s[0], s[1])


def clicked_animation_handler(mouse_x, mouse_y):
    for i in range(0, 800):
        ii = i // 8
        win.blit(nana_click, (mouse_x, mouse_y - ii))
        time.sleep(0.00001)


# Getting All Needed Data For Game. - MAIN BRANCH

# Get / Decode Money - SUB BRANCH
money_file = open("Data/money.txt", "r")
balance_encoded = money_file.read()
money_file.close()
balance = decode(balance_encoded, code)
balance = float(balance).__round__()
balance = int(balance)

data_f = open("Data/datalist.txt")
data = data_f.read()
data_f.close()
datafile = decode(data, code)
datafile = ast.literal_eval(datafile)

# Init Autos
auto = Autos(datafile)

# Generate Autos - They Will Appear top to bottom in the order that they are here. - No Caps In Names
auto.New_Auto("title", 0, 0)
auto.New_Auto("spoon_draw", 10, 0.1)
auto.New_Auto("spoon_tree", 100, 1)
auto.New_Auto("spoon_cave", 1500, 10)


# Tests Before Game Loads


save(auto)


run = True
TICKS = 0
while run:
    win.blit(background,(0, 0))
    win.blit(nana_bek, nana_bek_rect)
    auto.BLIT()
    auto.Tick()
    display_info(balance)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # Detect If nana Is Clicked
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_presses = pygame.mouse.get_pressed()
            if mouse_presses[0]:
                x, y = pygame.mouse.get_pos()
                if nana_bek_rect.collidepoint(x, y):
                    balance += ClickValue
                    thread = Thread(target=clicked_animation_handler, args=(x,y))
                    thread.start()
                auto.check_click(x, y)

    pygame.display.flip()
    clock.tick(20) # finsih tick
    TICKS += 1
    if TICKS >= 100:
        save(auto)
        auto.Check_Other()
        TICKS = 0

pygame.quit()
