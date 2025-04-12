# """Einstiegspunkt des Spiels."""

# from modules.game_flow import GameFlow

# if __name__ == "__main__":
#     game = GameFlow()
#     game.run()


from gui.app import BasketballGameApp

# Start der GUI-Anwendung
if __name__ == "__main__":
    app = BasketballGameApp()
    app.mainloop()

