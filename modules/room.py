"""Definiert die Basisklasse Room und spezifische Räume."""

from modules.utils import slow_print
from modules.constants import SHOP_ITEMS, SPONSOR_DEALS
import random


class Room:
    """Basisklasse für alle Räume."""

    def __init__(self, name: str, description: str, npc=None):
        self.name = name
        self.description = description
        self.npc = npc

    def enter(self, player):
        """Aktionen beim Betreten des Raumes."""
        slow_print(f"Du betrittst den Raum: {self.name}")
        slow_print(self.description)
        if self.npc:
            self.npc.interact()
        self.perform_actions(player)

    def perform_actions(self, player):
        """Wird in abgeleiteten Klassen implementiert."""
        pass


class LockerRoom(Room):
    """Repräsentiert den Umkleideraum."""

    def __init__(self, npc=None):
        super().__init__("Umkleideraum", "Hier bereiten sich die Spieler auf das Spiel vor.", npc)

    def perform_actions(self, player):
        while True:
            print("\n1. Statistiken ansehen\n2. Ausrüsten\n3. Duschen\n0. Zurück")
            choice = input("Wähle eine Aktion: ")
            if choice == "1":
                player.show_stats()
            elif choice == "2":
                print(f"Dein Inventar: {', '.join(player.inventory) if player.inventory else 'Leer'}")
            elif choice == "3":
                player.energy = min(100, player.energy + 20)
                slow_print("Du hast geduscht und fühlst dich erfrischt. Energie +20.", 0.05)
            elif choice == "0":
                break
            else:
                print("Ungültige Auswahl.")


class Court(Room):
    """Repräsentiert das Spielfeld."""

    def __init__(self, npc=None):
        super().__init__("Spielfeld", "Das Herz des Spiels. Zeit, dein Können zu zeigen!", npc)

    def perform_actions(self, player):
        slow_print("Das Spiel beginnt! Es gibt vier Viertel, in denen du Entscheidungen treffen kannst.")
        score = 0
        opponent_score = 0
        for quarter in range(1, 5):
            slow_print(f"\n--- Viertel {quarter} ---", 0.05)
            print("Was möchtest du tun?")
            print("1. Werfen")
            print("2. Passen")
            print("3. Verteidigen")
            print("0. Pause einlegen")
            try:
                choice = int(input("Wähle eine Aktion (Nummer): "))
                if choice == 1:  # Werfen
                    if random.random() < 0.6:
                        score += 2
                        slow_print("Du hast gepunktet! 🏀", 0.05)
                    else:
                        slow_print("Dein Wurf war daneben.", 0.05)
                elif choice == 2:  # Passen
                    if random.random() < 0.7:
                        slow_print("Ein perfekter Pass! Dein Team hat gepunktet.", 0.05)
                        score += 2
                    else:
                        slow_print("Der Pass wurde abgefangen.", 0.05)
                elif choice == 3:  # Verteidigen
                    if random.random() < 0.5:
                        slow_print("Du hast erfolgreich verteidigt!", 0.05)
                    else:
                        opponent_score += 2
                        slow_print("Die Gegner haben gepunktet.", 0.05)
                elif choice == 0:  # Pause
                    player.energy = min(100, player.energy + 10)
                    slow_print("Du hast eine Pause gemacht und Energie zurückgewonnen. Energie +10.", 0.05)
                else:
                    print("Ungültige Auswahl.")
            except ValueError:
                print("Bitte gib eine gültige Zahl ein.")
        slow_print(f"\nDas Spiel ist vorbei. Dein Team hat {score} Punkte erzielt, die Gegner {opponent_score}.", 0.05)
        if score > opponent_score:
            slow_print("Herzlichen Glückwunsch! Dein Team hat das Spiel gewonnen! 🎉", 0.05)
        elif score < opponent_score:
            slow_print("Dein Team hat leider verloren. Trainiere weiter, um besser zu werden!", 0.05)
        else:
            slow_print("Das Spiel endet unentschieden. Was für ein spannendes Match!", 0.05)


class Gym(Room):
    """Repräsentiert das Fitnessstudio."""

    def __init__(self, npc=None):
        super().__init__("Fitnessstudio", "Trainiere hier deine Skills.", npc)

    def perform_actions(self, player):
        skill = input("Welchen Skill möchtest du trainieren? (shooting, passing, defense, speed): ").strip().lower()
        if skill in player.attributes:
            player.train(skill)
        else:
            print("Ungültiger Skill. Wähle zwischen: shooting, passing, defense, speed.")


class PressConference(Room):
    """Repräsentiert die Pressekonferenz."""

    def __init__(self, npc=None):
        super().__init__("Pressekonferenz", "Beantworte Fragen und gewinne Follower.", npc)

    def perform_actions(self, player):
        questions = [
            ("Wie fühlst du dich nach dem Spiel?", ["Großartig!", "Es war hart.", "Wir hätten besser spielen können.", "Kein Kommentar."]),
            ("Wie bewertest du deine Leistung?", ["Ich bin zufrieden.", "Ich hätte mehr trainieren sollen.", "Das Team war großartig.", "Die Gegner waren stark."]),
        ]
        for question, answers in random.sample(questions, k=2):
            slow_print(f"\n{question}")
            for i, answer in enumerate(answers, start=1):
                print(f"{i}. {answer}")
            choice = input("Wähle eine Antwort (Nummer): ").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(answers):
                choice = int(choice) - 1
                if choice == 0:
                    player.social_media_followers += 50
                    slow_print("Die Fans lieben deine Antwort! +50 Follower.", 0.05)
                elif choice == 1:
                    player.social_media_followers += 30
                    slow_print("Eine solide Antwort. +30 Follower.", 0.05)
                elif choice == 2:
                    player.social_media_followers += 20
                    slow_print("Ein paar Fans mögen deine Antwort. +20 Follower.", 0.05)
                elif choice == 3:
                    slow_print("Deine Antwort war etwas kontrovers. Keine Änderung.", 0.05)
            else:
                print("Ungültige Auswahl. Keine Followeränderung.")


class Lounge(Room):
    """Repräsentiert die Lounge."""

    def __init__(self, npc=None):
        super().__init__("Lounge", "Entspanne dich und erhole deine Energie.", npc)

    def perform_actions(self, player):
        while True:
            print("\n1. Ruhen\n2. Social Media\n0. Zurück")
            choice = input("Wähle eine Aktion: ").strip()
            if choice == "1":
                player.energy = min(100, player.energy + 20)
                slow_print("Du hast dich ausgeruht. Energie +20.", 0.05)
            elif choice == "2":
                print("1. Beitrag posten\n2. Kommentare beantworten\n0. Zurück")
                social_choice = input("Wähle eine Social-Media-Aktion: ").strip()
                if social_choice == "1":
                    player.social_media_followers += 50
                    slow_print("Dein Beitrag ist beliebt! +50 Follower.", 0.05)
                elif social_choice == "2":
                    player.social_media_followers += 30
                    slow_print("Du hast auf Kommentare geantwortet. +30 Follower.", 0.05)
                elif social_choice == "0":
                    break
                else:
                    print("Ungültige Auswahl.")
            elif choice == "0":
                break
            else:
                print("Ungültige Auswahl.")


class AgentOffice(Room):
    """Repräsentiert das Büro des Agenten."""

    def __init__(self, npc=None):
        super().__init__("Büro des Agenten", "Hier kannst du Sponsoring-Deals abschließen.", npc)

    def perform_actions(self, player):
        print("\nVerfügbare Sponsoring-Verträge:")
        for deal in SPONSOR_DEALS:
            print(f"{deal['name']} - {deal['payout']}$ (Benötigte Follower: {deal['followers_required']})")
        while True:
            choice = input("\nWähle einen Vertrag (Name) oder 'zurück': ").strip()
            if choice.lower() == "zurück":
                break
            for deal in SPONSOR_DEALS:
                if choice == deal["name"]:
                    if player.social_media_followers >= deal["followers_required"]:
                        player.money += deal["payout"]
                        player.sponsor_contracts.append(deal["name"])
                        slow_print(f"Du hast den Vertrag mit {deal['name']} abgeschlossen! +{deal['payout']}$", 0.05)
                    else:
                        slow_print(f"Nicht genug Follower für {deal['name']}.", 0.05)
                    break
            else:
                print("Ungültige Auswahl.")


class Shop(Room):
    """Repräsentiert den Shop."""

    def __init__(self, npc=None):
        super().__init__("Shop", "Hier kannst du Artikel wie Kleidung und Schuhe kaufen.", npc)

    def perform_actions(self, player):
        print("\nVerfügbare Artikel:")
        for item, price in SHOP_ITEMS.items():
            print(f"{item}: {price}$")
        while True:
            choice = input("\nWas möchtest du kaufen? (oder 'zurück'): ").strip()
            if choice.lower() == "zurück":
                break
            if choice in SHOP_ITEMS:
                if player.money >= SHOP_ITEMS[choice]:
                    player.money -= SHOP_ITEMS[choice]
                    player.inventory.append(choice)
                    slow_print(f"Du hast {choice} für {SHOP_ITEMS[choice]}$ gekauft.", 0.05)
                else:
                    slow_print("Nicht genug Geld!", 0.05)
            else:
                print("Ungültige Auswahl.")
