import customtkinter as ctk
import pygame
import time
import threading
from PIL import Image

pygame.mixer.init()

def open_shop(player, window, back_to_menu):
    def play_sound(path):
        try:
            pygame.mixer.Sound(path).play()
        except:
            pass

    window.configure(fg_color="#1e1e1e")

    main_frame = ctk.CTkFrame(window, fg_color="transparent")
    main_frame.pack(fill="both", expand=True)

    # Scrollbarer Bereich mit Centering
    scroll_canvas = ctk.CTkCanvas(main_frame, bg="#1e1e1e", highlightthickness=0)
    scroll_canvas.pack(side="left", fill="both", expand=True)

    scrollbar = ctk.CTkScrollbar(main_frame, orientation="vertical", command=scroll_canvas.yview)
    scrollbar.pack(side="left", fill="y")

    container = ctk.CTkFrame(scroll_canvas, fg_color="transparent")
    scroll_canvas.create_window((0, 0), window=container, anchor="n", width=800)

    scroll_canvas.configure(yscrollcommand=scrollbar.set)

    def update_scroll_region(event=None):
        scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all"))
    container.bind("<Configure>", update_scroll_region)

    scroll_frame = ctk.CTkFrame(container, fg_color="transparent")
    scroll_frame.pack(pady=10)

    ctk.CTkLabel(scroll_frame, text="🛍️ Basketball Shop", font=("Arial Black", 24)).pack(pady=10)

    try:
        img = ctk.CTkImage(dark_image=Image.open("gui/assets/images/shop.png"), size=(400, 200))
        ctk.CTkLabel(scroll_frame, image=img, text="").pack(pady=5)
    except:
        pass

    ctk.CTkLabel(scroll_frame, text="👕 Verkäufer: „Hier gibt's Style, Skills und mehr. Skins? Klar!“", font=("Arial", 13)).pack(pady=(0, 10))

    feedback = ctk.CTkLabel(scroll_frame, text="", font=("Arial", 14))
    feedback.pack(pady=5)

    animation_label = ctk.CTkLabel(scroll_frame, text="", font=("Arial", 12, "italic"))
    animation_label.pack(pady=5)

    if not hasattr(player, "inventory"):
        player.inventory = []
    if not hasattr(player, "skins"):
        player.skins = []

    items = [
        {"name": "🔥 Sneaker Pro", "price": 300, "desc": "Leichtere Schuhe – du bewegst dich schneller."},
        {"name": "💪 Power-Armband", "price": 450, "desc": "Stärkt dein Selbstvertrauen auf dem Feld."},
        {"name": "🎧 Fokus-Kopfhörer", "price": 200, "desc": "Perfekt fürs Training – Fokus + Style."},
        {"name": "🏀 Limited Ball", "price": 600, "desc": "Einzigartiger Ball mit Grip – besserer Wurf."}
    ]

    skins = [
        {"name": "👕 Classic White", "price": 150, "desc": "Ein klassischer Look für jede Position."},
        {"name": "🧢 Street Style", "price": 300, "desc": "Urban-Look, beliebt bei Followern."},
        {"name": "🕶️ Black Mamba", "price": 500, "desc": "Inspiriert vom legendären Style."},
        {"name": "🎽 Champion Gold", "price": 700, "desc": "Goldenes Jersey – nur für echte Gewinner."},
        {"name": "👟 Neon Vibes", "price": 350, "desc": "Futuristische Leuchtschuhe."}
    ]

    def refresh_money_display():
        money_label.configure(text=f"Geld: {player.money}€", text_color="red" if player.money < 0 else "green")

    def show_animation(text, delay=0.5):
        animation_label.configure(text=text)
        window.update()
        time.sleep(delay)
        animation_label.configure(text="")

    def buy_item(item, target_list, label):
        def run():
            if item["name"] in target_list:
                feedback.configure(text="❗ Bereits gekauft.")
                return
            show_animation("🧾 Kasse scannt...")
            if player.money >= item["price"]:
                player.money -= item["price"]
                target_list.append(item["name"])
                play_sound("gui/assets/sounds/kaching.wav")
                feedback.configure(text=f"✅ {label} gekauft: {item['name']} für {item['price']}€")
                refresh_money_display()
            else:
                play_sound("gui/assets/sounds/lose.wav")
                feedback.configure(text="❌ Nicht genug Geld!")
            refresh_bars()
        threading.Thread(target=run).start()

    # Items
    ctk.CTkLabel(scroll_frame, text="🧰 Ausrüstung", font=("Arial", 15, "bold")).pack(pady=(10, 5))
    for item in items:
        unlocked = player.money >= item["price"]
        already_owned = item["name"] in player.inventory
        frame = ctk.CTkFrame(scroll_frame, fg_color="#333333" if unlocked else "#1f1f1f", corner_radius=8)
        frame.pack(pady=4, fill="x", padx=10)
        btn = ctk.CTkButton(
            frame,
            text=f"{item['name']} - {item['price']}€",
            state="disabled" if already_owned else ("normal" if unlocked else "disabled"),
            command=lambda i=item: buy_item(i, player.inventory, "Item")
        )
        btn.pack(side="top", fill="x", padx=5, pady=2)
        desc = item["desc"]
        if already_owned:
            desc += " ✅ Bereits gekauft."
        elif not unlocked:
            desc += f" 🔒 Du brauchst {item['price']}€."
        ctk.CTkLabel(frame, text=desc, wraplength=400, font=("Arial", 12), text_color="#cccccc").pack(padx=5, pady=(0, 5))

    # Skins
    ctk.CTkLabel(scroll_frame, text="🎽 Skins", font=("Arial", 15, "bold")).pack(pady=(10, 5))
    for skin in skins:
        unlocked = player.money >= skin["price"]
        already_owned = skin["name"] in player.skins
        frame = ctk.CTkFrame(scroll_frame, fg_color="#333333" if unlocked else "#1f1f1f", corner_radius=8)
        frame.pack(pady=4, fill="x", padx=10)
        btn = ctk.CTkButton(
            frame,
            text=f"{skin['name']} - {skin['price']}€",
            state="disabled" if already_owned else ("normal" if unlocked else "disabled"),
            command=lambda s=skin: buy_item(s, player.skins, "Skin")
        )
        btn.pack(side="top", fill="x", padx=5, pady=2)
        desc = skin["desc"]
        if already_owned:
            desc += " ✅ Bereits gekauft."
        elif not unlocked:
            desc += f" 🔒 Du brauchst {skin['price']}€."
        ctk.CTkLabel(frame, text=desc, wraplength=400, font=("Arial", 12), text_color="#cccccc").pack(padx=5, pady=(0, 5))

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

    money_label = ctk.CTkLabel(sidebar, text=f"Geld: {player.money}€", text_color="green")
    money_label.pack(pady=5)
    ctk.CTkLabel(sidebar, text=f"Rückennr: {player.number}").pack(pady=3)

    # Zurück
    btn_frame = ctk.CTkFrame(window, fg_color="transparent")
    btn_frame.pack(side="bottom", pady=20)
    ctk.CTkButton(btn_frame, text="🔙 Zurück zum Menü", command=lambda: [window.destroy(), back_to_menu()]).pack()
