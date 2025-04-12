"""Verwaltet die Spielstände."""

class GameData:
    """Verwaltet gespeicherte Spielstände."""

    save_games = {}

    @staticmethod
    def save_game(name: str, player):
        """Speichert den aktuellen Spielstand."""
        GameData.save_games[name] = player

    @staticmethod
    def load_game(name: str):
        """Lädt einen gespeicherten Spielstand."""
        return GameData.save_games.get(name, None)
