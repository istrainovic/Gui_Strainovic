# modules/player.py

class Player:
    def __init__(self, name, position, origin, style, accessories, weight, height, skin_color):
        self.name = name
        self.position = position
        self.origin = origin
        self.style = style
        self.accessories = accessories
        self.weight = weight
        self.height = height
        self.skin_color = skin_color

        self.xp = 0
        self.level = 1
        self.energy = 100
        self.money = 100
        self.followers = 0

        self.inventory = []
        self.skins = []           
        self.equipped = {}        

    def gain_xp(self, amount):
        self.xp += amount

    def use_energy(self, amount):
        self.energy = max(0, self.energy - amount)

    def add_money(self, amount):
        self.money += amount

    def remove_money(self, amount):
        if self.money >= amount:
            self.money -= amount
