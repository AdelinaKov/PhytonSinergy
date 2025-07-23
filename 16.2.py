class Turtle:
    def __init__(self, x=0, y=0, s=1):
        self.x = x
        self.y = y
        self.s = s  # шаг за один ход

    def go_up(self):
        """Увеличивает y на s."""
        self.y += self.s

    def go_down(self):
        """Уменьшает y на s."""
        self.y -= self.s

    def go_left(self):
        """Уменьшает x на s."""
        self.x -= self.s

    def go_right(self):
        """Увеличивает x на s (исправлено: в условии было y, но это ошибка)."""
        self.x += self.s

    def evolve(self):
        """Увеличивает шаг s на 1."""
        self.s += 1

    def degrade(self):
        """Уменьшает шаг s на 1. Если s ≤ 0, вызывает ошибку."""
        if self.s <= 1:
            raise ValueError("Шаг не может быть ≤ 0")
        self.s -= 1

    def count_moves(self, x2, y2):
        """Возвращает минимальное количество ходов для достижения (x2, y2)."""
        dx = abs(x2 - self.x)
        dy = abs(y2 - self.y)
        steps_x = dx // self.s + (1 if dx % self.s != 0 else 0)
        steps_y = dy // self.s + (1 if dy % self.s != 0 else 0)
        return steps_x + steps_y

# Пример использования
turtle = Turtle(0, 0, 2)
turtle.go_right()  # x=2, y=0
turtle.go_up()     # x=2, y=2
print(f"Позиция: ({turtle.x}, {turtle.y})")  # (2, 2)

turtle.evolve()    # s=3
print(f"Текущий шаг: {turtle.s}")  # 3

try:
    turtle.degrade()  # s=2
    turtle.degrade()  # s=1
    turtle.degrade()  # Ошибка: шаг не может быть ≤ 0
except ValueError as e:
    print(e)

print(f"Нужно ходов до (5, 5): {turtle.count_moves(5, 5)}")  # 2 (по x) + 2 (по y) = 4ss