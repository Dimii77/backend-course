def log_action(method):
    def wrapper(self, *args, **kwargs):
        print(f"{self.name} → {method.__name__}")
        return method(self, *args, **kwargs)
    return wrapper


class Character:
    count = 0

    def __init__(self, name, hp=100, level=1):
        self.name = name
        self.hp = hp
        self.level = level
        Character.count += 1

    def __str__(self):
        return f"{self.name} (Lv {self.level}, HP {self.hp})"

    def __eq__(self, other):
        return self.name == other.name and self.level == other.level

    def take_damage(self, amount):
        self.hp = max(0, self.hp - amount)

    @property
    def is_alive(self):
        return self.hp > 0

    @log_action
    def attack(self, target):
        target.take_damage(5)

    @classmethod
    def from_string(cls, text):
        name, hp = text.split(";")
        return cls(name, int(hp))

    @staticmethod
    def is_valid_name(name):
        return 2 <= len(name) <= 20


class Warrior(Character):
    def __init__(self, name, hp=100, strength=10):
        super().__init__(name, hp)
        self.strength = strength

    @log_action
    def attack(self, target):
        target.take_damage(self.strength)


class Mage(Character):
    def __init__(self, name, hp=100, mana=50):
        super().__init__(name, hp)
        self.mana = mana

    def __str__(self):
        return f"{super().__str__()} MP {self.mana}"

    @log_action
    def attack(self, target):
        if self.mana >= 10:
            self.mana -= 10
            target.take_damage(20)
        else:
            super().attack(target)


class HealerMixin:
    @log_action
    def heal(self, target, amount):
        target.hp += amount


class Priest(HealerMixin, Mage):
    pass


class Inventory:
    def __init__(self):
        self.items = []

    def add(self, **item):
        self.items.append(item)

    def find(self, **filters):
        return [i for i in self.items
                if all(i.get(k) == v for k, v in filters.items())]

    def __len__(self):
        return len(self.items)


def battle(a, b):
    while a.is_alive and b.is_alive:
        a.attack(b)
        if b.is_alive:
            b.attack(a)
        print(a)
        print(b)
    return a if a.is_alive else b