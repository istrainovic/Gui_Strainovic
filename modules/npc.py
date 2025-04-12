"""Definiert NPC-Klassen im Spiel."""

from modules.character import Character

class Coach(Character):
    """Repräsentiert einen Coach-NPC."""

    def interact(self):
        """Interagiert mit dem Spieler."""
        print(f"Coach {self.name}: 'Du musst härter trainieren, um besser zu werden!'")

class Journalist(Character):
    """Repräsentiert einen Journalisten-NPC."""

    def interact(self):
        """Interagiert mit dem Spieler."""
        print(f"Journalist {self.name}: 'Wie fühlst du dich nach dem letzten Spiel?'")

class Agent(Character):
    """Repräsentiert einen Agent-NPC."""

    def interact(self):
        """Interagiert mit dem Spieler."""
        print(f"Agent {self.name}: 'Ich habe einen neuen Sponsoring-Deal für dich!'")
