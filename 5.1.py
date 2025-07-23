num = int(input("Введите целое число: "))

if num == 0:
    print("нулевое число")
else:
    if num > 0:
        sign = "положительное"
    else:
        sign = "отрицательное"
    
    if num % 2 == 0:
        parity = "четное"
        print(f"{sign} {parity} число")
    else:
        print("число не является четным")