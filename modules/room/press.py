import customtkinter as ctk
import pygame
from PIL import Image
import threading
import time

pygame.mixer.init()

def open_press(player, window, back_to_menu):
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

    ctk.CTkLabel(content_frame, text="🎤 Pressekonferenz (Live!)", font=("Arial Black", 24)).pack(pady=10)

    try:
        img = ctk.CTkImage(dark_image=Image.open("gui/assets/images/press.png"), size=(400, 200))
        ctk.CTkLabel(content_frame, image=img, text="").pack(pady=5)
    except:
        pass

    ctk.CTkLabel(content_frame, text="🧑‍💼 Lisa (Reporterin):", font=("Arial", 14, "bold")).pack()
    ctk.CTkLabel(content_frame, text="„Die Kameras laufen. Sie haben 10 Sekunden pro Frage!“", font=("Arial", 13)).pack(pady=(0, 10))

    feedback = ctk.CTkLabel(content_frame, text="", font=("Arial", 14))
    feedback.pack(pady=5)

    timer_label = ctk.CTkLabel(content_frame, text="🕒 10 Sekunden", font=("Arial", 12, "bold"))
    timer_label.pack(pady=(0, 5))

    questions = [
        {
            "q": "Was sagen Sie zu Ihrer Leistung?",
            "options": [
                ("Ich bin top drauf!", 50),
                ("Da geht noch mehr.", 75),
                ("Ich bin der Beste.", -100),
                ("Ich konzentriere mich aufs Team.", 100)
            ]
        },
        {
            "q": "Wie gehen Sie mit der Medienkritik um?",
            "options": [
                ("Ich lese alles – motiviert mich.", 75),
                ("Ich schieße zurück.", -100),
                ("Ich blende es aus.", 50),
                ("Ich wachse daran.", 100)
            ]
        }
    ]

    question_index = [0]
    selected_option = ctk.StringVar()
    option_buttons = []
    timer_running = [False]

    def timeout_action():
        feedback.configure(text="⌛ Zeit abgelaufen! Du hast keine Antwort gegeben.")
        play_sound("gui/assets/sounds/lose.wav")
        player.followers -= 50
        refresh_bars()
        next_question()

    def start_timer():
        timer_running[0] = True
        for i in range(10, 0, -1):
            if not timer_running[0]:
                return
            timer_label.configure(text=f"🕒 {i} Sekunden")
            time.sleep(1)
        if timer_running[0]:
            timer_label.configure(text="⏱ Zeit vorbei")
            timeout_action()

    def next_question():
        timer_running[0] = False
        for widget in content_frame.winfo_children():
            if isinstance(widget, (ctk.CTkRadioButton, ctk.CTkButton)) and widget.cget("text") != "🔙 Zurück zum Menü":
                widget.destroy()

        if question_index[0] >= len(questions):
            feedback.configure(text="📸 Pressekonferenz beendet.")
            timer_label.configure(text="")
            return

        selected_option.set("")
        current = questions[question_index[0]]
        ctk.CTkLabel(content_frame, text=current["q"], font=("Arial", 14, "bold")).pack(pady=10)

        option_buttons.clear()
        for text, impact in current["options"]:
            rb = ctk.CTkRadioButton(content_frame, text=text, variable=selected_option, value=text)
            rb.pack(anchor="w", padx=40, pady=2)
            option_buttons.append((rb, impact))

        def confirm():
            choice = selected_option.get()
            if not choice:
                feedback.configure(text="❗ Bitte wähle eine Antwort.")
                return
            timer_running[0] = False
            for btn, impact in option_buttons:
                if btn.cget("text") == choice:
                    player.followers += impact
                    play_sound("gui/assets/sounds/gain.wav" if impact > 0 else "gui/assets/sounds/lose.wav")
                    feedback.configure(text=f"Antwort: „{choice}“ ➤ {'+' if impact > 0 else ''}{impact} Follower")
                    refresh_bars()
                    break
            question_index[0] += 1
            next_question()

        ctk.CTkButton(content_frame, text="Antwort bestätigen", command=confirm).pack(pady=10)

        threading.Thread(target=start_timer, daemon=True).start()

    next_question()

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

    # Zurück-Button
    btn_frame = ctk.CTkFrame(window, fg_color="transparent")
    btn_frame.pack(side="bottom", pady=20)
    ctk.CTkButton(btn_frame, text="🔙 Zurück zum Menü", command=lambda: [window.destroy(), back_to_menu()]).pack()
