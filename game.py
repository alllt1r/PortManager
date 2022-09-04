import re

import pygame
import sys
import serial.tools.list_ports
from tkinter import *
from tkinter import messagebox

Tk().wm_withdraw()  # to hide the main window

FPS = 60
WIN_WIDTH = 300
WIN_HEIGHT = 270
BACKGROUND_COLOR = (37, 37, 38)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
TEXT_COLOR = (255, 255, 255)
COLOR_LIST_INACTIVE = (51, 51, 55)
COLOR_LIST_ACTIVE = (34, 83, 118)
COLOR_SLIDER_INACTIVE = (51, 51, 55)
COLOR_SLIDER_ACTIVE = (34, 83, 118)
COLOR_SLIDER_BOX = (6, 106, 174)
COLOR_BUTTON_INACTIVE = (51, 51, 55)
COLOR_BUTTON_ACTIVE = (34, 83, 118)
COLOR_BUTTON_PRESSED = (49, 98, 133)
COLOR_INDICATOR = (51, 51, 55)
COLOR_TITLE_BOX = (66, 66, 70)
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption('Port Manager')
programIcon = pygame.image.load('icon.png')
pygame.display.set_icon(programIcon)
screen.fill(BACKGROUND_COLOR)

MyFont = pygame.font.Font("PixelFont.ttf", 15)


class OptionBox:

    def __init__(self, x, y, w, h, main, color=COLOR_LIST_INACTIVE, highlight_color=COLOR_LIST_ACTIVE, font=MyFont,
                 option_list=None, selected=0):
        if option_list is None:
            option_list = []
        self.color = color
        self.highlight_color = highlight_color
        self.rect = pygame.Rect(x, y, w, h)
        self.font = font
        self.main = main
        self.option_list = option_list
        self.selected = selected
        self.draw_menu = False
        self.menu_active = False
        self.active_option = -1

    def draw(self, surface):
        if self.draw_menu:
            s = pygame.Surface((WIN_WIDTH, WIN_HEIGHT), pygame.SRCALPHA)  # per-pixel alpha
            s.fill((0, 0, 0, 25))  # notice the alpha value in the color
            surface.blit(s, (0, 0))
        pygame.draw.rect(surface, self.highlight_color if self.menu_active else self.color, self.rect)
        msg = self.font.render(self.main, True, TEXT_COLOR)
        pygame.draw.polygon(surface=screen, color=WHITE, points=[
            (self.rect.x + self.rect.w - self.rect.h + (self.rect.h / 3), self.rect.y + (self.rect.h / 3)),
            (self.rect.x + self.rect.w - self.rect.h + (self.rect.h / 3 * 2), self.rect.y + (self.rect.h / 3)),
            (self.rect.x + self.rect.w - self.rect.h + (self.rect.h / 2), self.rect.y + (self.rect.h / 3 * 2))])
        surface.blit(msg, (self.rect.x + 10, msg.get_rect(center=self.rect.center)[1]))

        if self.draw_menu:
            for element, text in enumerate(self.option_list):
                rect = self.rect.copy()
                rect.y += (element + 1) * self.rect.height
                pygame.draw.rect(surface, self.highlight_color if element == self.active_option else self.color, rect)
                msg = self.font.render(text, True, TEXT_COLOR)
                surface.blit(msg, (self.rect.x + 10, msg.get_rect(center=rect.center)[1]))

    def update(self, events):
        mouse_position = pygame.mouse.get_pos()
        self.menu_active = self.rect.collidepoint(mouse_position)

        self.active_option = -1
        for element in range(len(self.option_list)):
            rect = self.rect.copy()
            rect.y += (element + 1) * self.rect.height
            if rect.collidepoint(mouse_position):
                self.active_option = element
                break

        if not self.menu_active and self.active_option == -1:
            self.draw_menu = False

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.menu_active:
                    self.draw_menu = not self.draw_menu
                elif self.draw_menu and self.active_option >= 0:
                    self.selected = self.active_option
                    self.draw_menu = False
                    return self.active_option
        return -1

    def check(self):
        if self.menu_active is True or self.draw_menu is True:
            return "Menu"


class Slider:
    def __init__(self, x, y, w, h, box_w=12, position=0, font=MyFont):
        self.box_active = None
        self.slider_active = None
        self.rect = pygame.Rect(x, y, w, h)
        self.box_w = box_w
        self.box_rect = pygame.Rect(x + 3, y + 3, box_w, h - 3 - 3)
        self.font = font
        self.position = position
        self.isPressed = False
        self.min_x = x + 3
        self.max_x = x + w - box_w - 3

    def draw(self, surface):
        pygame.draw.rect(surface, COLOR_SLIDER_INACTIVE, self.rect)
        if self.slider_active is True or self.isPressed is True:
            pygame.draw.rect(surface, COLOR_SLIDER_ACTIVE, self.rect)
        pygame.draw.rect(surface, COLOR_SLIDER_BOX, self.box_rect)
        msg = self.font.render(str(self.position), True, TEXT_COLOR)
        surface.blit(msg, msg.get_rect(center=self.rect.center))

    def update(self, events, statement):
        if statement != "Menu":
            mouse_position = pygame.mouse.get_pos()
            self.slider_active = self.rect.collidepoint(mouse_position)
            self.box_active = self.box_rect.collidepoint(mouse_position)
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 or self.isPressed is True:
                    if self.slider_active is True or self.isPressed is True:
                        if self.max_x >= self.box_rect.x >= self.min_x:
                            self.isPressed = True
                            self.box_rect.x = pygame.mouse.get_pos()[0] - 5
                        if self.box_rect.x < self.min_x:
                            self.box_rect.x = self.min_x
                        if self.box_rect.x > self.max_x:
                            self.box_rect.x = self.max_x
                        self.position = round(
                            ((self.box_rect.x - self.min_x) * (255 - 0) / (self.max_x - self.min_x)) + 0)
                if event.type == pygame.MOUSEBUTTONUP:
                    self.isPressed = False
            return self.position


class Text:
    def __init__(self, x, y, text, font=MyFont, color=TEXT_COLOR):
        self.x = x
        self.y = y
        self.text = text
        self.font = font
        self.color = color

    def draw(self, surface):
        msg = self.font.render(str(self.text), True, self.color)
        surface.blit(msg, msg.get_rect(center=(self.x, self.y)))


class Button:
    def __init__(self, x, y, w, h, text, func=None, font=MyFont, color_inactive=COLOR_BUTTON_INACTIVE,
                 color_active=COLOR_BUTTON_ACTIVE, color_pressed=COLOR_BUTTON_PRESSED, pressed=False):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.font = font
        self.color_inactive = color_inactive
        self.color_active = color_active
        self.color_pressed = color_pressed
        self.pressed = pressed
        self.func = func
        self.button_active = False
        self.button_pressed = False

    def draw(self, surface):
        pygame.draw.rect(surface, self.color_inactive, self.rect)
        if self.button_active:
            pygame.draw.rect(surface, self.color_active, self.rect)
        if self.button_pressed:
            pygame.draw.rect(surface, self.color_pressed, self.rect)
            if self.pressed is False:
                self.button_pressed = False
        msg = self.font.render(str(self.text), True, TEXT_COLOR)
        surface.blit(msg, msg.get_rect(center=self.rect.center))

    def update(self, events):
        if stat != "Menu":
            mouse_position = pygame.mouse.get_pos()
            self.button_active = self.rect.collidepoint(mouse_position)
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.button_active:
                        if self.pressed:
                            self.func()
                        else:
                            self.button_pressed = not self.button_pressed

    def set_unpressed(self):
        self.button_pressed = False

    def set_pressed(self):
        self.button_pressed = True


class Indicator:
    def __init__(self, x, y, w, h, title_text, font=MyFont, color=COLOR_INDICATOR, color_box=COLOR_TITLE_BOX):
        self.rect = pygame.Rect(x, y, w, h)
        self.title_text = title_text
        self.font = font
        self.color = color
        self.color_box = color_box
        self.title_box = pygame.Rect(x + 5, y + h - 17 - 5, w - 10, 17)
        self.box_text = 0

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        msg = self.font.render(str(self.title_text), True, TEXT_COLOR)
        surface.blit(msg, (msg.get_rect(center=self.rect.center).x, self.rect.y + 4))
        pygame.draw.rect(surface, self.color_box, self.title_box)
        msg = self.font.render(str(self.box_text), True, TEXT_COLOR)
        surface.blit(msg, msg.get_rect(center=self.title_box.center))

class Circle:
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r
        self.color = GREEN

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.r)

    def set_green(self):
        self.color = GREEN

    def set_red(self):
        self.color = RED

def Curr_1():
    print("Current 1")


def Curr_2():
    print("Current 2")


def Left():
    global rotation_direct
    if button_start.button_pressed:
        if button_right.button_pressed:
            messagebox.showerror('Error', 'Остановите процесс, чтобы выбрать другое направление')
            if rotation_direct == 'Lft':
                button_left.set_pressed()
                button_right.set_unpressed()
        elif button_left.button_pressed:
            messagebox.showerror('Error', 'Это направление уже выбрано')
            if rotation_direct == 'Lft':
                button_left.set_pressed()
                button_right.set_unpressed()
    else:
        button_left.set_pressed()
        button_right.set_unpressed()
        rotation_direct = 'Lft'


def Right():
    global rotation_direct
    if button_start.button_pressed:
        if button_left.button_pressed:
            messagebox.showerror('Error', 'Остановите процесс, чтобы выбрать другое направление')
            if rotation_direct == 'Rgt':
                button_right.set_pressed()
                button_left.set_unpressed()
        elif button_right.button_pressed:
            messagebox.showerror('Error', 'Это направление уже выбрано')
            if rotation_direct == 'Rgt':
                button_right.set_pressed()
                button_left.set_unpressed()
    else:
        button_right.set_pressed()
        button_left.set_unpressed()
        rotation_direct = 'Rgt'


def Start():
    global slider_res
    if not button_left.button_pressed and not button_right.button_pressed:
        messagebox.showerror('Error', 'Выберите сторону вращения')
        button_start.set_unpressed()
    else:
        if isCOMopen is True:
            button_start.set_pressed()
            slider_res = slider.position
            print(f'{rotation_direct}_{slider.position}')
            with serial.Serial() as ser:
                ser.baudrate = combobox_BAUD.main[:(len(combobox_BAUD.main) - 5)]
                ser.port = combobox_COM.main
                ser.open()
                ser.write(f'{rotation_direct}_{slider.position}\n'.encode())
                ser.close()


def Stop():
    if not button_start.button_pressed:
        messagebox.showerror('Error', 'Нет процессов для остановки')
    else:
        button_start.set_unpressed()
        button_left.set_unpressed()
        button_right.set_unpressed()
        with serial.Serial() as ser:
            ser.baudrate = combobox_BAUD.main[:(len(combobox_BAUD.main) - 5)]
            ser.port = combobox_COM.main
            ser.open()
            ser.write('Stp\n'.encode())
            ser.close()
    button_stop.set_unpressed()


combobox_COM = OptionBox(x=15, y=15, w=125, h=20, main="COM",
                         option_list=[comport.device for comport in serial.tools.list_ports.comports()])
combobox_BAUD = OptionBox(x=160, y=15, w=125, h=20, main="BAUD",
                          option_list=[comport.device for comport in serial.tools.list_ports.comports()])
slider = Slider(x=50, y=70, w=200, h=25)
text_pwm = Text(x=WIN_WIDTH / 2, y=60, text='PWM')
button_curr_1 = Button(x=30, y=120, w=100, h=20, text='Current 1', pressed=False, func=Curr_1)
button_curr_2 = Button(x=170, y=120, w=100, h=20, text='Current 2', pressed=False, func=Curr_2)
current_1 = Indicator(x=30, y=107, w=100, h=45, title_text='Current 1')
current_2 = Indicator(x=170, y=107, w=100, h=45, title_text='Current 2')
button_left = Button(x=50, y=162, w=60, h=20, text='<--', pressed=True, func=Left)
button_right = Button(x=190, y=162, w=60, h=20, text='-->', pressed=True, func=Right)
button_start = Button(x=40, y=190, w=80, h=20, text='Start', pressed=True, func=Start)
button_stop = Button(x=180, y=190, w=80, h=20, text='Stop', pressed=True, func=Stop)
text_error_1 = Text(x=80, y=230, text='Error 1')
text_error_2 = Text(x=220, y=230, text='Error 2')
circle_1 = Circle(x=80, y=250, r=5)
circle_2 = Circle(x=220, y=250, r=5)

# baud_rates = ['50 Baud', '75 Baud', '110 Baud', '134 Baud', '150 Baud', '200 Baud', '300 Baud', '600 Baud',
# '1200 Baud', '1800 Baud', '2400 Baud', '4800 Baud', '9600 Baud', '19200 Baud', '38400 Baud', '57600 Baud',
# '115200 Baud']
baud_rates = ['1200 Baud', '1800 Baud', '2400 Baud', '4800 Baud', '9600 Baud', '19200 Baud', '38400 Baud', '57600 Baud',
              '115200 Baud']


def Check(**kwargs):
    for a, b in kwargs.items():
        if b.check() == "Menu":
            return "Menu"
    return "Non-menu"


slider_res = slider.position

isCOMchosen = False
isBAUDchosen = False
isCOMopen = False
connected = False

rotation_direct = None

def Reader():
    my_string = ""
    char = ''
    with serial.Serial() as ser:
        ser.baudrate = combobox_BAUD.main[:(len(combobox_BAUD.main) - 5)]
        ser.port = combobox_COM.main
        ser.open()
        while True:
            char = ser.read(1).decode('utf-8')
            if char != '\n':
                my_string += char
            else:
                return my_string
                char = ''
                my_string = ""
        ser.close()

my_string = ""
while True:

    screen.fill(BACKGROUND_COLOR)
    event_list = pygame.event.get()
    for i in event_list:
        if i.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    '''try:'''
    stat = Check(arg_1=combobox_COM, darg_1=combobox_BAUD)

    combobox_COM.option_list = [comport.device for comport in serial.tools.list_ports.comports()]
    select_COM = combobox_COM.update(event_list)
    if select_COM >= 0:
        combobox_COM.main = combobox_COM.option_list[select_COM]
        isCOMchosen = True
    if [comport.device for comport in serial.tools.list_ports.comports()] != combobox_COM.option_list:
        combobox_COM.option_list = [comport.device for comport in serial.tools.list_ports.comports()]
    if combobox_COM.main not in combobox_COM.option_list:
        combobox_COM.main = "COM"
    combobox_BAUD.option_list = baud_rates
    select_BAUD = combobox_BAUD.update(event_list)
    if select_BAUD >= 0:
        combobox_BAUD.main = combobox_BAUD.option_list[select_BAUD]
        isBAUDchosen = True

    select_slider = slider.update(event_list, stat)

    button_curr_1.update(event_list)
    button_curr_2.update(event_list)

    button_left.update(event_list)
    button_right.update(event_list)

    button_start.update(event_list)
    button_stop.update(event_list)

    slider.draw(screen)
    text_pwm.draw(screen)
    button_left.draw(screen)
    button_right.draw(screen)
    button_start.draw(screen)
    button_stop.draw(screen)
    text_error_1.draw(screen)
    text_error_2.draw(screen)
    circle_1.draw(screen)
    circle_2.draw(screen)
    current_1.draw(screen)
    current_2.draw(screen)
    combobox_COM.draw(screen)
    combobox_BAUD.draw(screen)

    if isBAUDchosen and isCOMchosen:
        isCOMopen = True
        my_string = Reader()

    if len(my_string) > 1:
        #print(my_string)
        message = re.findall(r'Curr\d_\d{1,4}', my_string)
        if 'Curr1' in my_string:
            message = re.findall(r'_\d{1,4}', re.findall(r'Curr1_\d{1,4}', my_string)[0])
            current_1.box_text = int(message[0][1:]) / 100
        if 'Curr2' in my_string:
            message = re.findall(r'_\d{1,4}', re.findall(r'Curr2_\d{1,4}', my_string)[0])
            current_2.box_text = int(message[0][1:]) / 100
        if "Err1" in my_string:
            circle_1.set_red()
        else:
            circle_1.set_green()
        if "Err2" in my_string:
            circle_2.set_red()
        else:
            circle_2.set_green()

    if slider_res is not slider.position and button_start.button_pressed:
        slider_res = slider.position
        print(f'{rotation_direct}_{slider.position}')
        if isCOMopen is True:
            with serial.Serial() as ser:
                ser.baudrate = combobox_BAUD.main[:(len(combobox_BAUD.main) - 5)]
                ser.port = combobox_COM.main
                ser.open()
                ser.write(f'{rotation_direct}_{slider.position}\n'.encode())
                ser.close()
    '''                
    except:
        messagebox.showerror('Error', 'Что-то пошло не так')
        button_left.set_unpressed()
        button_right.set_unpressed()
        button_start.set_unpressed()
        button_stop.set_unpressed()
     '''
    pygame.display.update()
    clock.tick(FPS)
