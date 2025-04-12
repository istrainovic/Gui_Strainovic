import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
from customtkinter import CTkImage
import os
import sys
import pygame

# Initialisiere Sound
pygame.mixer.init()

# Spielpfade importieren
sys.path.append(os.path.abspath("."))

from modules.room.player import Player
from modules.room.lockerroom import open_lockerroom
from modules.room.field import open_field
from modules.room.gym import open_gym
from modules.room.press import open_press
from modules.room.lounge import open_lounge
from modules.room.agency import open_agency
from modules.room.shop import open_shop


class BasketballGameApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.title("Basketball RPG")
        self.geometry("1000x600")
        self.minsize(800, 500)
        self.fullscreen = False
        self.player = None

        self.statusbar = None
        self.main_frame = None

        self.protocol("WM_DELETE_WINDOW", self.quit_game)
        self.bind("<Configure>", self.on_resize)

        self.show_main_menu()

    def set_small(self):
        self.attributes("-fullscreen", False)
        self.after(100, lambda: self.geometry("800x500"))

    def set_medium(self):
        self.attributes("-fullscreen", False)
        self.after(100, lambda: self.geometry("1000x650"))

    def set_fullscreen(self):
        self.attributes("-fullscreen", True)


    def clear_widgets(self):
        for widget in self.winfo_children():
            widget.destroy()

    def show_main_menu(self):
        self.clear_widgets()
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(expand=True, fill="both")

        # Großes Titelbild
        try:
            image_path = os.path.join("gui", "assets", "images", "main_menu.png")
            img = Image.open(image_path)
            img = img.resize((800, 300))
            bg = CTkImage(light_image=img, size=(800, 300))
            label_img = ctk.CTkLabel(self.main_frame, image=bg, text="")
            label_img.image = bg
            label_img.pack(pady=10)
        except:
            pass

        ctk.CTkLabel(self.main_frame, text="🏀 Basketball RPG", font=("Arial Black", 28)).pack(pady=10)
        ctk.CTkLabel(self.main_frame, text="Werde zur Legende auf dem Court!", font=("Arial", 18)).pack(pady=5)

        ctk.CTkButton(self.main_frame, text="🎮 Jetzt spielen", command=self.show_player_creation, height=40, width=200).pack(pady=10)
        button_frame = ctk.CTkFrame(self.main_frame)
        button_frame.pack(pady=10)

        ctk.CTkLabel(button_frame, text="Fenstergröße ändern:", font=("Arial", 14)).pack(pady=5)

        ctk.CTkButton(button_frame, text="🗔 Klein (800x500)", command=self.set_small).pack(pady=2)
        ctk.CTkButton(button_frame, text="🪟 Mittel (1000x650)", command=self.set_medium).pack(pady=2)
        ctk.CTkButton(button_frame, text="🖥 Vollbild", command=self.set_fullscreen).pack(pady=2)



    def show_player_creation(self):
        self.clear_widgets()

        # zentriertes zentrales Layout
        container = ctk.CTkFrame(self)
        container.pack(expand=True, fill="both")

        frame = ctk.CTkFrame(container, width=600)
        frame.pack(expand=True)
    
        ctk.CTkLabel(frame, text="👤 Spieler erstellen", font=("Arial Black", 24)).pack(pady=10)

        # Name
        ctk.CTkLabel(frame, text="Name").pack()
        name_entry = ctk.CTkEntry(frame, placeholder_text="Dein Spielername")
        name_entry.pack(pady=5)

        # Rückennummer über 2 Felder + "+" Zeichen
        ctk.CTkLabel(frame, text="Rückennummer = Zahl 1 + Zahl 2").pack()
        number_frame = ctk.CTkFrame(frame)
        number_frame.pack(pady=5)

        num1 = ctk.CTkEntry(number_frame, width=60)
        num1.pack(side="left", padx=5)
        ctk.CTkLabel(number_frame, text="+").pack(side="left")
        num2 = ctk.CTkEntry(number_frame, width=60)
        num2.pack(side="left", padx=5)

        # Position
        ctk.CTkLabel(frame, text="Position").pack()
        position_dropdown = ctk.CTkOptionMenu(frame, values=[
            "Point Guard", "Shooting Guard", "Small Forward", "Power Forward", "Center"
        ])
        position_dropdown.pack(pady=5)

        # Herkunft
        ctk.CTkLabel(frame, text="Herkunft").pack()
        origin_dropdown = ctk.CTkOptionMenu(frame, values=[
            "USA", "Frankreich", "Spanien", "Deutschland", "Kanada", "Brasilien",
            "Japan", "Italien", "Australien", "Serbien", "Österreich"
        ])
        origin_dropdown.pack(pady=5)

        # Style
        ctk.CTkLabel(frame, text="Style").pack()
        style_dropdown = ctk.CTkOptionMenu(frame, values=[
            "Streetwear", "Classic", "Sportlich", "Casual", "Luxus", "Retro"
        ])
        style_dropdown.pack(pady=5)

        # Accessoires
        ctk.CTkLabel(frame, text="Accessoire").pack()
        accessories_dropdown = ctk.CTkOptionMenu(frame, values=[
            "Ball", "Kette", "Kappe", "Handschuhe", "Armband", "Schweißband"
        ])
        accessories_dropdown.pack(pady=5)

        # Hautfarbe
        ctk.CTkLabel(frame, text="Hautfarbe").pack()
        skin_color_dropdown = ctk.CTkOptionMenu(frame, values=[
            "hell", "mittel", "dunkel", "sehr hell", "sehr dunkel"
        ])
        skin_color_dropdown.pack(pady=5)

        # Gewicht (Slider + Anzeige)
        ctk.CTkLabel(frame, text="Gewicht (kg)").pack()
        weight_var = ctk.StringVar(value="80")
        weight_slider = ctk.CTkSlider(frame, from_=50, to=150, number_of_steps=100, width=400,
                                    command=lambda v: weight_var.set(f"{int(v)}"))
        weight_slider.set(80)
        weight_slider.pack()
        ctk.CTkLabel(frame, textvariable=weight_var).pack(pady=2)

        # Größe (Slider + Anzeige)
        ctk.CTkLabel(frame, text="Größe (cm)").pack()
        height_var = ctk.StringVar(value="190")
        height_slider = ctk.CTkSlider(frame, from_=160, to=230, number_of_steps=70, width=400,
                                    command=lambda v: height_var.set(f"{int(v)}"))
        height_slider.set(190)
        height_slider.pack()
        ctk.CTkLabel(frame, textvariable=height_var).pack(pady=2)

        # Animation
        frame.after(100, lambda: frame.configure(fg_color="#1f1f1f"))

        def create():
            name = name_entry.get().strip()
            if not name:
                messagebox.showwarning("Fehler", "Name darf nicht leer sein!")
                return

            try:
                num_a = int(num1.get())
                num_b = int(num2.get())
                total = num_a + num_b
                if not (0 <= num_a <= 99 and 0 <= num_b <= 99):
                    raise ValueError("Zahlen müssen zwischen 0-99 liegen.")
                if total > 99:
                    raise ValueError("Summe darf maximal 99 sein.")
            except Exception as e:
                messagebox.showerror("Fehler bei Rückennummer", str(e))
                return

            self.player = Player(
                name=name,
                position=position_dropdown.get(),
                origin=origin_dropdown.get(),
                style=style_dropdown.get(),
                accessories=[accessories_dropdown.get()],
                skin_color=skin_color_dropdown.get(),
                weight=int(weight_slider.get()),
                height=int(height_slider.get())
            )
            self.player.number = str(total)
            self.show_game_hub()

        ctk.CTkButton(frame, text="🚀 Spieler erstellen", command=create, height=40).pack(pady=20)


    
    def show_game_hub(self):
        self.clear_widgets()

        hub = ctk.CTkFrame(self)
        hub.pack(expand=True, fill="both", padx=20, pady=10)

        title = ctk.CTkLabel(hub, text=f"🏀 Willkommen, {self.player.name}!", font=("Arial Black", 22))
        title.pack(pady=10)
        
                # Einführungstext (visuell)
        intro_box = ctk.CTkFrame(hub, corner_radius=15, fg_color="#333333")
        intro_box.pack(pady=10, padx=20, fill="x")

        intro_text = (
            "📢 Willkommen bei deinem Basketball-Abenteuer!\n\n"
            "Trainiere hart im Gym, zeig dein Können auf dem Spielfeld, "
            "baue deine Follower auf, werde ein Star – oder verliere alles. "
            "Jede Entscheidung zählt. 🏀💼\n\n"
            "Bereit für dein Spiel des Lebens?"
        )

        ctk.CTkLabel(intro_box, text=intro_text, font=("Arial", 14), justify="left", wraplength=700).pack(padx=10, pady=10)

        # Raum-Buttons im Grid
        button_grid = ctk.CTkFrame(hub)
        button_grid.pack(pady=10)

        rooms = [
            ("🏋 Gym", open_gym),
            ("👟 Shop", open_shop),
            ("📰 Presse", open_press),
            ("🎮 Lounge", open_lounge),
            ("🎽 Locker Room", open_lockerroom),
            ("🎯 Field", open_field),
            ("💼 Agentur", open_agency),
        ]

        for i, (label, func) in enumerate(rooms):
            btn = ctk.CTkButton(button_grid, text=label, width=200,
                                command=lambda f=func: self.enter_room(f))
            btn.grid(row=i // 3, column=i % 3, padx=10, pady=10)

        # Profil-Toggle
        self.profile_frame = ctk.CTkFrame(hub, corner_radius=10)
        self.profile_visible = False

        def toggle_profile():
            if self.profile_visible:
                self.profile_frame.pack_forget()
            else:
                self.show_profile_embed(hub)
            self.profile_visible = not self.profile_visible

        ctk.CTkButton(hub, text="👤 Profil anzeigen/ausblenden", command=toggle_profile).pack(pady=10)

                # Spiel beenden Button
        ctk.CTkButton(hub, text="❌ Spiel beenden", fg_color="#8B0000", hover_color="#a30000",
                      command=self.quit_game, height=40, width=200).pack(pady=20)


    def show_profile_embed(self, parent):
        self.profile_frame = ctk.CTkFrame(parent, fg_color="#222222", corner_radius=12)
        self.profile_frame.pack(pady=10, padx=10, fill="x")

        def make_bar(label, value, max_value):
            ctk.CTkLabel(self.profile_frame, text=label).pack(anchor="w", padx=10)
            bar = ctk.CTkProgressBar(self.profile_frame, width=300, height=15)
            bar.set(min(value / max_value, 1.0))
            bar.pack(pady=2)

        make_bar("📈 Erfahrung (XP)", self.player.xp, 100)
        make_bar("⚡ Energie", self.player.energy, 100)
        make_bar("👥 Follower", self.player.followers, 5000)

        money_color = "green" if self.player.money >= 0 else "red"
        ctk.CTkLabel(self.profile_frame, text="💰 Geld", anchor="w").pack(anchor="w", padx=10)
        ctk.CTkLabel(self.profile_frame, text=f"{self.player.money}€", text_color=money_color, font=("Arial", 14)).pack(pady=2)

        ctk.CTkLabel(self.profile_frame, text=f"🎽 Rückennummer: {self.player.number}").pack(pady=2)
        ctk.CTkLabel(self.profile_frame, text=f"🎭 Style: {self.player.style} | 🧬 Herkunft: {self.player.origin}").pack(pady=2)

    def gain_xp(self, amount):
        old = self.player.xp
        self.player.xp += amount
        self.animate_value_change("XP", old, self.player.xp)

    def use_energy(self, amount):
        old = self.player.energy
        self.player.energy = max(0, self.player.energy - amount)
        self.animate_value_change("Energie", old, self.player.energy)

    def add_money(self, amount):
        old = self.player.money
        self.player.money += amount
        self.animate_value_change("Geld", old, self.player.money)

    def add_followers(self, amount):
        old = self.player.followers
        self.player.followers += amount
        self.animate_value_change("Follower", old, self.player.followers)

    def animate_value_change(self, label, old_value, new_value):
        diff = new_value - old_value
        if diff == 0:
            return

        color = "green" if diff > 0 else "red"
        sound_file = "gui/assets/sounds/gain.wav" if diff > 0 else "gui/assets/sounds/lose.wav"

        # Sound abspielen
        try:
            pygame.mixer.Sound(sound_file).play()
        except Exception as e:
            print(f"[Soundfehler] {e}")

        # Anzeige
        change_text = f"{'+' if diff > 0 else ''}{diff} {label}"
        notif = ctk.CTkLabel(self, text=change_text, text_color=color, font=("Arial", 16))
        notif.place(relx=0.5, rely=0.1, anchor="center")
        notif.after(1500, notif.destroy)


    def enter_room(self, room_func):
    # Zerstöre das aktuelle Fenster (Menü, etc.)
        self.clear_widgets()

    # Raum-Fenster wird direkt in self (dem Hauptfenster) eingebettet
        room_frame = ctk.CTkFrame(self)
        room_frame.pack(expand=True, fill="both")

    # Zurück-zum-Menü-Funktion
        def back_to_menu():
            room_frame.destroy()
            self.show_game_hub()

    # Raumfunktion aufrufen
        room_func(self.player, room_frame, back_to_menu)

        if self.statusbar:
            self.statusbar.configure(text=self.get_status_text())


    def on_resize(self, event):
        # Optional: Resize-Feedback oder Layout-Anpassung
        pass

    def quit_game(self):
        if messagebox.askokcancel("Spiel beenden", "Willst du das Spiel wirklich schließen?"):
            self.destroy()


def launch_app():
    app = BasketballGameApp()
    app.mainloop()
