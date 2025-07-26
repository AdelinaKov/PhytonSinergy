import random
import time
import os
import json
import sys
import threading

# Эмодзи для отображения
EMPTY = ' '
TREE = '🌲'
BURNING_TREE = '🔥'
BURNT_TREE = '🪵'
RIVER = '🌊'
HELICOPTER = '🚁'
HOSPITAL = '🏥'
SHOP = '🏪'
CLOUD = '☁️'
LIGHTNING = '⚡'

TICK_TIME = 1.0  # время одного тика в секундах

class Cell:
    def __init__(self, x, y, kind=EMPTY):
        self.x = x
        self.y = y
        self.kind = kind  # тип клетки
        self.on_fire = False
        self.fire_timer = 0  # сколько тиков горит клетка

    def is_walkable(self):
        # Вертолёт может летать над пустыми, водой, госпиталем, магазином, облаками и деревьями
        return self.kind in [EMPTY, RIVER, HOSPITAL, SHOP, CLOUD, TREE]

    def symbol(self):
        if self.on_fire:
            return BURNING_TREE
        if self.kind == TREE:
            return TREE
        if self.kind == RIVER:
            return RIVER
        if self.kind == BURNT_TREE:
            return BURNT_TREE
        if self.kind == HOSPITAL:
            return HOSPITAL
        if self.kind == SHOP:
            return SHOP
        if self.kind == CLOUD:
            return CLOUD
        return EMPTY


class Helicopter:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.water = 0
        self.water_capacity = 1
        self.lives = 3
        self.score = 0
        self.health = 3

    def can_extinguish(self):
        return self.water > 0

    def refill_water(self):
        self.water = self.water_capacity


class Game:
    FIRE_DURATION = 10  # Время горения дерева в тиках (примерно 10 секунд)
    MAX_BURNING_TREES = 3  # Максимум одновременно горящих деревьев

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.map = [[Cell(x, y) for x in range(width)] for y in range(height)]
        self.helicopter = Helicopter(0, 0)
        self.hospital_pos = None
        self.shop_pos = None
        self.tick_count = 0
        self.clouds = []
        self.lock = threading.Lock()
        self.running = True

        self.load_or_new()

    def load_or_new(self):
        if os.path.exists('savegame.json'):
            self.load_game()
        else:
            self.generate_map()
            self.place_hospital()
            self.place_shop()
            self.place_helicopter()
            self.spawn_clouds()

    def generate_map(self):
        # Река - вертикальная полоса
        river_x = random.randint(self.width // 4, 3 * self.width // 4)
        for y in range(self.height):
            self.map[y][river_x].kind = RIVER
            if river_x + 1 < self.width:
                self.map[y][river_x + 1].kind = RIVER

        # Деревья случайно по карте, примерно 20% клеток
        tree_count = (self.width * self.height) // 5
        placed = 0
        while placed < tree_count:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if self.map[y][x].kind == EMPTY:
                self.map[y][x].kind = TREE
                placed += 1

    def place_hospital(self):
        while True:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if self.map[y][x].kind == EMPTY:
                self.map[y][x].kind = HOSPITAL
                self.hospital_pos = (x, y)
                break

    def place_shop(self):
        while True:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if self.map[y][x].kind == EMPTY:
                self.map[y][x].kind = SHOP
                self.shop_pos = (x, y)
                break

    def place_helicopter(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.map[y][x].kind == EMPTY:
                    self.helicopter.x = x
                    self.helicopter.y = y
                    return

    def spawn_clouds(self):
        self.clouds = []
        for _ in range(random.randint(1, 5)):
            while True:
                x = random.randint(0, self.width - 1)
                y = random.randint(0, self.height - 1)
                if self.map[y][x].kind == EMPTY:
                    self.clouds.append((x, y))
                    self.map[y][x].kind = CLOUD
                    break

    def clear_clouds(self):
        for (x, y) in self.clouds:
            if self.map[y][x].kind == CLOUD:
                self.map[y][x].kind = EMPTY
        self.clouds = []

    def update_fire(self):
        new_fires = []
        for y in range(self.height):
            for x in range(self.width):
                cell = self.map[y][x]
                if cell.on_fire:
                    cell.fire_timer -= 1
                    if cell.fire_timer <= 0:
                        # Дерево сгорело
                        cell.kind = BURNT_TREE
                        cell.on_fire = False
                        self.helicopter.score -= 1  # штраф за потерю дерева
                    else:
                        # Пока дерево горит, распространяем огонь на соседей
                        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                            nx, ny = x + dx, y + dy
                            if 0 <= nx < self.width and 0 <= ny < self.height:
                                neighbor = self.map[ny][nx]
                                if neighbor.kind == TREE and not neighbor.on_fire:
                                    if len(self.get_burning_trees()) + len(new_fires) < self.MAX_BURNING_TREES:
                                        if random.random() < 0.3:
                                            new_fires.append(neighbor)
        for cell in new_fires:
            cell.on_fire = True
            cell.fire_timer = self.FIRE_DURATION

    def get_burning_trees(self):
        return [c for row in self.map for c in row if c.on_fire]

    def grow_trees(self):
        for y in range(self.height):
            for x in range(self.width):
                c = self.map[y][x]
                if c.kind == EMPTY and random.random() < 0.05:
                    c.kind = TREE

    def start_fires(self):
        burning = self.get_burning_trees()
        if len(burning) >= self.MAX_BURNING_TREES:
            return  # Уже горит максимум деревьев
        trees = [
            self.map[y][x]
            for y in range(self.height)
            for x in range(self.width)
            if self.map[y][x].kind == TREE and not self.map[y][x].on_fire
        ]
        if trees and random.random() < 0.1:
            f = random.choice(trees)
            f.on_fire = True
            f.fire_timer = self.FIRE_DURATION

    def move_helicopter(self, dx, dy):
        nx = self.helicopter.x + dx
        ny = self.helicopter.y + dy
        if 0 <= nx < self.width and 0 <= ny < self.height:
            cell = self.map[ny][nx]
            if cell.is_walkable():
                self.helicopter.x = nx
                self.helicopter.y = ny

                if cell.kind == RIVER:
                    self.helicopter.refill_water()

                if (nx, ny) == self.hospital_pos:
                    if self.helicopter.score >= 5 and self.helicopter.health < 3:
                        self.helicopter.score -= 5
                        self.helicopter.health += 1

                if (nx, ny) == self.shop_pos:
                    if self.helicopter.score >= 10:
                        self.helicopter.score -= 10
                        self.helicopter.water_capacity += 1

    def extinguish(self):
        c = self.map[self.helicopter.y][self.helicopter.x]
        if c.on_fire and self.helicopter.can_extinguish():
            c.on_fire = False
            c.fire_timer = 0
            c.kind = TREE
            self.helicopter.water -= 1
            self.helicopter.score += 3

    def draw(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        for y in range(self.height):
            row = ''
            for x in range(self.width):
                if self.helicopter.x == x and self.helicopter.y == y:
                    row += HELICOPTER
                else:
                    row += self.map[y][x].symbol()
            print(row)
        print(
            f"Очки: {self.helicopter.score}  Вода: {self.helicopter.water}/{self.helicopter.water_capacity}"
            + f"  Жизни: {self.helicopter.lives}  Здоровье: {self.helicopter.health}"
        )
        print("Управление: WASD - движение, E - тушить, Q - выход, S - сохранить, L - загрузить")

    def cloud_effects(self):
        self.clear_clouds()
        self.spawn_clouds()
        burning = self.get_burning_trees()
        if len(burning) >= self.MAX_BURNING_TREES:
            return  # Не создаём новый пожар, если лимит достигнут
        if random.random() < 0.2:
            trees = [
                self.map[y][x]
                for y in range(self.height)
                for x in range(self.width)
                if self.map[y][x].kind == TREE and not self.map[y][x].on_fire
            ]
            if trees:
                f = random.choice(trees)
                f.on_fire = True
                f.fire_timer = self.FIRE_DURATION

    def save_game(self):
        data = {
            "width": self.width,
            "height": self.height,
            "map": [[{"kind": c.kind, "on_fire": c.on_fire, "fire_timer": c.fire_timer} for c in row] for row in self.map],
            "helicopter": {
                "x": self.helicopter.x,
                "y": self.helicopter.y,
                "water": self.helicopter.water,
                "water_capacity": self.helicopter.water_capacity,
                "lives": self.helicopter.lives,
                "score": self.helicopter.score,
                "health": self.helicopter.health,
            },
            "hospital_pos": self.hospital_pos,
            "shop_pos": self.shop_pos,
            "tick_count": self.tick_count,
        }
        with open("savegame.json", "w", encoding="utf-8") as f:
            json.dump(data, f)

    def load_game(self):
        with open("savegame.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        self.width = data["width"]
        self.height = data["height"]
        self.map = [[Cell(x, y) for x in range(self.width)] for y in range(self.height)]
        for y in range(self.height):
            for x in range(self.width):
                cell_data = data["map"][y][x]
                self.map[y][x].kind = cell_data["kind"]
                self.map[y][x].on_fire = cell_data["on_fire"]
                self.map[y][x].fire_timer = cell_data.get("fire_timer", 0)
        h = data["helicopter"]
        self.helicopter = Helicopter(h["x"], h["y"])
        self.helicopter.water = h["water"]
        self.helicopter.water_capacity = h["water_capacity"]
        self.helicopter.lives = h["lives"]
        self.helicopter.score = h["score"]
        self.helicopter.health = h["health"]
        self.hospital_pos = tuple(data["hospital_pos"])
        self.shop_pos = tuple(data["shop_pos"])
        self.tick_count = data.get("tick_count", 0)
        self.spawn_clouds()

    def game_over(self):
        print("Игра окончена!")
        print(f"Ваш счет: {self.helicopter.score}")
        if os.path.exists("savegame.json"):
            os.remove("savegame.json")
        sys.exit(0)

    def tick(self):
        with self.lock:
            self.tick_count += 1
            self.grow_trees()
            self.start_fires()
            self.update_fire()
            if self.tick_count % 10 == 0:
                self.cloud_effects()
            c = self.map[self.helicopter.y][self.helicopter.x]
            if c.on_fire:
                self.helicopter.health -= 1
                if self.helicopter.health <= 0:
                    self.helicopter.lives -= 1
                    if self.helicopter.lives <= 0:
                        self.game_over()
                    else:
                        print("Вертолёт потерял жизнь! Возрождаемся...")
                        self.helicopter.health = 3
                        self.place_helicopter()

    def run(self):
        def tick_loop():
            while self.running:
                self.tick()
                self.draw()
                time.sleep(TICK_TIME)

        tick_thread = threading.Thread(target=tick_loop, daemon=True)
        tick_thread.start()

        while True:
            cmd = input().lower()
            with self.lock:
                if cmd == "q":
                    print("Выход из игры...")
                    self.running = False
                    break
                elif cmd == "w":
                    self.move_helicopter(0, -1)
                elif cmd == "a":
                    self.move_helicopter(-1, 0)
                elif cmd == "s":
                    self.move_helicopter(0, 1)
                elif cmd == "d":
                    self.move_helicopter(1, 0)
                elif cmd == "e":
                    self.extinguish()
                elif cmd == "l":
                    self.load_game()
                elif cmd == "save" or cmd == "s":
                    self.save_game()
                    print("Игра сохранена.")
                else:
                    print(
                        "Неверная команда. WASD - движение, E - тушить, Q - выход, S - сохранить, L - загрузить"
                    )


if __name__ == "__main__":
    print("Введите ширину игрового поля (например, 20): ")
    w = int(input())
    print("Введите высоту игрового поля (например, 10): ")
    h = int(input())
    game = Game(w, h)
    game.run()
