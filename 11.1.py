def factorial(n):
    if n == 0 or n == 1:
        return 1
    else:
        return n * factorial(n - 1)

def factorial_list(n):
    fact_n = factorial(n)
    result = []
    for i in range(fact_n, 0, -1):
        result.append(factorial(i))
    return result

# Пример использования
n = int(input("Введите число: "))
print(f"Факториал числа {n}: {factorial(n)}")
print(f"Список факториалов от {factorial(n)} до 1: {factorial_list(n)}")