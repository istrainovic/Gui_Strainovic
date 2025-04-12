import customtkinter as ctk
import pygame
import random
import time
import threading
from PIL import Image

pygame.mixer.init()

def open_field(player, window, back_to_menu):
    def play_sound(path):
        try:
            pygame.mixer.Sound(path).play()
        except:
            pass

    window.configure(fg_color="#1e1e1e")

    main_frame = ctk.CTkFrame(window, fg_color="transparent")
    main_frame.pack(fill="both", expand=True)

    content_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    content_frame.pack(side="left", fill="both", expand=True, padx=20)

    ctk.CTkLabel(content_frame, text="🏟 Spielfeld", font=("Arial Black", 24)).pack(pady=10)

    try:
        img = ctk.CTkImage(dark_image=Image.open("gui/assets/images/field.png"), size=(400, 200))
        ctk.CTkLabel(content_frame, image=img, text="").pack(pady=5)
    except:
        pass

    announcer = ctk.CTkLabel(content_frame, text="🎙 Kommentator: „Du hast 8 Aktionen. Gewinne durch Können – nur dann gibt's die Belohnung!“", font=("Arial", 13))
    announcer.pack(pady=(0, 10))

    feedback = ctk.CTkLabel(content_frame, text="", font=("Arial", 14))
    feedback.pack(pady=5)

    animation_label = ctk.CTkLabel(content_frame, text="", font=("Arial", 12, "italic"))
    animation_label.pack(pady=5)

    action_counter = [0]
    success_counter = [0]
    game_over = [False]

    def show_animation(text, delay=0.5):
        animation_label.configure(text=text)
        window.update()
        time.sleep(delay)
        animation_label.configure(text="")

    def end_game():
        game_over[0] = True
        for widget in content_frame.winfo_children():
            if isinstance(widget, ctk.CTkButton):
                widget.destroy()

        if success_counter[0] >= 5:
            reward = 150 + success_counter[0] * 20
            player.money += reward
            play_sound("gui/assets/sounds/cheer.wav")
            feedback.configure(text=f"🏆 Du hast das Spiel gewonnen!\nErfolgreiche Aktionen: {success_counter[0]}/8\nBelohnung: +{reward}€")
        else:
            play_sound("gui/assets/sounds/lose.wav")
            feedback.configure(text=f"❌ Du hast verloren!\nNur {success_counter[0]} erfolgreiche Aktionen.\nKeine Belohnung.")

        refresh_bars()

    def make_result_text(success, action, xp):
        if success:
            player.followers += 100
            player.gain_xp(xp)
            success_counter[0] += 1
            return f"✅ {action} erfolgreich! +100 Follower, +{xp} XP"
        else:
            player.followers = max(0, player.followers - 80)
            player.gain_xp(int(xp / 2))
            return f"❌ {action} misslungen! -80 Follower, +{int(xp / 2)} XP"

    def perform_action(action_name):
        if game_over[0]:
            return
        def run():
            show_animation("🏀 Aktion läuft...")
            result = random.random() < 0.6
            xp_reward = random.randint(10, 20)
            feedback.configure(text=make_result_text(result, action_name, xp_reward))
            action_counter[0] += 1
            refresh_bars()
            if action_counter[0] >= 8:
                time.sleep(1)
                end_game()
        threading.Thread(target=run).start()

    def rest_action():
        if game_over[0]:
            return
        player.energy = min(100, player.energy + 20)
        play_sound("gui/assets/sounds/gain.wav")
        feedback.configure(text="💤 Ausgeruht! +20 Energie")
        action_counter[0] += 1
        refresh_bars()
        if action_counter[0] >= 8:
            time.sleep(1)
            end_game()

    btn_style = {"width": 200, "font": ("Arial", 14)}
    ctk.CTkButton(content_frame, text="🏀 Werfen", command=lambda: perform_action("Wurf"), **btn_style).pack(pady=5)
    ctk.CTkButton(content_frame, text="📤 Passen", command=lambda: perform_action("Pass"), **btn_style).pack(pady=5)
    ctk.CTkButton(content_frame, text="🛡 Verteidigen", command=lambda: perform_action("Verteidigung"), **btn_style).pack(pady=5)
    ctk.CTkButton(content_frame, text="🛌 Ausruhen", command=rest_action, **btn_style).pack(pady=10)

    # Sidebar
    sidebar = ctk.CTkFrame(main_frame, fg_color="#2a2a2a", corner_radius=12)
    sidebar.pack(side="right", fill="y", padx=10, pady=10)

    def make_bar(label, value, max_value):
        ctk.CTkLabel(sidebar, text=label).pack(pady=2)
        bar = ctk.CTkProgressBar(sidebar, width=150)
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

    ctk.CTkLabel(sidebar, text=f"Geld: {player.money}€", text_color="red" if player.money < 0 else "green").pack(pady=5)
    ctk.CTkLabel(sidebar, text=f"Rückennr: {player.number}").pack(pady=3)

    # Zurück-zum-Menü
    btn_frame = ctk.CTkFrame(window, fg_color="transparent")
    btn_frame.pack(side="bottom", pady=20)
    ctk.CTkButton(btn_frame, text="🔙 Zurück zum Menü", command=lambda: [window.destroy(), back_to_menu()]).pack()
