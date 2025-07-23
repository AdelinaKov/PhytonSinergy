class Transport:
    def __init__(self, name, max_speed, mileage):
        self.name = name
        self.max_speed = max_speed
        self.mileage = mileage

# Создаем класс Autobus, наследующий Transport
class Autobus(Transport):
    pass

# Создаем объект Autobus
bus = Autobus("Renaul Logan", 180, 12)

# Выводим информацию
print(f"Название автомобиля: {bus.name} Скорость: {bus.max_speed} Пробег: {bus.mileage}")