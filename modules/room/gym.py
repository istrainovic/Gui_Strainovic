import customtkinter as ctk
import pygame
import random
import time
import threading
from PIL import Image

pygame.mixer.init()

def open_gym(player, window, back_to_menu):
    def play_sound(path):
        try:
            pygame.mixer.Sound(path).play()
        except Exception as e:
            print("Sound error:", e)

    window.configure(fg_color="#1c1c1c")
    ctk.CTkLabel(window, text="🏋 Willkommen im Gym", font=("Arial Black", 24)).pack(pady=10)
    ctk.CTkLabel(window, text="Coach Mike: \"Zeit zum Schwitzen, Champion!\"", font=("Arial", 16)).pack(pady=5)

    profile_frame = ctk.CTkFrame(window, fg_color="#2a2a2a", corner_radius=12)
    profile_frame.pack(side="right", fill="y", padx=10, pady=10)

    def make_bar(label, value, max_value):
        ctk.CTkLabel(profile_frame, text=label).pack(pady=2)
        bar = ctk.CTkProgressBar(profile_frame, width=150)
        bar.set(min(value / max_value, 1.0))
        bar.pack(pady=2)
        return bar

    bars = {
        "XP": make_bar("XP", player.xp, 100),
        "Energie": make_bar("Energie", player.energy, 100),
        "Follower": make_bar("Follower", player.followers, 5000),
    }

    def refresh_bars():
        bars["XP"].set(min(player.xp / 100, 1.0))
        bars["Energie"].set(min(player.energy / 100, 1.0))
        bars["Follower"].set(min(player.followers / 5000, 1.0))

    ctk.CTkLabel(profile_frame, text=f"Geld: {player.money}€", text_color="red" if player.money < 0 else "green").pack(pady=5)
    ctk.CTkLabel(profile_frame, text=f"Rückennr: {player.number}").pack(pady=3)

    box = ctk.CTkFrame(window, fg_color="#2b2b2b", corner_radius=10)
    box.pack(pady=10, padx=20, expand=True, fill="both")

    def clear_box():
        for widget in box.winfo_children():
            widget.destroy()

    def show_main_buttons():
        ctk.CTkLabel(box, text="Wähle dein Training:", font=("Arial", 18)).pack(pady=10)
        ctk.CTkButton(box, text="🏃 Cardio", command=open_cardio).pack(pady=5)
        ctk.CTkButton(box, text="💪 Krafttraining", command=open_kraft).pack(pady=5)
        ctk.CTkButton(box, text="🏀 Basketball", command=open_basketball).pack(pady=5)
        ctk.CTkButton(box, text="🔙 Zurück zum Menü", command=lambda: [window.destroy(), back_to_menu()]).pack(pady=15)

    def open_cardio():
        clear_box()

        ctk.CTkLabel(box, text="🏃 Cardio Training – Laufband", font=("Arial", 18)).pack(pady=5)
        ctk.CTkLabel(box, text="Coach Mike: \"Wie schnell kannst du laufen?\"").pack()

        ctk.CTkLabel(box, text="Geschwindigkeit (1 = locker, 10 = Sprint):").pack()
        speed_slider = ctk.CTkSlider(box, from_=1, to=10, number_of_steps=9)
        speed_slider.set(5)
        speed_slider.pack(pady=5)

        feedback = ctk.CTkLabel(box, text="")
        feedback.pack(pady=5)

        def start_cardio():
            speed = speed_slider.get()
            xp = int(speed * 3)
            energy = int(speed * 2)

            player.gain_xp(xp)
            play_sound("gui/assets/sounds/gain.wav")
            refresh_bars()
            feedback.configure(text=f"Coach Mike: Gut gemacht! +{xp} XP | -{energy} Energy")

            window.after(3000, lambda: [
                player.use_energy(energy),
                play_sound("gui/assets/sounds/lose.wav"),
                refresh_bars()
            ])

        ctk.CTkButton(box, text="Start", command=start_cardio).pack(pady=5)
        ctk.CTkButton(box, text="Zurück zum Gym", command=lambda: [clear_box(), show_main_buttons()]).pack(pady=10)

        try:
            img = ctk.CTkImage(dark_image=Image.open("gui/assets/images/cardio.png"), size=(600, 360))
            ctk.CTkLabel(box, image=img, text="").pack()
        except:
            pass

    def open_kraft():
        clear_box()

        ctk.CTkLabel(box, text="💪 Krafttraining – Bankdrücken", font=("Arial", 18)).pack(pady=5)
        ctk.CTkLabel(box, text="Coach Mike: \"Schneller, los! 10 Sekunden Vollgas!\"").pack()

        click_count = [0]
        btn = ctk.CTkButton(box, text="DRÜCK MICH!", command=lambda: click_count.__setitem__(0, click_count[0]+1))
        btn.pack(pady=10)

        feedback = ctk.CTkLabel(box, text="")
        feedback.pack(pady=5)

        def start_timer():
            btn.configure(state="normal")
            click_count[0] = 0
            feedback.configure(text="Los geht’s!")

            def run():
                time.sleep(10)
                btn.configure(state="disabled")
                xp_gain = int(click_count[0] / 3)
                energy_loss = 15

                player.gain_xp(xp_gain)
                play_sound("gui/assets/sounds/gain.wav")
                refresh_bars()
                feedback.configure(text=f"Coach Mike: Du hast {xp_gain} XP erdrückt und {energy_loss} Energy verloren")

                time.sleep(3)
                player.use_energy(energy_loss)
                play_sound("gui/assets/sounds/lose.wav")
                refresh_bars()

            threading.Thread(target=run).start()

        ctk.CTkButton(box, text="Start", command=start_timer).pack(pady=5)
        ctk.CTkButton(box, text="Zurück zum Gym", command=lambda: [clear_box(), show_main_buttons()]).pack(pady=10)

        try:
            img = ctk.CTkImage(dark_image=Image.open("gui/assets/images/kraft.png"), size=(600, 360))
            ctk.CTkLabel(box, image=img, text="").pack()
        except:
            pass

    def open_basketball():
        clear_box()

        ctk.CTkLabel(box, text="🏀 Basketballtraining – Wurfspiel", font=("Arial", 18)).pack(pady=5)
        ctk.CTkLabel(box, text="Coach Mike: \"Triff 3 Ringe! Klick sie so schnell du kannst.\"").pack()

        ring_frame = ctk.CTkFrame(box)
        ring_frame.pack(pady=10)
        result = ctk.CTkLabel(box, text="")
        result.pack(pady=5)

        targets_hit = [0]
        ring_buttons = []

        def ring_clicked(btn):
            btn.destroy()
            targets_hit[0] += 1
            if targets_hit[0] == 3:
                xp = 25
                energy = 10

                player.gain_xp(xp)
                play_sound("gui/assets/sounds/gain.wav")
                refresh_bars()
                result.configure(text=f"Coach Mike: Saubere Würfe! +{xp} XP | -{energy} Energy")

                window.after(3000, lambda: [
                    player.use_energy(energy),
                    play_sound("gui/assets/sounds/lose.wav"),
                    refresh_bars()
                ])

        for i in range(3):
            btn = ctk.CTkButton(ring_frame, text=f"🎯 RING {i+1}", command=lambda b=i: ring_clicked(ring_buttons[b]))
            btn.grid(row=0, column=i, padx=10)
            ring_buttons.append(btn)

        ctk.CTkButton(box, text="Zurück zum Gym", command=lambda: [clear_box(), show_main_buttons()]).pack(pady=10)

        try:
            img = ctk.CTkImage(dark_image=Image.open("gui/assets/images/korb.png"), size=(600, 360))
            ctk.CTkLabel(box, image=img, text="").pack()
        except:
            pass

    show_main_buttons()
