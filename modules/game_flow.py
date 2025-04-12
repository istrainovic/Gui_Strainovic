"""Verwaltet den modularen Spielablauf."""

from modules.room import LockerRoom, Court, Gym, PressConference, Lounge, AgentOffice, Shop
from modules.utils import slow_print
from modules.player import Player
from modules.npc import Coach, Journalist, Agent


class GameFlow:
    """Verwaltet den gesamten Spielablauf."""

    def __init__(self):
        self.player = None
        self.rooms = self.initialize_rooms()

    @staticmethod
    def initialize_rooms():
        """Initialisiert die Räume und NPCs."""
        return [
            LockerRoom(npc=Coach("Coach Carter", 100)),
            Court(npc=Coach("Coach Johnson", 100)),
            Gym(npc=Coach("Trainer Max", 100)),
            PressConference(npc=Journalist("Anna Smith", 100)),
            Lounge(npc=Journalist("Sarah Brown", 100)),
            AgentOffice(npc=Agent("Mark Lee", 100)),
            Shop(npc=None)
        ]

    def display_welcome(self):
        """Zeigt eine Begrüßung an."""
        slow_print("**************************************", 0.03)
        slow_print("  Willkommen beim Basketball-Adventure!  ", 0.05)
        slow_print("  Erstelle deinen Spieler und werde ein  ", 0.05)
        slow_print("        echter Basketballstar!          ", 0.05)
        slow_print("**************************************\n", 0.03)

    def display_goodbye(self):
        """Zeigt eine Abschiedsnachricht an."""
        slow_print("\nDanke fürs Spielen! Wir hoffen, du hattest Spaß! Bis zum nächsten Mal! 🏀", 0.05)

    def create_player(self):
        """Erstellt einen neuen Spieler."""
        self.player = self.get_player_data()
        slow_print(f"\nSpieler {self.player.name} erfolgreich erstellt! Viel Erfolg auf deinem Weg zum Ruhm! 🏀", 0.05)

    @staticmethod
    def get_player_data():
        """Fragt den Spieler nach seinen Daten und erstellt ein Player-Objekt."""
        # Name
        name = input("Gib deinem Spieler einen Namen: ").strip()
        while not name:
            print("Der Name darf nicht leer sein. Bitte erneut eingeben.")
            name = input("Gib deinem Spieler einen Namen: ").strip()

        # Position
        positions = ["Point Guard", "Shooting Guard", "Small Forward", "Power Forward", "Center"]
        print("\nWähle eine Position:")
        for i, pos in enumerate(positions, start=1):
            print(f"{i}. {pos}")
        position = GameFlow.get_valid_choice(positions, "Wähle eine Option (Nummer): ")

        # Größe
        height = GameFlow.get_valid_number("Gib die Größe deines Spielers (in cm) ein: ", 150, 250)

        # Gewicht
        weight = GameFlow.get_valid_number("Gib das Gewicht deines Spielers (in kg) ein: ", 50, 150)

        # Hautfarbe
        skin_colors = ["Hell", "Mittel", "Dunkel"]
        print("\nWähle die Hautfarbe:")
        for i, color in enumerate(skin_colors, start=1):
            print(f"{i}. {color}")
        skin_color = GameFlow.get_valid_choice(skin_colors, "Wähle eine Option (Nummer): ")

        # Nation
        nations = ["USA", "Deutschland", "Frankreich", "Spanien", "China", "Brasilien", "Serbien"]
        print("\nWähle die Nation:")
        for i, nation in enumerate(nations, start=1):
            print(f"{i}. {nation}")
        nation = GameFlow.get_valid_choice(nations, "Wähle eine Option (Nummer): ")

        # Trikotnummer
        jersey_number = GameFlow.get_valid_number("Wähle eine Trikotnummer (1-99): ", 1, 99)

        # Accessoires
        accessories = ["Halskette", "Ohrringe", "Armband", "Stirnband"]
        chosen_accessories = GameFlow.get_accessories(accessories)

        # Spieler erstellen
        player = Player(name, position, height, weight, nation, skin_color, chosen_accessories)
        player.attributes["jersey_number"] = jersey_number
        return player

    @staticmethod
    def get_valid_choice(options, prompt):
        """Fragt den Nutzer nach einer gültigen Auswahl aus einer Liste."""
        while True:
            try:
                choice = int(input(prompt))
                if 1 <= choice <= len(options):
                    return options[choice - 1]
                else:
                    print("Bitte gib eine gültige Nummer ein.")
            except ValueError:
                print("Ungültige Eingabe. Bitte gib eine Zahl ein.")

    @staticmethod
    def get_valid_number(prompt, min_value, max_value):
        """Fragt den Nutzer nach einer Zahl innerhalb eines Bereichs."""
        while True:
            try:
                value = int(input(prompt))
                if min_value <= value <= max_value:
                    return value
                else:
                    print(f"Bitte gib eine Zahl zwischen {min_value} und {max_value} ein.")
            except ValueError:
                print("Ungültige Eingabe. Bitte gib eine Zahl ein.")

    @staticmethod
    def get_accessories(accessories):
        """Lässt den Nutzer mehrere Accessoires auswählen."""
        chosen_accessories = []
        print("\nWähle Accessoires (du kannst mehrere wählen):")
        for i, accessory in enumerate(accessories, start=1):
            print(f"{i}. {accessory}")
        while True:
            accessory_choice = input("Gib die Nummer eines Accessoires ein (oder 'fertig', um zu beenden): ").lower()
            if accessory_choice == "fertig":
                break
            try:
                accessory_choice = int(accessory_choice)
                if 1 <= accessory_choice <= len(accessories):
                    chosen_accessories.append(accessories[accessory_choice - 1])
                else:
                    print("Bitte gib eine gültige Nummer ein.")
            except ValueError:
                print("Ungültige Eingabe. Bitte gib eine Zahl ein.")
        return chosen_accessories

    def explore_rooms(self):
        """Ermöglicht das Erkunden von Räumen."""
        while True:
            print("\nRäume:")
            for i, room in enumerate(self.rooms):
                print(f"{i + 1}. {room.name} - {room.description}")
            print("0. Zurück ins Hauptmenü")
            choice = input("Wähle einen Raum (Nummer): ")
            if choice == "0":
                slow_print("\nDu bist zurück im Hauptmenü.", 0.05)
                break
            try:
                room_index = int(choice) - 1
                if 0 <= room_index < len(self.rooms):
                    self.rooms[room_index].enter(self.player)
                else:
                    print("Ungültige Eingabe.")
            except ValueError:
                print("Bitte gib eine gültige Nummer ein.")

    def main_menu(self):
        """Zeigt das Hauptmenü an."""
        slow_print("\nWas möchtest du tun?", 0.05)
        print("1. Neuen Spieler erstellen")
        print("2. Spiel spielen (falls ein Spieler existiert)")
        print("3. Beenden")
        return input("Bitte Auswahl treffen: ")

    def run(self):
        """Startet den Spielablauf."""
        self.display_welcome()
        while True:
            choice = self.main_menu()
            if choice == "1":
                self.create_player()
                self.explore_rooms()
            elif choice == "2":
                if self.player:
                    self.explore_rooms()
                else:
                    slow_print("Es gibt keinen Spieler. Bitte erstelle einen neuen Spieler.", 0.05)
            elif choice == "3":
                self.display_goodbye()
                break
            else:
                slow_print("Ungültige Eingabe. Bitte wähle eine gültige Option.", 0.05)
