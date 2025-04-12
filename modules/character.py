"""Definiert die Basisklasse Character."""

class Character:
    """Repräsentiert einen allgemeinen Charakter im Spiel."""

    def __init__(self, name: str, energy: int):
        self.name = name
        self._energy = energy

    @property
    def energy(self) -> int:
        """Gibt die Energie des Charakters zurück."""
        return self._energy

    @energy.setter
    def energy(self, value: int) -> None:
        """Setzt die Energie des Charakters zwischen 0 und 100."""
        self._energy = max(0, min(value, 100))

    def interact(self):
        """Interagiert mit dem Spieler."""
        pass
