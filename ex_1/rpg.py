from functools import wraps


#4
def log_action(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        print(f"{self.name} → {func.__name__}")
        return func(self, *args, **kwargs)

    return wrapper


#1 & 3
class Character:
    count = 0

    def __init__(self, name, hp=100, level=1):
        self.name = name
        self._hp = hp
        self.level = level
        Character.count += 1

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        self._hp = max(0, value)

    def __str__(self):
        return f"{self.name} (Lv {self.level}, HP {self.hp})"

    def take_damage(self, amount):
        self.hp -= amount

    @property
    def is_alive(self):
        return self.hp > 0

    #2
    @log_action
    def attack(self, target):
        target.take_damage(5)

    #3
    @classmethod
    def from_string(cls, text):
        parts = text.split(";")
        name = parts[0]
        hp = int(parts[1]) if len(parts) > 1 else 100
        return cls(name, hp=hp)

    @staticmethod
    def is_valid_name(name):
        return 2 <= len(name) <= 20

    def __eq__(self, other):
        if not isinstance(other, Character):
            return False
        return self.name == other.name and self.level == other.level


#2
class Warrior(Character):

    def __init__(self, name, hp=100, level=1, strength=10):
        super().__init__(name, hp=hp, level=level)
        self.strength = strength

    @log_action
    def attack(self, target):
        target.take_damage(self.strength)


class Mage(Character):

    def __init__(self, name, hp=100, level=1, mana=50):
        super().__init__(name, hp=hp, level=level)
        self.mana = mana

    @log_action
    def attack(self, target):
        if self.mana >= 10:
            self.mana -= 10
            target.take_damage(20)
        else:
            super().attack(target)

    def __str__(self):
        base_str = super().__str__()
        return f"{base_str} MP {self.mana}"


#3
class HealerMixin:

    @log_action
    def heal(self, target, amount):
        target.hp += amount

class Priest(HealerMixin, Mage):
    pass


#4
class Inventory:

    def __init__(self):
        self.items = []

    def add(self, **item):
        self.items.append(item)

    def find(self, **filters):
        return [
            item
            for item in self.items
            if all(item.get(k) == v for k, v in filters.items())
        ]

    def __len__(self):
        return len(self.items)


#ბონუსი
def battle(a, b):
    print(f"--- ბრძოლა იწყება: {a.name} VS {b.name} ---")
    while a.is_alive and b.is_alive:
        a.attack(b)
        if not b.is_alive:
            break
        b.attack(a)
        print(f"შედეგი: {a} | {b}")

    winner = a if a.is_alive else b
    print(f"🏆 გამარჯვებულია: {winner.name}!\n")
    return winner


#შემოწმება
if __name__ == "__main__":
    print("--- სავარჯიშო 1 ---")
    a = Character("Tariel")
    b = Character("Avtandil", hp=50)
    b.take_damage(70)

    print(a)  # Tariel (Lv 1, HP 100)
    print(b)  # Avtandil (Lv 1, HP 0)
    print(b.is_alive)  # False
    print(Character.count)  # 2

    print("\n--- საბოლოო მიზნი ---")
    tariel = Warrior("Tariel", hp=120, strength=15)
    nestan = Mage("Nestan", hp=80, mana=50)

    tariel.attack(nestan)
    print(nestan)  # Nestan (Lv 1, HP 65) MP 50
    print(nestan.is_alive) 
