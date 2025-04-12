import customtkinter as ctk
import pygame
from PIL import Image

pygame.mixer.init()

def open_lounge(player, window, back_to_menu):
    def play_sound(path):
        try:
            pygame.mixer.Sound(path).play()
        except Exception as e:
            print("Soundfehler:", e)

    window.configure(fg_color="#1e1e1e")
    ctk.CTkLabel(window, text="🎮 Lounge", font=("Arial Black", 24)).pack(pady=10)

    # Bild
    try:
        img = ctk.CTkImage(dark_image=Image.open("gui/assets/images/lounge.png"), size=(500, 300))
        ctk.CTkLabel(window, image=img, text="").pack(pady=5)
    except:
        pass

    # Profilanzeige
    profile_frame = ctk.CTkFrame(window, fg_color="#2b2b2b", corner_radius=12)
    profile_frame.pack(side="right", fill="y", padx=10, pady=10)

    def make_bar(label, value, max_value):
        ctk.CTkLabel(profile_frame, text=label).pack(pady=2)
        bar = ctk.CTkProgressBar(profile_frame, width=150)
        bar.set(min(value / max_value, 1.0))
        bar.pack(pady=2)
        return bar

    bars = {
        "Energie": make_bar("Energie", player.energy, 100),
        "Follower": make_bar("Follower", player.followers, 5000),
    }

    def refresh_bars():
        bars["Energie"].set(min(player.energy / 100, 1.0))
        bars["Follower"].set(min(player.followers / 5000, 1.0))

    # Feedbacktext
    feedback = ctk.CTkLabel(window, text="", font=("Arial", 14))
    feedback.pack(pady=5)

    # Auswahlrahmen
    action_frame = ctk.CTkFrame(window, fg_color="#292929", corner_radius=10)
    action_frame.pack(pady=10, padx=20, fill="x")

    # Radiobutton: Aktion wählen
    ctk.CTkLabel(action_frame, text="Was möchtest du tun?", font=("Arial", 16)).pack(pady=5)
    action = ctk.StringVar(value="relax")

    ctk.CTkRadioButton(action_frame, text="🛋️ Erholen", variable=action, value="relax").pack(anchor="w", padx=10)
    ctk.CTkRadioButton(action_frame, text="📱 Beitrag posten", variable=action, value="post").pack(anchor="w", padx=10)
    ctk.CTkRadioButton(action_frame, text="💬 Kommentar schreiben", variable=action, value="comment").pack(anchor="w", padx=10)

    def perform_action():
        selected = action.get()
        if selected == "relax":
            player.energy = min(100, player.energy + 20)
            play_sound("gui/assets/sounds/gain.wav")
            refresh_bars()
            feedback.configure(text="🛋️ Du fühlst dich erfrischt! +20 Energie")
        elif selected == "post":
            player.followers += 150
            play_sound("gui/assets/sounds/gain.wav")
            refresh_bars()
            feedback.configure(text="📱 Dein Beitrag war ein Hit! +150 Follower")
        elif selected == "comment":
            player.followers += 75
            play_sound("gui/assets/sounds/gain.wav")
            refresh_bars()
            feedback.configure(text="💬 Du hast dich eingebracht! +75 Follower")

    ctk.CTkButton(window, text="✅ Aktion ausführen", command=perform_action, height=40).pack(pady=10)
    ctk.CTkButton(window, text="🔙 Zurück zum Menü", command=lambda: [window.destroy(), back_to_menu()]).pack(pady=20)
