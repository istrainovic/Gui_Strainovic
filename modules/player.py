"""Definiert die Player-Klasse."""

from modules.character import Character
import random

class Player(Character):
    """Repräsentiert einen spielbaren Charakter."""

    def __init__(self, name: str, position: str, height: int, weight: int, nation: str, skin_color: str, accessories: list, energy: int = 100):
        super().__init__(name, energy)
        self.position = position
        self.height = height
        self.weight = weight
        self.nation = nation
        self.skin_color = skin_color
        self.accessories = accessories
        self.attributes = {
            "shooting": 50,
            "passing": 50,
            "defense": 50,
            "speed": 50
        }
        self.money = 1000
        self.social_media_followers = 100
        self.inventory = []
        self.sponsor_contracts = []

    def train(self, skill: str):
        """Verbessert einen spezifischen Skill des Spielers."""
        if self.energy < 10:
            print("Nicht genug Energie zum Trainieren!")
            return
        if skill in self.attributes:
            increase = random.randint(5, 10)
            self.attributes[skill] += increase
            self.energy -= 10
            print(f"{self.name} hat {skill} trainiert. Verbesserung: +{increase}. Energie: {self.energy}")
        else:
            print(f"{skill} ist kein gültiger Skill. Wähle zwischen: {', '.join(self.attributes.keys())}")

    def show_stats(self):
        """Zeigt die aktuellen Statistiken des Spielers an."""
        print("\n--- Aktueller Spielstand ---")
        print(f"Name: {self.name}")
        print(f"Position: {self.position}")
        print(f"Hautfarbe: {self.skin_color}")
        print(f"Nation: {self.nation}")
        print(f"Größe: {self.height} cm")
        print(f"Gewicht: {self.weight} kg")
        print(f"Energie: {self.energy}")
        print(f"Geld: {self.money}")
        print(f"Follower: {self.social_media_followers}")
        print("Fähigkeiten:")
        for skill, value in self.attributes.items():
            print(f"  {skill.capitalize()}: {value}")
        print(f"Accessoires: {', '.join(self.accessories)}")
        print(f"Inventar: {', '.join(self.inventory) if self.inventory else 'Leer'}")
        print(f"Sponsoren: {', '.join(self.sponsor_contracts) if self.sponsor_contracts else 'Keine'}")
        print("----------------------------")
