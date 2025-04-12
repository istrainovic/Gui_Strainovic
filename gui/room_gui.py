import customtkinter as ctk
from modules.room.gym import open_gym
from modules.room.shop import open_shop
from modules.room.lounge import open_lounge
from modules.room.field import open_field
from modules.room.press import open_press
from modules.room.lockerroom import open_lockerroom
from modules.room.agency import open_agency

def enter_room(room_func):
    window = ctk.CTkToplevel()  # Neues Fenster für den Raum
    window.geometry("800x600")  # Raumgröße
    room_func(window)  # Raum öffnen
    window.mainloop()
