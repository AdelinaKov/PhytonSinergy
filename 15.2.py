class Transport:
    def __init__(self, name, max_speed, mileage):
        self.name = name
        self.max_speed = max_speed
        self.mileage = mileage

    def seating_capacity(self, capacity):
        return f"Вместимость одного автобуса {self.name} {capacity} пассажиров"

# Создаем класс Autobus с переопределенным методом seating_capacity
class Autobus(Transport):
    def seating_capacity(self, capacity=50):
        return super().seating_capacity(capacity)

# Создаем объект Autobus
bus = Autobus("Renaul Logan", 180, 12)

# Выводим информацию
print(bus.seating_capacity())