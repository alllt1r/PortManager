from cProfile import label
from turtle import width
import serial.tools.list_ports

import dearpygui.dearpygui as dpg
from Tools.demo.spreadsheet import center

dpg.create_context()

SCREEN_WIDTH = 300
SCREEN_HEIGHT = 250
BUTTON_CURRENT_WIDTH = 75
BUTTON_ARROW_WIDTH = 50
SLIDER_WIDTH = 175

def _log(sender, app_data, user_data):
    print(f"sender: {sender}, \t app_data: {app_data}, \t user_data: {user_data}")

with dpg.window(tag="Primary Window"):
    with dpg.group(horizontal=True):
        dpg.add_combo([comport.device for comport in serial.tools.list_ports.comports()], default_value="COM", width=100, pos=(SCREEN_WIDTH/4-100/2, 10), callback=_log)
        dpg.add_combo(("BOD1", "BOD2", "BOD3", "BOD4", "BOD5"), default_value="BOD", width=100, pos=(SCREEN_WIDTH*3/4-20-100/2, 10), callback=_log)
    with dpg.group(horizontal=True):
        dpg.add_text("Error 1", pos=(SCREEN_WIDTH/4-45/2, 160))
        dpg.add_text("Error 2", pos=(SCREEN_WIDTH*3/4-20-45/2, 160))
    with dpg.viewport_drawlist():
        dpg.draw_circle(((SCREEN_WIDTH)/4, 190), 5, color=(100, 255, 0, 255), fill=(100, 255, 0, 255)) #65
    with dpg.viewport_drawlist():
        dpg.draw_circle(((SCREEN_WIDTH-27)/4*3, 190), 5, color=(100, 255, 0, 255), fill=(100, 255, 0, 255))
    with dpg.group(horizontal=True):
        dpg.add_button(label="Current 1", small=False, width=BUTTON_CURRENT_WIDTH, pos=(SCREEN_WIDTH/4-BUTTON_CURRENT_WIDTH/2, 95), callback=_log)
        dpg.add_button(label="Current 2", small=False, width=BUTTON_CURRENT_WIDTH, pos=(SCREEN_WIDTH*3/4-20-BUTTON_CURRENT_WIDTH/2, 95), callback=_log)
    with dpg.group(horizontal=True):
        dpg.add_button(label="--->", width=BUTTON_ARROW_WIDTH, pos=(SCREEN_WIDTH/4-BUTTON_ARROW_WIDTH/2,125), callback=_log)
        dpg.add_button(label="<---", width=BUTTON_ARROW_WIDTH, pos=(SCREEN_WIDTH*3/4-20-BUTTON_ARROW_WIDTH/2,125), callback=_log)

    dpg.add_text("PWM", pos=(SCREEN_WIDTH/2-40/2, 40)) #150
    dpg.add_slider_int(min_value=0, max_value=255, callback=_log, width=SLIDER_WIDTH, pos=(SCREEN_WIDTH/2-SLIDER_WIDTH/2-9.5, 60)) #170


dpg.create_viewport(title='Port Manager', width=SCREEN_WIDTH, height=SCREEN_HEIGHT, resizable=False)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Primary Window", True)
dpg.start_dearpygui()
dpg.destroy_context()






'''
with dpg.window(tag="Primary Window"):
    with dpg.group(horizontal=True):
        dpg.add_combo(("COM1", "COM2", "COM3", "COM4", "COM5"), default_value="COM", width=100, pos=(SCREEN_WIDTH/4-100/2, 10), callback=_log)
        dpg.add_combo(("BOD1", "BOD2", "BOD3", "BOD4", "BOD5"), default_value="BOD", width=100, pos=(SCREEN_WIDTH*3/4-20-100/2, 10), callback=_log)
    with dpg.group(horizontal=True):
        dpg.add_text("Error 1", pos=(SCREEN_WIDTH/4-45/2, 35)) #45
        dpg.add_text("Error 2", pos=(SCREEN_WIDTH*3/4-20-45/2, 35))
    with dpg.viewport_drawlist():
        dpg.draw_circle(((SCREEN_WIDTH)/4, 65), 5, color=(100, 255, 0, 255), fill=(100, 255, 0, 255)) #65
    with dpg.viewport_drawlist():
        dpg.draw_circle(((SCREEN_WIDTH-27)/4*3, 65), 5, color=(100, 255, 0, 255), fill=(100, 255, 0, 255))
    with dpg.group(horizontal=True):
        dpg.add_button(label="Current 1", small=False, width=BUTTON_CURRENT_WIDTH, pos=(SCREEN_WIDTH/4-BUTTON_CURRENT_WIDTH/2, 90))
        dpg.add_button(label="Current 2", small=False, width=BUTTON_CURRENT_WIDTH, pos=(SCREEN_WIDTH*3/4-20-BUTTON_CURRENT_WIDTH/2, 90))
    with dpg.group(horizontal=True):
        dpg.add_button(label="--->", small=False, width=BUTTON_ARROW_WIDTH, pos=(SCREEN_WIDTH/4-BUTTON_ARROW_WIDTH/2,120))
        dpg.add_button(label="<---", small=False, width=BUTTON_ARROW_WIDTH, pos=(SCREEN_WIDTH*3/4-20-BUTTON_ARROW_WIDTH/2,120))

    dpg.add_text("PWM", pos=(SCREEN_WIDTH/2-40/2, 150)) #150
    dpg.add_slider_int(min_value=0, max_value=255, callback=_log, width=SLIDER_WIDTH, pos=(SCREEN_WIDTH/2-SLIDER_WIDTH/2-9.5, 170)) #170
'''
