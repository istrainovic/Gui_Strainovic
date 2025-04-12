import customtkinter as ctk
import pygame
from PIL import Image

pygame.mixer.init()

def open_lockerroom(player, window, back_to_menu):
    def play_sound(path):
        try:
            pygame.mixer.Sound(path).play()
        except:
            pass

    window.configure(fg_color="#1e1e1e")
    ctk.CTkLabel(window, text="🧼 Locker Room", font=("Arial Black", 24)).pack(pady=10)

    try:
        img = ctk.CTkImage(dark_image=Image.open("gui/assets/images/lockerroom.png"), size=(400, 200))
        ctk.CTkLabel(window, image=img, text="").pack(pady=5)
    except:
        pass

    if not hasattr(player, "inventory"):
        player.inventory = []
    if not hasattr(player, "skins"):
        player.skins = []
    if not hasattr(player, "equipped"):
        player.equipped = {}

    feedback = ctk.CTkLabel(window, text="", font=("Arial", 14))
    feedback.pack(pady=5)

    box = ctk.CTkFrame(window, fg_color="#2b2b2b", corner_radius=10)
    box.pack(pady=10, padx=20, fill="x")

    # Duschen
    def shower():
        player.energy = min(100, player.energy + 30)
        play_sound("gui/assets/sounds/gain.wav")
        feedback.configure(text="🚿 Geduscht! +30 Energie")
        refresh_bars()

    ctk.CTkButton(box, text="🚿 Duschen (Energy +30)", command=shower).pack(pady=10)

    # Ausrüstungssystem
    ctk.CTkLabel(box, text="🎽 Ausrüstung", font=("Arial", 15, "bold")).pack(pady=(10, 5))

    layout = ctk.CTkFrame(box, fg_color="transparent")
    layout.pack(pady=10, padx=10, fill="x")

    inventory_frame = ctk.CTkFrame(layout, fg_color="#222222", corner_radius=10)
    inventory_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

    player_frame = ctk.CTkFrame(layout, fg_color="#1f1f1f", corner_radius=10, width=200)
    player_frame.pack(side="left", fill="y")

    ctk.CTkLabel(inventory_frame, text="🎒 Inventar", font=("Arial", 13, "bold")).pack(pady=5)
    ctk.CTkLabel(player_frame, text="🧍 Spieler", font=("Arial", 13, "bold")).pack(pady=5)

    item_labels = []
    equipped_labels = {}

    dragging = {"item": None, "label": None}

    def update_equipped_display():
        for cat in equipped_labels:
            equipped_labels[cat].destroy()
        equipped_labels.clear()

        for cat, item in player.equipped.items():
            lbl = ctk.CTkLabel(player_frame, text=f"{cat}: {item}", fg_color="#444444", corner_radius=5)
            lbl.pack(pady=2, padx=5, fill="x")
            lbl.bind("<Button-1>", lambda e, c=cat: remove_equipment(c))
            equipped_labels[cat] = lbl

    def remove_equipment(category):
        if category in player.equipped:
            removed = player.equipped.pop(category)
            play_sound("gui/assets/sounds/lose.wav")
            feedback.configure(text=f"🧺 {removed} abgelegt.")
            update_equipped_display()

    def start_drag(label, item):
        dragging["item"] = item
        dragging["label"] = label
        label.configure(fg_color="#4444aa")

    def stop_drag_over_target():
        if dragging["item"]:
            equip_item(dragging["item"])
            dragging["label"].configure(fg_color="#333333")
            dragging["item"] = None
            dragging["label"] = None

    def equip_item(item):
        category = "Shirt" if "Shirt" in item or "Skin" in item else "Zubehör"
        if category in player.equipped:
            feedback.configure(text=f"❗ Du hast bereits ein {category} an!")
        else:
            player.equipped[category] = item
            play_sound("gui/assets/sounds/gain.wav")
            feedback.configure(text=f"✅ {item} ausgerüstet!")
            update_equipped_display()

    for item in player.inventory:
        lbl = ctk.CTkLabel(inventory_frame, text=item, fg_color="#333333", corner_radius=5)
        lbl.pack(pady=2, padx=5, fill="x")
        lbl.bind("<Button-1>", lambda e, l=lbl, i=item: start_drag(l, i))
        item_labels.append(lbl)

    drop_zone = ctk.CTkLabel(player_frame, text="⬇️ Hierher ziehen zum Anlegen", fg_color="#2d2d2d", text_color="#aaaaaa")
    drop_zone.pack(pady=10, padx=10, fill="x")
    drop_zone.bind("<Button-1>", lambda e: stop_drag_over_target())

    update_equipped_display()

    # Sidebar
    sidebar = ctk.CTkFrame(window, fg_color="#2a2a2a", corner_radius=12)
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

    ctk.CTkLabel(sidebar, text=f"Geld: {player.money}€", text_color="green").pack(pady=5)
    ctk.CTkLabel(sidebar, text=f"Rückennr: {player.number}").pack(pady=3)

    # Zurück zum Menü
    ctk.CTkButton(window, text="🔙 Zurück zum Menü", command=lambda: [window.destroy(), back_to_menu()]).pack(pady=20)
