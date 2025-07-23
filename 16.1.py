class CashRegister:
    def __init__(self, initial_amount=0):
        self.money = initial_amount

    def top_up(self, amount):
        """Пополняет кассу на указанную сумму."""
        self.money += amount

    def count_1000(self):
        """Возвращает количество целых тысяч в кассе."""
        return self.money // 1000

    def take_away(self, amount):
        """Уменьшает количество денег в кассе на указанную сумму.
        Если денег недостаточно, вызывает исключение ValueError."""
        if self.money < amount:
            raise ValueError("Недостаточно денег в кассе")
        self.money -= amount

# Пример использования
kassa = CashRegister(5000)
kassa.top_up(3000)
print(f"Тысяч в кассе: {kassa.count_1000()}")  # 8
kassa.take_away(2000)
print(f"Тысяч в кассе: {kassa.count_1000()}")  # 6
try:
    kassa.take_away(10000)  # Вызовет ошибку
except ValueError as e:
    print(e)  # Недостаточно денег в кассе