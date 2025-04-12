import customtkinter as ctk
import pygame
from PIL import Image

pygame.mixer.init()

def open_agency(player, window, back_to_menu):
    def play_sound(path):
        try:
            pygame.mixer.Sound(path).play()
        except Exception as e:
            print("Soundfehler:", e)

    window.configure(fg_color="#1e1e1e")

    # Hauptlayout
    main_frame = ctk.CTkFrame(window, fg_color="transparent")
    main_frame.pack(fill="both", expand=True)

    # Content-Frame links
    content_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    content_frame.pack(side="left", fill="both", expand=True, padx=20)

    ctk.CTkLabel(content_frame, text="🏢 Agentur", font=("Arial Black", 24)).pack(pady=10)

    try:
        img = ctk.CTkImage(dark_image=Image.open("gui/assets/images/agency.png"), size=(400, 200))
        ctk.CTkLabel(content_frame, image=img, text="").pack(pady=5)
    except:
        pass

    ctk.CTkLabel(content_frame, text="🧍‍♀️ Mia (deine Agentin):", font=("Arial", 14, "bold")).pack()
    ctk.CTkLabel(content_frame, text="„Willkommen in der Agentur! Hier verhandle ich deine Sponsordeals.“,", font=("Arial", 13)).pack(pady=(0, 10))

    feedback = ctk.CTkLabel(content_frame, text="", font=("Arial", 14))
    feedback.pack(pady=5)

    # Vertragsbereich
    contract_frame = ctk.CTkFrame(content_frame, fg_color="#292929", corner_radius=10)
    contract_frame.pack(pady=10, fill="x")

    ctk.CTkLabel(contract_frame, text="📄 Verträge", font=("Arial", 16)).pack(pady=5)

    contracts = [
        {"name": "📄 Local Deal (+500€)", "requirement": 0, "amount": 500, "desc": "Ein lokales Sportgeschäft will mit dir werben. Klein, aber fein!"},
        {"name": "📄 Stadtweiter Sponsor (+1000€)", "requirement": 1000, "amount": 1000, "desc": "Ein stadtbekannter Ausrüster ist interessiert an einer Zusammenarbeit."},
        {"name": "📄 Nationaler Vertrag (+2500€)", "requirement": 2500, "amount": 2500, "desc": "Ein nationales Unternehmen sieht in dir Potenzial."},
        {"name": "📄 Global Brand Deal (+5000€)", "requirement": 4000, "amount": 5000, "desc": "Ein internationaler Top-Brand will dich als Gesicht!"}
    ]

    if not hasattr(player, "signed_contracts"):
        player.signed_contracts = set()

    def sign_contract(index, amount, requirement):
        if index in player.signed_contracts:
            feedback.configure(text="✅ Diesen Vertrag hast du bereits abgeschlossen!")
            return
        if player.followers >= requirement:
            player.money += amount
            player.signed_contracts.add(index)
            play_sound("gui/assets/sounds/gain.wav")
            refresh_bars()
            feedback.configure(text=f"✅ Vertrag über {amount}€ unterschrieben!")
        else:
            play_sound("gui/assets/sounds/lose.wav")
            feedback.configure(text=f"❌ Du brauchst mindestens {requirement} Follower!")

    for i, c in enumerate(contracts):
        already_signed = i in player.signed_contracts
        unlocked = player.followers >= c["requirement"]
        state = "normal" if unlocked and not already_signed else "disabled"

        frame = ctk.CTkFrame(contract_frame, fg_color="#1f1f1f" if not unlocked else "#333333", corner_radius=8)
        frame.pack(pady=5, fill="x", padx=10)

        btn = ctk.CTkButton(
            frame,
            text=c["name"],
            state=state,
            command=lambda i=i, a=c["amount"], r=c["requirement"]: sign_contract(i, a, r)
        )
        btn.pack(side="top", fill="x", padx=5, pady=2)

        desc = c["desc"]
        if already_signed:
            desc += " ✅ Vertrag bereits unterschrieben."
        elif not unlocked:
            desc += f" 🔒 Benötigt {c['requirement']} Follower."

        ctk.CTkLabel(frame, text=desc, wraplength=400, font=("Arial", 12), text_color="#cccccc").pack(padx=5, pady=(0, 5))

    # Rechte Sidebar – wie im Gym
    profile_frame = ctk.CTkFrame(main_frame, fg_color="#2a2a2a", corner_radius=12)
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

    # Zurück-zum-Menü
    btn_frame = ctk.CTkFrame(window, fg_color="transparent")
    btn_frame.pack(side="bottom", pady=20)

    ctk.CTkButton(btn_frame, text="🔙 Zurück zum Menü", command=lambda: [window.destroy(), back_to_menu()]).pack()
